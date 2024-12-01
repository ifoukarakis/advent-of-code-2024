import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description="Advent of Code 2024")
    parser.add_argument("day", type=int, help="Day of the challenge")
    parser.add_argument("--duck", help="Run duck db solution", action="store_true")
    args = parser.parse_args()

    if args.day < 0 or args.day > 25:
        print("day number must be between 1 and 25")
        exit()

    if args.duck:
        stack = "DuckDB"
        sol = importlib.import_module(f"aoc2024.day{args.day}.duck")
    else:
        stack = "Python"
        sol = importlib.import_module(f"aoc2024.day{args.day}.solution")
    print(f"Answer to day {args.day} - Implemented using {stack}\n")
    sol.solution()


if __name__ == "__main__":
    main()
