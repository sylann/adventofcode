# Advent Of Code

This is just a personal repo for puzzles of https://adventofcode.com.

Contains helper scripts to automatically download, organize and run a
puzzle by simply giving a **year**, a **day** and a **lang** in the CLI.

Only works with python and go for now. More languages to come!

Currently trying to add benchmarking and profiling stuff, but I don't know much about it at this point.

## Get started

- Prepare a puzzle solution: `bin/new.sh 2023 1 py`
  - Also get the user input: `bin/new.sh 2023 1 py --get`

- Run a puzzle solution: `bin/run.sh 2023 1 py`

**Requirements**:
- Python 3.10 is required to execute python solutions
- Golang 1.21 is required to execute go solutions

- You need to setup the [.cookie](./.cookie) file to be able to download the user-specific input from https://adventofcode.com.
  - If not done already, create an account on https://adventofcode.com
  - Authenticate on the website
  - inspect requests
  - retrieve the `Cookie` header
  - paste it in the [.cookie](./.cookie) file

## Project structure

Organization of files related to working on a puzzle

```
  ├── bin
  │   ├── new.sh    Prepare a puzzle
  │   └── run.sh    Execute a puzzle solution
  │
  ├── inputs
  │   └── year_<year>
  │       │
  │       │    Example files must be created manually.
  │       │
  │       ├── day_<0n>_example.txt         Default example name
  │       ├── day_<0n>_example_1.txt       Default for part 1 (Uses base default if missing)
  │       ├── day_<0n>_example_2.txt       Default for part 2 (Uses base default if missing)
  │       ├── day_<0n>_example_<id>.txt    Additional example names can be used from the CLI
  │       │
  │       │    User specific input files are downloaded from the website. They are not tracked in GIT
  │       │    because it seems to be a well established convention to not share them.
  │       │
  │       └── day_<0n>.txt
  │
  ├── src
  │   └── <lang>
  │       └── year_<year>
  │           │
  │           ├── template_base   May be used as a year entry point for some languages
  │           ├── template_day    May be written to speedup initialization of a puzzle
  │           │
  │           └── day_<0n>.<ext>    Automatically created, using the language's template if available
  │
  └── .cookie       (Not tracked in git)
  
```
