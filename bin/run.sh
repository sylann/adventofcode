# #!/usr/bin/env bash
usage="
USAGE: $0 YEAR DAY LANG [-d] [-e] [-E NAME]

    YEAR       a number between 2010 and 2030  (we'll see if this code survives that long)
    DAY        a number between 1 and 24
    LANG       one of the supported languages: py, go
    -d         enable debug / disable optimization
    -e         use example instead of user input
    -E NAME    use specific example with given NAME
"
while [[ $# -gt 0 ]]; do case $1 in
	20[1-3][0-9])         year="$1";      shift ;;
	[1-9]|1[0-9]|2[0-4])  day="$1";       shift ;;
	py|go)                lang="$1";      shift ;;
	-d)                   debug=yes;      shift ;;
	-e)                   example=yes;    shift ;;
	-E)                   example=yes;    shift; exid="$1"; shift ;;
	*)                    echo "$usage";  exit 1 ;;
esac done
if [ -z "$year" ] || [ -z "$day" ] || [ -z "$lang" ]; then echo "$usage"; exit 1; fi

oday="$(printf %02d "$day")"

if [ -z $example ]; then path_in="inputs/year_${year}/day_${oday}.txt"
elif [ -z $exid ]; then path_in="inputs/year_${year}/day_${oday}_example.txt"
else                     path_in="inputs/year_${year}/day_${oday}_example_$exid.txt"
fi

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                      EXECUTE SOLUTION                       ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

if [ "$lang" == "py" ]; then

	path_code="src/py/year_${year}/day_${oday}.py"

	if [ -n "$debug" ]; then
		echo python "$path_code" "<" "$path_in" "2>" debug.log
		python "$path_code" < "$path_in" 2> debug.log
	else
		echo python -O "$path_code" "<" "$path_in"
		python -O "$path_code" < "$path_in"
	fi

elif [ "$lang" == "go" ]; then

	if [ -n "$debug" ]; then
		echo go run ./src/go "$year" "$day" "<" "$path_in" "2>" debug.log
		go run ./src/go "$year" "$day" < "$path_in" 2> debug.log
	else
		echo go build -o src/go/aoc -ldflags "-s" ./src/go "&&" src/go/aoc "$year" "$day" "<" "$path_in"
		go build -o src/go/aoc -ldflags "-s" ./src/go && src/go/aoc "$year" "$day" < "$path_in"
	fi

fi
