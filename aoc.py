#!/usr/bin/env python3
import argparse
import subprocess
import urllib.request
from pathlib import Path


directory_by_lang = {
    "py": "python",
    "go": "golang",
}

DESCRIPTION = """\
Shortcut script to prepare and run a solution to a puzzle of https://adventofcode.com.

By default, the script is executed with the input that is generated specifically
for the authenticated user. If missing, this input must be downloaded from the
website which requires being authenticated. See --example for more info.

By default, scripts are run in optimized mode (no debug messages).
See --debug for more info.

ABOUT AUTHENTICATION

To download puzzles from the website, a cookie header is required.
This scripts expects to find the cookie string in `./.cookie`.

The file must be crated manually, and must contain a valid cookie. To get one,
authenticate on the website, then take the "Cookie" header from a request using
your browser debugger, and then copy & paste it in the .cookie file.
"""

p = argparse.ArgumentParser(
    description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

p.add_argument("year", type=int).help = """\
The year of the puzzle to execute. e.g. "2022", "2021"
"""

p.add_argument("day", type=int).help="""\
The day (or id) of the puzzle. e.g. "1", "2".
"""

p.add_argument("lang", choices=directory_by_lang).help = """\
The programming language to use (corresponds to the file extension).

Also prepares a solution file based on the language tempalte, if it does not yet exist.
"""

p.add_argument("-e", "--example", nargs="?", default=False, const=True).help = """\
Use an example input file instead of the user specific input file.

The example file is created if missing but its content must be retrieved manually
from the website's puzzle description (it can't reliably be scrapped from the page).

EXAMPLES:
    aoc 2022 6 py -e        ->  inputs/year_2022/day_06_example.txt
    aoc 2022 6 py -e 1      ->  inputs/year_2022/day_06_example_1.txt
    aoc 2022 6 py -e hello  ->  inputs/year_2022/day_06_example_hello.txt
"""

p.add_argument("-d", "--debug", action="store_true").help = """\
Enable debugging mode (disable optimization) and write debug messages to `debug.log`.
"""

p.add_argument("--timeout", type=int, default=5).help = """\
Interrupt execution if it takes more than the given time in seconds.

Defaults to 5 seconds.
"""



class Args(argparse.Namespace):
    year: int
    day: int
    lang: str
    example: bool | str
    debug: bool
    timeout: int


args = p.parse_args(namespace=Args())

directory = directory_by_lang[args.lang]
ex_id = "_example" + (f"_{args.example}" if isinstance(args.example, str) else "")
oday = f"{args.day:0>2}"

input_file_example = Path("inputs") / f"year_{args.year}" / f"day_{oday}{ex_id}.txt"
input_file_user    = Path("inputs") / f"year_{args.year}" / f"day_{oday}.txt"
code_day           = Path(directory) / f"year_{args.year}" / f"day_{oday}.{args.lang}"
template_day       = Path(directory) / f"template_day"
code_base          = Path(directory) / f"year_{args.year}" / f"base.{args.lang}"
template_base      = Path(directory) / f"template_base"

aoc_url = f"https://adventofcode.com/{args.year}/day/{args.day}/input"
aoc_cookie = Path(".cookie").read_text().strip()

input_file = input_file_example if args.example else input_file_user


if not args.example and not input_file_user.exists():
    print(f"[INFO] Retrieving input from {aoc_url}")

    req = urllib.request.Request(aoc_url, method="GET")
    req.add_header("Cookie", aoc_cookie)

    with urllib.request.urlopen(req) as res:
        text = res.read().decode()

    print(f"[INFO] Writing input file")

    input_file_user.parent.mkdir(parents=True, exist_ok=True)
    input_file_user.write_text(text)


if not input_file_example.exists():
    print(f"[INFO] Writing example file (no content)")

    input_file_example.parent.mkdir(parents=True, exist_ok=True)
    input_file_example.touch()


if template_day.exists() and not code_day.exists():
    print(f"[INFO] Writing solution file")

    content = template_day.read_text()

    code_day.parent.mkdir(parents=True, exist_ok=True)
    code_day.write_text(content)

if template_base.exists() and not code_base.exists():
    print(f"[INFO] Writing year base file")

    content = template_base.read_text()
    code_base.write_text(content)

if args.lang == "go":
    assert code_base.exists()
    content = code_base.read_text().replace(f"nil, // Day{oday}{{}}", f"Day{oday}{{}},")
    code_base.write_text(content)


# TODO: handle more languages
CMD = None
if args.lang == "py":
    if args.debug:
        CMD = f"python {code_day} < {input_file} 2> debug.log"
    else:
        CMD = f"python -O {code_day} < {input_file}"

if args.lang == "go":
    if args.debug:
        CMD = f"go run ./golang {args.year} {args.day} < {input_file} 2> debug.log"
    else:
        CMD = f"go build -o golang/aoc -ldflags '-s' ./golang && golang/aoc {args.year} {args.day} < {input_file}"

if CMD is not None:
    print(CMD)
    try:
        subprocess.run(CMD, shell=True, timeout=args.timeout)
    except TimeoutError:
        print(f"[Timeout {args.timeout}]")
