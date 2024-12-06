# #!/usr/bin/env bash
usage="
USAGE: $0 YEAR DAY LANG [-d] [-e] [-E NAME]

    YEAR       a number between 2010 and 2030  (we'll see if this code survives that long)
    DAY        a number between 1 and 25
    LANG       one of the supported languages: py, go, rs, ml
    -d         enable debug / disable optimization
    -e         use example instead of user input
    -E NAME    use specific example with given NAME
"
while [[ $# -gt 0 ]]; do case $1 in
	20[1-3][0-9])         year="$1";      shift ;;
	[1-9]|1[0-9]|2[0-5])  day="$1";       shift ;;
	py|go|rs|ml)          lang="$1";      shift ;;
	-d)                   debug=yes;      shift ;;
	-e)                   example=yes;    shift ;;
	-E)                   example=yes;    shift; exid="$1"; shift ;;
	*)                    echo "$usage";  exit 1 ;;
esac done
if [ -z "$year" ] || [ -z "$day" ] || [ -z "$lang" ]; then echo "$usage"; exit 1; fi

# Ensure current directory is project's root to allow using the cli from anywhere
cd "$(dirname "$(dirname "$0")")"

oday="$(printf %02d "$day")"

if [ -z $example ]; then path_in="inputs/year_${year}/day_${oday}.txt"
elif [ -z $exid ]; then path_in="inputs/year_${year}/day_${oday}_example.txt"
else                     path_in="inputs/year_${year}/day_${oday}_example_$exid.txt"
fi

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                      EXECUTE SOLUTION                       ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

echo > debug.log

if [ "$lang" == "py" ]; then

	py_module="py.year_${year}.day_${oday}"

	if [ -n "$debug" ]; then
		echo PYTHONPATH=./src python -m "$py_module" "<" "$path_in" "2>" debug.log
		PYTHONPATH=./src python -m "$py_module" < "$path_in" 2> debug.log
	else
		echo PYTHONPATH=./src python -O -m "$py_module" "<" "$path_in"
		PYTHONPATH=./src python -O -m "$py_module" < "$path_in"
	fi

elif [ "$lang" == "go" ]; then

	if [ -n "$debug" ]; then
		echo go run ./src/go "$year" "$day" "<" "$path_in" "2>" debug.log
		go run ./src/go "$year" "$day" < "$path_in" 2> debug.log
	else
		echo go build -o src/go/aoc -ldflags "-s" ./src/go "&&" src/go/aoc "$year" "$day" "<" "$path_in"
		go build -o src/go/aoc -ldflags "-s" ./src/go && src/go/aoc "$year" "$day" < "$path_in"
	fi

elif [ "$lang" == "rs" ]; then

	args="--manifest-path src/rs/Cargo.toml --bin ${year}_${oday}"
	if [ -n "$debug" ]; then
		echo cargo run $args "<" "$path_in" "2>" debug.log
		cargo run $args < "$path_in" 2> debug.log
	else
		echo cargo run $args --release "<" "$path_in"
		cargo run $args --release < "$path_in"
	fi

elif [ "$lang" == "ml" ]; then

	# TODO: add debug mode later...

	echo dune --root src/ml exec year_${year}/day_${oday}.exe "<" "$path_in"
	dune exec --root src/ml year_${year}/day_${oday}.exe < "$path_in"

fi

max_err_lines=20
if [ -n "$(<debug.log)" ]; then
	echo -e "\033[1;31m"
	if [ "$(wc -l < debug.log)" -le "$max_err_lines" ]; then
		cat debug.log
	else
		echo "Stderr output is more than $max_err_lines lines long. See ./debug.log."
	fi
	echo -e "\033[0m"
fi
