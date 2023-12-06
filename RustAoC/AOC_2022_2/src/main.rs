use std::fs;

fn calculate_strategy_one(puzzle_input: &str) -> i32 {
    let mut total = 0;

    let mut contest_results = Vec::new();

    contest_results.push(("A X", 4)); // Rock v Rock = Draw 3 + 1
    contest_results.push(("A Y", 8)); // Rock v Paper = Win 6 + 2
    contest_results.push(("A Z", 3)); // Rock v Scissors = Loss 0 + 3
    contest_results.push(("B X", 1)); // Paper v Rock = Lose 0 + 1
    contest_results.push(("B Y", 5)); // Paper v Paper = Draw 3 + 2
    contest_results.push(("B Z", 9)); // Paper v Scissors = Win 6 + 3
    contest_results.push(("C X", 7)); // Scissors v Rock = Win 6 + 1
    contest_results.push(("C Y", 2)); // Scissors v Paper = Lose 0 + 2
    contest_results.push(("C Z", 6)); // Scissors v Scissors = Draw 3 + 3

    for row in puzzle_input.lines() {
        for (contest, result) in &contest_results {
            if row == *contest {
                total += result;
            }
        }
    }

    return total;
}

fn calculate_strategy_two(puzzle_input: &str) -> i32 {
    let mut total = 0;

    let mut contest_results = Vec::new();

    contest_results.push(("A X", 3)); // Lose vs Rock = Scissors 0 + 3
    contest_results.push(("A Y", 4)); // Draw vs Rock = Rock 3 + 1
    contest_results.push(("A Z", 8)); // Win vs Rock = Paper 6 + 2
    contest_results.push(("B X", 1)); // Lose vs Paper = Rock 0 + 1
    contest_results.push(("B Y", 5)); // Draw vs Paper = Paper 3 + 2
    contest_results.push(("B Z", 9)); // Win vs Paper = Scissors 6 + 3
    contest_results.push(("C X", 2)); // Lose vs Scissors = Paper 0 + 2
    contest_results.push(("C Y", 6)); // Draw vs Scissors  = Scissors 3 + 3
    contest_results.push(("C Z", 7)); // Win vs Scissors = Rock 6 + 1

    for row in puzzle_input.lines() {
        for (contest, result) in &contest_results {
            if row == *contest {
                total += result;
            }
        }
    }

    return total;
}

fn main() {
    let puzzle_input = fs::read_to_string("PuzzleInput.txt").expect("Failed to read the file");

    let strategy_one_score = calculate_strategy_one(&puzzle_input);

    println!("Strategy one score: {}", strategy_one_score);

    let strategy_two_score = calculate_strategy_two(&puzzle_input);

    println!("Strategy two score: {}", strategy_two_score);
}
