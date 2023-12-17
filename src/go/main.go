package main

import (
	"fmt"
	"io"
	"os"
	"strconv"

	"github.com/sylann/adventofcode/year_2022"
	"github.com/sylann/adventofcode/year_2023"
)

func main() {
	year, day := parseArgs()
	sol := getSolution(year, day)
	data := readDataFromStdin()
	fmt.Printf("[PART 1]\n%s\n", sol.Solve1(data))
	fmt.Printf("[PART 2]\n%s\n", sol.Solve2(data))
}

type Solution interface {
	Solve1(data string) string
	Solve2(data string) string
}

func getSolution(year, day int) Solution {
	var sol Solution
	switch year {
	case 2022:
		sol = year_2022.Solutions[day-1]
	case 2023:
		sol = year_2023.Solutions[day-1]
	}

	if sol == nil {
		fmt.Printf("No solution found for day %d of year %d\n", day, year)
		os.Exit(1)
	}

	return sol
}

func parseArgs() (year, day int) {
	if len(os.Args) < 3 {
		fmt.Printf("Usage: %s YEAR DAY\n", os.Args[0])
		os.Exit(1)
	}

	year, _ = strconv.Atoi(os.Args[1])
	if year == 0 {
		fmt.Printf("Invalid args: YEAR must be a number\n")
		os.Exit(1)
	}

	day, _ = strconv.Atoi(os.Args[2])
	if day < 1 || day > 24 {
		fmt.Printf("Invalid args: DAY must be a number between 1 and 24 included\n")
		os.Exit(1)
	}

	return year, day
}

func readDataFromStdin() string {
	stat, _ := os.Stdin.Stat()
	isRepl := stat == nil || (stat.Mode()&os.ModeCharDevice) != 0
	if isRepl {
		fmt.Printf("Waiting for input\n(Press CTRL+D on an empty line to validate)\n")
	}

	bytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Printf("Could not read from stdin\n")
		os.Exit(1)
	}

	data := string(bytes)
	if data == "" {
		fmt.Printf("Received nothing from stdin\n")
		os.Exit(1)
	}

	return data
}
