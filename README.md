# Advent Of Code

This is just a personal repo for puzzles of https://adventofcode.com.

Contains a cool helper script to automatically download, organize and run a
puzzle by simply giving a **year** and a **day** in the CLI.

Initially thought to work with python files but it should work with any immediately
executable script file (as opposed to files that need to be compiled first).

## Get started

- Have python installed (3.10 at least)

- Setup authentication
  (This lets you download your input files from https://adventofcode.com)

  - If not done already, create an account on https://adventofcode.com
  - Authenticate on the website
  - inspect requests
  - retrieve the `Cookie` header
  - paste it in the [.cookie](./.cookie) file

- [aoc.py](./aoc.py) should already be executable.
  (If not, run `chmod u+x aoc.py` on Linux/MacOS)

- Prepare a puzzle, for example the first of 2022: `./aoc.py 2022 1`

  - This also runs the file but if it did not exist, it won't do much at first 😅

- Happy coding! 🎉


## Logging

By default, stderr will not appear in the console when running a puzzle solution.
Even if enabled, there is an arbitrary limit to the number of stderr lines that
will be printed.

This is to avoid flooding the terminal when running a puzzle with user specific
input that tends to be large.

It is possible to go against this default behaviour, here are some examples:

```sh
# Enable printing of errors and logging messages
./aoc.py 2022 1 -d
./aoc.py 2022 1 --debug
# Also increase the maximum number of debug lines to 1000
./aoc.py 2022 1 -d --max-debug-lines 1000
```

> **NOTE**: Stderr is intercepted by the `aoc.py` script but there is currently
> no attempt to limit the performance impact of printing to stderr in puzzle
> solutions.

## Project structure

Organization of files related to working on a puzzle

```
  ├── puzzles
  │   └── <year>
  │       ├── examples
  │       │   └── <n>.txt      Must be created manually
  │       │
  │       ├── inputs           (Not tracked by git)
  │       │   └── <n>.txt      Automatically downloaded from website
  │       │
  │       └── solutions
  │           └── <n>.<ext>    Automatically created (uses template if available)
  │
  ├── templates
  │   └── .<ext>    May be written to speedup initialization of a puzzle
  │
  ├── .cookie       (Not tracked by git)
  │
  └── aoc.py        Entry point
```

## TODO

Add support for rust files.

## Disclaimer

I'm not trying to make this work on Windows. It might work, but I doubt it.
