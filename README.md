# Advent Of Code

This is just a personal repo for puzzles of https://adventofcode.com.

Contains a cool helper script to automatically download, organize and run a
puzzle by simply giving a **year** and a **day** in the CLI.

Only works with python for now, but I intend to add other languages, one day.

## Get started

- Have python installed (3.10 at least)

- Setup the authentication
  (This lets you download your input files from https://adventofcode.com)

  - If not done already, create an account on https://adventofcode.com
  - Authenticate on the website
  - inspect requests
  - retrieve the `Cookie` header
  - paste it in the [.cookie](./.cookie) file

- [aoc.py](./aoc.py) should already be executable.
  (If not, run `chmod u+x aoc.py` on Linux/MacOS)

- Optionally add a symlink of `aoc.py` in a directory that is in the PATH for extra conciseness:
  - `ln -s path/to/this-project/aoc.py  ~/.local/bin/aoc`

- Prepare a puzzle, for example the first of 2022: `aoc 2022 1`

- Write a solution in the generated solution file

- Re-run `aoc 2022 1` to check the result

Variations on the command:

```sh
aoc 2022 1
aoc 2022 1 -e
aoc 2022 1 -e1
aoc 2022 1 -e foo
aoc 2022 1 -d
aoc 2022 1 --debug
```

## Project structure

Organization of files related to working on a puzzle

```
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
  ├── <language>
  │   └── year_<year>
  │       │
  │       ├── template.<ext>    May be written to speedup initialization of a puzzle
  │       │
  │       └── day_<0n>.<ext>    Automatically created, using the language's template if available
  │
  ├── .cookie       (Not tracked in git)
  │
  └── aoc.py        Entry point
```
