use std::io::{self, Read};

fn count_total_volume<F: Fn(&str) -> (i64, i64, i64)>(data: &String, decode_line: F) -> i64 {
    let (mut total, mut x, mut y) = (0, 0, 0);

    for line in data.trim().split("\n") {
        let (dx, dy, length) = decode_line(line);
        let nx = x + dx * length;
        let ny = y + dy * length;
        total += x * ny - nx * y + length; // Gauss shoelace formula + length for perimeter
        (x, y) = (nx, ny);
    }

    return total / 2 + 1;
}

fn dir_to_vec2(d: u8) -> (i64, i64) {
    match d {
        b'U' => (0, -1),
        b'D' => (0, 1),
        b'L' => (-1, 0),
        b'R' => (1, 0),
        _ => unreachable!(),
    }
}

fn decode_dir(d: u8) -> u8 {
    "RDLU".as_bytes()[(d - b'0') as usize] // d is 0 | 1 | 2 | 3
}

fn solve_1(data: &String) -> i64 {
    count_total_volume(data, |line: &str| {
        let d = line.as_bytes()[0];
        let (dx, dy) = dir_to_vec2(d);

        let (l1, l2) = (2, line.len() - 10);
        let l = line[l1..l2].parse().unwrap();
        (dx, dy, l)
    })
}

fn solve_2(data: &String) -> i64 {
    count_total_volume(data, |line: &str| {
        let d = decode_dir(line.as_bytes()[line.len() - 2]);
        let (dx, dy) = dir_to_vec2(d);

        let (l1, l2) = (line.len() - 7, line.len() - 2);
        let l = i64::from_str_radix(&line[l1..l2], 16).unwrap();
        (dx, dy, l)
    })
}

fn main() {
    let mut data = String::new();
    io::stdin().read_to_string(&mut data).expect("no stdin");
    println!("{}\n{}", solve_1(&data), solve_2(&data));
}
