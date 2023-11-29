import urllib.request, urllib.parse
import os, sys, json, datetime
from time import sleep
from pathlib import Path


class Files:
    @staticmethod
    def download_puzzle_input(day):
        session = Files.get_session()
        year = Files.get_path().split(os.sep)[-1].split("-")[-1]

        headers = Files.get_headers()
        headers["Referer"] = f"https://adventofcode.com/{year}/day/{day}"
        headers["Cookie"] = f"session={session}"

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        method = "GET"

        req = urllib.request.Request(url, method=method, headers=headers)

        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")

        return content

    @staticmethod
    def add_day(day):
        path = Files.get_path()

        solution = os.path.realpath(f"{path}/solutions/day{day:02}.py")
        solution_path = Path(solution)
        if not solution_path.exists():
            remote_file = "https://raw.githubusercontent.com/nitekat1124/aoc-tool/files/template-files/solutions/day_sample.py"
            with urllib.request.urlopen(remote_file) as response:
                remote_content = response.read().decode("utf-8")
            with open(solution, "w+") as f:
                f.write(remote_content)
                print("Created file: " + solution)

        folder = os.path.realpath(f"{path}/data/day{day:02}")
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        files = ["puzzle_input.txt", "test_1_input.txt", "test_1_part1_result.txt", "test_1_part2_result.txt"]
        for file in files:
            file_path = Path(f"{folder}/{file}")
            if not file_path.exists():
                file_path.touch()
                print("Created file:", file_path)

        input_path = Path(f"{folder}/{files[0]}")
        if input_path.stat().st_size == 0:
            now = datetime.datetime.utcnow()
            available_to_download = datetime.datetime(int(path.split(os.sep)[-1].split("-")[-1]), 12, day, 5, 0, 0)
            if now < available_to_download:
                print("Puzzle input not available to download until", available_to_download.strftime("%Y-%m-%d %H:%M:%S"), "UTC\n")
            while now < available_to_download:
                print("\033[Fnow:", now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], "UTC")
                sleep(1)
                now = datetime.datetime.utcnow()

            print("Downloading puzzle input...")
            with open(input_path, "w+") as f:
                f.write(Files.download_puzzle_input(day))
                print("Downloaded puzzle input to:", input_path)

    @staticmethod
    def add_test_file(day, test_no):
        path = Files.get_path()
        folder = os.path.realpath(f"{path}/data/day{day:02}")
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        files = [f"test_{test_no}_input.txt", f"test_{test_no}_part1_result.txt", f"test_{test_no}_part2_result.txt"]
        for file in files:
            file_path = Path(f"{folder}/{file}")
            if not file_path.exists():
                file_path.touch()
                print("Created test file:", file_path)

    @staticmethod
    def get_session():
        session = ""
        path = Files.get_path()
        session_path = os.path.realpath(f"{path}/../aoc_session")
        with open(session_path, "r") as f:
            session = f.read().strip()
        return session

    @staticmethod
    def get_headers():
        headers = {}
        path = Files.get_path()
        headers_config_path = os.path.realpath(f"{path}/../aoc_headers.json")
        with open(headers_config_path, "r") as f:
            headers = json.loads(f.read().strip())
        return headers

    @staticmethod
    def get_path():
        return path if os.path.isdir(path := os.path.realpath(sys.argv[0])) else os.path.dirname(path)
