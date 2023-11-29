import argparse, importlib, datetime
from utils.submission import Submission
from utils.files import Files


def main():
    _today = datetime.date.today().day

    parser = argparse.ArgumentParser(description="Advent of Code solution runner")
    parser.add_argument("-d", "--day", dest="day", default=_today, metavar="day_number", type=int, help="Required, day number of the AoC event")
    parser.add_argument("-p", "--part", dest="part", default=1, metavar="part_number", type=int, help="Required, part number of the day of the AoC event")
    parser.add_argument("--raw", action="store_true", help="Optional, use raw input instead of stripped input")
    parser.add_argument("--add", action="store_true", help="Optional, create daily file")
    parser.add_argument("--add-test-file", metavar="test_number", type=int, help="Optional, create additional test files")
    parser.add_argument("--skip-test", action="store_true", help="Optional, skipping tests")
    parser.add_argument("--benchmark", action="store_true", help="Optional, benchmarking the code, and also skipping tests")
    parser.add_argument("--submit", action="store_true", help="Optional, submit your answer to AoC")
    args = parser.parse_args()

    if not 0 < args.day < 26:
        print("day number must be between 1 and 25")
        exit()
    elif args.add is True:
        print("Adding day", args.day)
        Files.add_day(args.day)
    elif args.add_test_file is not None:
        print("Adding test file for day", args.day, ", no", args.add_test_file)
        Files.add_test_file(args.day, args.add_test_file)
    elif args.part not in [1, 2]:
        print("part number must be 1 or 2")
        exit()
    else:
        print(f"Solving day {args.day} part {args.part}\n")
        sol = importlib.import_module(f"solutions.day{args.day:02d}").Solution(args.day, args.raw, args.skip_test, args.benchmark)
        print(f"the answer is {answer}\n" if (answer := sol.solve(part_num=args.part)) is not None else "")
        sol.benchmark(_print=True)

        if answer and args.submit is True:
            Submission.send_answer(args.day, args.part, answer)


if __name__ == "__main__":
    main()
