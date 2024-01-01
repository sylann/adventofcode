use std::io::{self, Read};

macro_rules! iter_lines {
    ($data:ident) => {
        $data
            .trim()
            .split('\n')
            .map(|line| line.split(' ').flat_map(str::parse).collect::<Vec<i32>>())
    };
}

fn compute_deltas(nums: &Vec<i32>) -> Vec<i32> {
    assert!(nums.len() >= 2, "no delta for N<2");
    (1..nums.len()).map(|i| nums[i] - nums[i - 1]).collect()
}

enum Fold {
    Left,
    Right,
}

fn extrapolate(nums: &Vec<i32>, fold: Fold) -> i32 {
    let deltas = compute_deltas(nums);
    let (prev, sign) = match fold {
        Fold::Right => (*nums.last().unwrap_or(&0), 1),
        Fold::Left => (*nums.first().unwrap_or(&0), -1),
    };
    match deltas.iter().all(|&n| n == 0) {
        true => prev,
        false => prev + sign * extrapolate(&deltas, fold),
    }
}

fn solve_1(data: &String) -> i32 {
    iter_lines!(data).fold(0, |t, nums| t + extrapolate(&nums, Fold::Right))
}

fn solve_2(data: &String) -> i32 {
    iter_lines!(data).fold(0, |t, nums| t + extrapolate(&nums, Fold::Left))
}

fn main() {
    let mut data = String::new();
    io::stdin().read_to_string(&mut data).expect("no stdin");
    println!("{}\n{}", solve_1(&data), solve_2(&data));
}
