use std::io::{self, Read};

const DIGIT_NAMES: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn first_num<I, F>(line: &str, it: I, is_digit_name: F) -> u32
where
    I: Iterator<Item = usize>,
    F: Fn(usize, &str) -> bool,
{
    for i in it {
        if let Some(n) = line.chars().nth(i).and_then(|c| c.to_digit(10)) {
            return n;
        }
        for di in 0..DIGIT_NAMES.len() {
            if is_digit_name(i, DIGIT_NAMES[di]) {
                return di as u32 + 1;
            }
        }
    }
    unreachable!()
}

fn solve_1(data: &String) -> u32 {
    let mut total = 0;
    for line in data.trim().split('\n') {
        let first = line.chars().find_map(|c| c.to_digit(10)).unwrap_or(0);
        let last = line.chars().rev().find_map(|c| c.to_digit(10)).unwrap_or(0);
        total += first * 10 + last;
    }
    return total;
}

fn solve_2(data: &String) -> u32 {
    let mut total = 0;
    for line in data.trim().split('\n') {
        let first = first_num(line, 0..line.len(), |i, n| line[i..].starts_with(n));
        let last = first_num(line, (0..line.len()).rev(), |i, n| line[..=i].ends_with(n));
        total += first * 10 + last;
    }
    return total;
}

fn main() {
    let mut data = String::new();
    io::stdin().read_to_string(&mut data).expect("no stdin");
    println!("{}\n{}", solve_1(&data), solve_2(&data));
}
