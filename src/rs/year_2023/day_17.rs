use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashSet},
    io::{self, Read},
    ops::Add,
};

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct Vec2(i32, i32);

impl Vec2 {
    fn turn1(&self) -> Vec2 {
        Vec2(-self.1, -self.0)
    }
    fn turn2(&self) -> Vec2 {
        Vec2(self.1, self.0)
    }
}

impl Add for Vec2 {
    type Output = Vec2;

    fn add(self, rhs: Self) -> Self {
        Self(self.0 + rhs.0, self.1 + rhs.1)
    }
}

#[derive(PartialEq, Eq, Hash)]
struct State {
    pos: Vec2,
    d: Vec2,
    streak: i32,
}

#[derive(PartialEq, Eq)]
struct HeapItem {
    hl: i32,
    streak: i32,
    pos: Vec2,
    d: Vec2,
}

impl PartialOrd for HeapItem {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Reverse(self.hl).partial_cmp(&Reverse(other.hl))
    }
}

impl Ord for HeapItem {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        Reverse(self.hl).cmp(&Reverse(other.hl))
    }
}

fn cost_to_target(data: &String, min_streak: i32, max_streak: i32) -> i32 {
    let width = data.find('\n').unwrap() as i32;
    let height = data.bytes().filter(|&b| b == b'\n').count() as i32;
    let target = Vec2(width - 1, height - 1);

    let mut seen = HashSet::new();
    let mut min_pq = BinaryHeap::new();

    min_pq.push(HeapItem {
        hl: 0,
        streak: 0,
        pos: Vec2(0, 0),
        d: Vec2(1, 0), // Right
    });

    while let Some(HeapItem { hl, streak, pos, d }) = min_pq.pop() {
        // found minimum possible heat loss
        if streak >= min_streak && pos == target {
            return hl;
        }

        let state = State { pos, d, streak };
        if !seen.contains(&state) {
            seen.insert(state);

            let mut explore = |d: Vec2, streak: i32| {
                let pos = pos + d;
                let in_bound = pos.0 >= 0 && pos.1 >= 0 && pos.0 < width && pos.1 < height;
                if in_bound {
                    let offset = (pos.1 * (width + 1) + pos.0) as usize;
                    let heat_loss = (data.as_bytes()[offset] - b'0') as i32;
                    let hl = hl + heat_loss;
                    min_pq.push(HeapItem { hl, streak, pos, d });
                }
            };

            // straight ahead
            if streak < max_streak {
                explore(d, streak + 1);
            }

            // left and right
            if streak >= min_streak {
                explore(d.turn1(), 1);
                explore(d.turn2(), 1);
            }
        }
    }
    return 0;
}

fn solve_1(data: &String) -> i32 {
    cost_to_target(data, 0, 3)
}

fn solve_2(data: &String) -> i32 {
    cost_to_target(data, 4, 10)
}

fn main() {
    let mut data = String::new();
    io::stdin().read_to_string(&mut data).expect("no stdin");
    println!("{}\n{}", solve_1(&data), solve_2(&data));
}
