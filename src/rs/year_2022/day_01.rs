use std::collections::BinaryHeap;
use std::io::{self, Read};

fn sum_calories_of_n_best(data: &String, n: usize) -> Result<u32, &str> {
    let mut max_heap: BinaryHeap<u32> = BinaryHeap::new();

    for elf in data.trim().split("\n\n") {
        let elf_calories = elf.split("\n").filter_map(|x| x.parse::<u32>().ok()).sum();
        max_heap.push(elf_calories)
    }

    let mut out = 0;
    for _ in 0..n {
        out += max_heap.pop().ok_or("Expected n ≤ number of elves")?;
    }

    Ok(out)
}

fn solve_1(data: &String) -> u32 {
    sum_calories_of_n_best(data, 1).unwrap()
}

fn solve_2(data: &String) -> u32 {
    sum_calories_of_n_best(data, 3).unwrap()
}

fn main() {
    let mut data = String::new();
    io::stdin().read_to_string(&mut data).expect("no stdin");
    println!("{}\n{}", solve_1(&data), solve_2(&data));
}
