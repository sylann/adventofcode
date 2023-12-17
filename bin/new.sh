# #!/usr/bin/env bash
usage="
USAGE: $0 YEAR DAY LANG [--get]

    YEAR     a number between 2010 and 2030  (we'll see if this code survives that long)
    DAY      a number between 1 and 24
    LANG     one of the supported languages: py, go
    --get    download user specific input from adventofcode.com
"
while [[ $# -gt 0 ]]; do case $1 in
	20[1-3][0-9])         year="$1";      shift ;;
	[1-9]|1[0-9]|2[0-4])  day="$1";       shift ;;
	py|go)                lang="$1";      shift ;;
	--get)                get=yes;        shift ;;
	*)                    echo "$usage";  exit 1 ;;
esac done
if [ -z "$year" ] || [ -z "$day" ] || [ -z "$lang" ]; then echo "$usage"; exit 1; fi

oday="$(printf %02d "$day")"

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                     PREPARE INPUT FILES                     ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

path_in_year="inputs/year_${year}"
path_in_user="inputs/year_${year}/day_${oday}.txt"
path_in_example="inputs/year_${year}/day_${oday}_example.txt"

if ! [ -d "$path_in_year" ]; then mkdir -p "$path_in_year"; fi
if ! [ -f "$path_in_example" ]; then touch "$path_in_example"; fi
if ! [ -f "$path_in_user" ]; then
	if [ -n "$get" ]; then
		url="https://adventofcode.com/$year/day/$day/input"
		cookie=$(< .cookie)

		echo "[INFO] Retrieving input from $url"
		curl "$url" -H "Cookie: $cookie" -o "$path_in_user" --progress-bar
	else
		touch "$path_in_user"
	fi
fi

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                     PREPARE CODE FILES                      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

feed_template() {
	sed -e "s/__year__/$year/g" -e "s/__day__/$oday/g" "$1"
}

if [ "$lang" = "py" ]; then

	path_year="python/year_${year}"
	path_day="python/year_${year}/day_${oday}.py"
	path_tmpl_day="python/template_day"

	if ! [ -d "$path_year" ]; then mkdir -p "$path_year"; fi
	if ! [ -f "$path_day" ]; then feed_template "$path_tmpl_day" > "$path_day"; fi

elif [ "$lang" = "go" ]; then

	path_year="golang/year_${year}"
	path_day="golang/year_${year}/day_${oday}.go"
	path_tmpl_day="golang/template_day"
	path_base="golang/year_${year}/base.go"
	path_tmpl_base="golang/template_base"

	if ! [ -d "$path_year" ]; then mkdir -p "$path_year"; fi
	if ! [ -f "$path_day" ]; then feed_template "$path_tmpl_day" > "$path_day"; fi
	if ! [ -f "$path_base" ]; then feed_template "$path_tmpl_base" > "$path_base"; fi
	sed -e "s/nil, \/\/ Day$oday{},/Day$oday{},/" -i '' "$path_base"

fi
