use std::fs;

fn calculate_backpacks(puzzle_input: &str) -> Vec<(i32, i32)> {
    let mut backpacks = Vec::new();
    let mut pack_number = 1;
    let mut pack_value = 0;

    for row in puzzle_input.lines() {
        if !row.trim().is_empty() {
            pack_value += row.trim().parse::<i32>().expect("Failed to parse integer");
        } else {
            backpacks.push((pack_number, pack_value));
            pack_value = 0;
            pack_number += 1;
        }
    }

    if pack_value != 0 {
        backpacks.push((pack_number, pack_value));
    }

    return backpacks;
}

fn main() {
    let puzzle_input = fs::read_to_string("PuzzleInput.txt").expect("Failed to read the file");

    println!("{}", puzzle_input);

    let mut backpacks = calculate_backpacks(&puzzle_input);

    let total_calories: i32 = backpacks.iter().map(|(_, y)| y).sum();
    println!("Total calories: {}", total_calories);

    backpacks.sort_by(|a, b| b.1.cmp(&a.1));

    println!("{:?}", backpacks);

    println!(
        "Highest calorie backpack: {:?}",
        backpacks.first().unwrap().1
    );

    let sum_of_top_three: i32 = backpacks.iter().take(3).map(|(_, y)| y).sum();

    println!(
        "Sum of second values of the top three: {}",
        sum_of_top_three
    );
}
