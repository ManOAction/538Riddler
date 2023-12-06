use std::collections::HashSet;
use std::fs;

fn find_priority_of_bag(backpack: &str) -> i32 {
    dbg!(backpack);

    let character_count = backpack.chars().count();
    let mut chars_seen = HashSet::new();
    let mut priority = 0;
    let compartment_a = &backpack[..(character_count / 2)];
    let compartment_b = &backpack[(character_count / 2)..];

    dbg!(character_count);
    dbg!(compartment_a);
    dbg!(compartment_b);

    // Insert each character of the first string into the set.
    for ch in compartment_a.chars() {
        chars_seen.insert(ch);
    }

    // Check if any character in the second string is already in the set.
    for ch in compartment_b.chars() {
        if chars_seen.contains(&ch) {
            if ch as u8 >= 97 && ch as u8 <= 122 {
                priority = ch as u8 - 96;
            }
            if ch as u8 >= 65 && ch as u8 <= 90 {
                priority = ch as u8 - 38;
            }
            println!("The priority of {} is {}", ch, priority);

            return priority.into();
        }
        dbg!(ch);
    }

    return 0;
}

fn main() {
    let puzzle_input = fs::read_to_string("PuzzleInput.txt").expect("Failed to read the file");

    let mut total_priority = 0;

    for row in puzzle_input.lines() {
        total_priority += find_priority_of_bag(&row);
    }

    dbg!(total_priority);

    // let Char1 = 'a';
    // let Char2 = 'b';
    // let Char3 = 'c';

    // let Char4 = 'A';
    // let Char5 = 'B';
    // let Char6 = 'C';

    // println!("The UTF-8 code unit for '{}' is {}", Char1, Char1 as u8);
    // println!("The UTF-8 code unit for '{}' is {}", Char2, Char2 as u8);
    // println!("The UTF-8 code unit for '{}' is {}", Char3, Char3 as u8);
    // println!("The UTF-8 code unit for '{}' is {}", Char4, Char4 as u8);
    // println!("The UTF-8 code unit for '{}' is {}", Char5, Char5 as u8);
    // println!("The UTF-8 code unit for '{}' is {}", Char6, Char6 as u8);

    // It looks like a-z is 97-122 and A-Z is 65-90
}
