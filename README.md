# Advent of code 2024

This repository contains the solutions to the problems of Advent of Code 2024. The solutions are written in Python and
DuckDB (so far).

## Project structure

```
.
├── .github
│  └── workflows
│     └── ci-lint.yml    <----- GitHub Actions workflow for linting
├── .gitignore           <----- Git ignore file
├── aoc2024
│  ├── day1
│  │  └── solution.py    <----- Solution for day 1
│  ├── day2
│  │  └── solution.py    <----- Solution for day 2
│  ...
│  └── helpers.py        <----- Helper functions
├── data                 <----- Sample data files, as defined in problem statement
│  ├── day1              <----- Day 1 data
│  │  └── input.txt      <----- File containing input for day 1
│  ├── day2              <----- Day 2 data
│  │  └── input.txt      <----- File containing input for day 2
│  ...
├── poetry.lock          <----- Poetry lock file
├── pyproject.toml       <----- Poetry project file
└── README.md            <----- This file
```

## Running

To run the solution for a specific day, use the following command:

```bash
poetry run aoc2024 <day>
```

For example, to run the solution for day 1:

```bash
poetry run aoc2024 1
```

The DuckDB solution can be run instead of the (default) Python solution by adding the `--duckdb` flag:

```bash
poetry run aoc2024 1 --duckdb
```
