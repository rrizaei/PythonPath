"""
Dice Rolling Game - Interactive Dice Simulation

A comprehensive dice rolling game that simulates various dice types with
statistics tracking, multiple dice support, and betting mechanics.

WHAT IT DOES:
- Rolls various dice types (D4, D6, D8, D10, D12, D20, D100)
- Supports rolling multiple dice at once
- Tracks roll history and statistics
- Includes betting/casino mode
- Provides probability analysis
- Shows dice visualization (ASCII)
- Supports custom dice (any number of sides)

USE CASES:
- Tabletop RPG companion (D&D, Pathfinder)
- Probability learning tool
- Casino game simulation
- Random number generation practice
- Game night entertainment

KEY FEATURES:
- Multiple dice types (4, 6, 8, 10, 12, 20, 100 sides)
- Roll any number of dice simultaneously
- Keep highest/lowest dice (advantage/disadvantage)
- Betting mode with starting chips
- Roll history with timestamps
- Statistical analysis (average, min, max, distribution)
- ASCII art dice visualization
- Custom dice creation
- Probability calculator

REQUIREMENTS: Python 3.6+ (random module, datetime)
"""

import random
from datetime import datetime
from collections import Counter
from typing import List, Dict, Tuple

class DiceGame:
    def __init__(self):
        """Initialize the dice game"""
        self.roll_history = []
        self.dice_types = {
            'd4': 4,
            'd6': 6,
            'd8': 8,
            'd10': 10,
            'd12': 12,
            'd20': 20,
            'd100': 100
        }

    def roll_dice(self, sides: int, num_dice: int = 1, advantage: int = 0) -> Tuple[List[int], List[int]]:
        """
        Roll dice with optional advantage/disadvantage

        Args:
            sides: Number of sides on the die
            num_dice: Number of dice to roll
            advantage: 0=normal, 1=advantage (roll extra, keep highest),
                      -1=disadvantage (roll extra, keep lowest)

        Returns:
            Tuple of (all_rolls, final_rolls)
        """
        if advantage == 0:
            # Normal roll
            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            return rolls, rolls
        else:
            # Advantage/Disadvantage: roll double the dice
            rolls = [random.randint(1, sides) for _ in range(num_dice * 2)]

            if advantage > 0:
                # Keep highest num_dice rolls
                final_rolls = sorted(rolls, reverse=True)[:num_dice]
            else:
                # Keep lowest num_dice rolls
                final_rolls = sorted(rolls)[:num_dice]

            return rolls, final_rolls

    def display_dice_ascii(self, roll: int, sides: int):
        """Display ASCII art of dice"""
        dice_art = {
            1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
            2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
            3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
            4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
            5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
            6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
        }

        # For d20 or d100, show number instead of ASCII
        if sides > 6 or roll > 6:
            print(f"  ┌─────┐")
            print(f"  │     │")
            print(f"  │  {roll:2d}  │")
            print(f"  │     │")
            print(f"  └─────┘")
        else:
            art = dice_art.get(roll, dice_art[1])
            for line in art:
                print(f"  {line}")

    def roll_dice_with_display(self, dice_type: str, num_dice: int = 1, show_ascii: bool = False):
        """Roll dice and display results"""
        if dice_type not in self.dice_types:
            print(f"Invalid dice type. Choose from: {', '.join(self.dice_types.keys())}")
            return None

        sides = self.dice_types[dice_type]

        # Ask about advantage/disadvantage
        adv_choice = input("Advantage/Disadvantage? (normal/advantage/disadvantage): ").lower()
        if adv_choice == 'advantage':
            advantage = 1
        elif adv_choice == 'disadvantage':
            advantage = -1
        else:
            advantage = 0

        # Roll the dice
        all_rolls, final_rolls = self.roll_dice(sides, num_dice, advantage)

        # Record in history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        roll_record = {
            'timestamp': timestamp,
            'dice_type': dice_type,
            'sides': sides,
            'num_dice': num_dice,
            'all_rolls': all_rolls,
            'final_rolls': final_rolls,
            'total': sum(final_rolls),
            'advantage': advantage
        }
        self.roll_history.append(roll_record)

        # Display results
        print("\n" + "="*50)
        print(f"ROLLING {num_dice}{dice_type.upper()}...")
        if advantage != 0:
            print(f"Mode: {advantage_choice.capitalize()}")
        print("="*50)

        # Show all rolls if advantage/disadvantage
        if advantage != 0 and num_dice == 1:
            print(f"Rolled: {all_rolls}")
            print(f"Kept: {final_rolls[0]} (highest)" if advantage > 0 else f"Kept: {final_rolls[0]} (lowest)")
        else:
            print(f"Results: {final_rolls}")

        # Show individual dice ASCII
        if show_ascii and num_dice <= 6:  # Limit to 6 dice for display
            print("\nDice Visualization:")
            for i, roll in enumerate(final_rolls, 1):
                print(f"\nDie {i}:")
                self.display_dice_ascii(roll, sides)
        elif show_ascii and num_dice > 6:
            print(f"\n(Too many dice to display ASCII for all {num_dice})")

        print(f"\nTOTAL: {sum(final_rolls)}")
        print("="*50)

        return final_rolls

    def show_statistics(self):
        """Display rolling statistics"""
        if not self.roll_history:
            print("No rolls recorded yet")
            return

        print("\n" + "="*60)
        print("DICE ROLLING STATISTICS")
        print("="*60)

        total_rolls = len(self.roll_history)
        total_dice_rolled = sum(record['num_dice'] for record in self.roll_history)
        all_numbers = []

        for record in self.roll_history:
            all_numbers.extend(record['final_rolls'])

        if all_numbers:
            print(f"Total Sessions: {total_rolls}")
            print(f"Total Dice Rolled: {total_dice_rolled}")
            print(f"Average Roll: {sum(all_numbers)/len(all_numbers):.2f}")
            print(f"Highest Roll: {max(all_numbers)}")
            print(f"Lowest Roll: {min(all_numbers)}")

            # Most common rolls
            counter = Counter(all_numbers)
            print("\nMost Common Rolls:")
            for number, count in counter.most_common(5):
                percentage = (count / len(all_numbers)) * 100
                print(f"  {number}: {count} times ({percentage:.1f}%)")

            # Distribution by dice type
            print("\nRolls by Dice Type:")
            dice_stats = {}
            for record in self.roll_history:
                dice_key = record['dice_type']
                if dice_key not in dice_stats:
                    dice_stats[dice_key] = {'count': 0, 'rolls': []}
                dice_stats[dice_key]['count'] += 1
                dice_stats[dice_key]['rolls'].extend(record['final_rolls'])

            for dice_type, stats in dice_stats.items():
                avg = sum(stats['rolls']) / len(stats['rolls']) if stats['rolls'] else 0
                print(f"  {dice_type.upper()}: {stats['count']} rolls, Avg: {avg:.2f}")

        print("="*60)

    def show_history(self, limit: int = 10):
        """Show recent roll history"""
        if not self.roll_history:
            print("No rolls recorded yet")
            return

        print("\n" + "="*60)
        print(f"RECENT ROLL HISTORY (Last {min(limit, len(self.roll_history))})")
        print("="*60)

        for record in self.roll_history[-limit:]:
            adv_text = ""
            if record['advantage'] > 0:
                adv_text = " [Advantage]"
            elif record['advantage'] < 0:
                adv_text = " [Disadvantage]"

            print(f"{record['timestamp']} - {record['num_dice']}{record['dice_type'].upper()}{adv_text}: "
                  f"{record['final_rolls']} = Total: {record['total']}")

        print("="*60)

    def probability_calculator(self):
        """Calculate probability of specific outcomes"""
        print("\n" + "="*60)
        print("PROBABILITY CALCULATOR")
        print("="*60)

        dice_type = input("Dice type (d6, d20, etc.): ").lower()
        if dice_type not in self.dice_types:
            print(f"Invalid dice type. Use: {', '.join(self.dice_types.keys())}")
            return

        sides = self.dice_types[dice_type]
        num_dice = int(input("Number of dice: "))
        target = int(input("Target number (sum or individual die): "))
        target_type = input("Target type (sum, exactly, at_least, at_most): ").lower()

        # Simulate probabilities
        simulations = 10000
        successes = 0
        results = []

        for _ in range(simulations):
            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            roll_sum = sum(rolls)

            if target_type == 'sum':
                if roll_sum == target:
                    successes += 1
            elif target_type == 'exactly':
                if all(r == target for r in rolls):
                    successes += 1
            elif target_type == 'at_least':
                if roll_sum >= target:
                    successes += 1
            elif target_type == 'at_most':
                if roll_sum <= target:
                    successes += 1

            results.append(roll_sum if target_type != 'exactly' else max(rolls))

        probability = (successes / simulations) * 100
        print(f"\nProbability: {probability:.2f}%")
        print(f"Based on {simulations} simulations")

        # Show distribution
        counter = Counter(results[:100])  # First 100 for distribution
        print("\nSample distribution (first 100 rolls):")
        for value, count in sorted(counter.items())[:10]:
            bar = "#" * (count // 2)
            print(f"  {value:3d}: {bar} ({count})")

    def betting_mode(self, starting_chips: int = 100):
        """Casino-style betting mode"""
        chips = starting_chips

        print("\n" + "="*60)
        print("BETTING MODE - CASINO DICE")
        print("="*60)
        print(f"Starting chips: {chips}")
        print("Bet on dice rolls to win chips!")
        print("="*60)

        while chips > 0:
            print(f"\nYour chips: {chips}")
            print("\nBetting options:")
            print("  1. Bet on specific number (pays 5x)")
            print("  2. Bet on odd/even (pays 2x)")
            print("  3. Bet on high/low (pays 2x)")
            print("  4. Exit betting mode")

            choice = input("\nYour choice: ").strip()

            if choice == '4':
                print(f"\nLeaving with {chips} chips")
                break

            try:
                bet = int(input("Place your bet (chips): "))
                if bet > chips:
                    print("You don't have enough chips!")
                    continue
                if bet <= 0:
                    print("Bet must be positive")
                    continue
            except ValueError:
                print("Invalid bet amount")
                continue

            # Roll the dice
            dice_type = input("Dice to roll (d6/d20): ").lower()
            if dice_type not in self.dice_types:
                print("Invalid dice type, using d6")
                dice_type = 'd6'

            sides = self.dice_types[dice_type]
            roll = random.randint(1, sides)

            print(f"\nRolling {dice_type.upper()}... Result: {roll}")
            self.display_dice_ascii(roll, sides)

            # Handle bet types
            won = False
            multiplier = 1

            if choice == '1':
                number = int(input("Bet on which number? "))
                if roll == number:
                    won = True
                    multiplier = 5
                    print(f"Lucky number! You win!")
                else:
                    print(f"Number {number} didn't hit")

            elif choice == '2':
                parity = input("Bet on (odd/even): ").lower()
                if (parity == 'odd' and roll % 2 == 1) or (parity == 'even' and roll % 2 == 0):
                    won = True
                    multiplier = 2
                    print(f"The roll is {parity}! You win!")
                else:
                    print(f"The roll is {'odd' if roll % 2 else 'even'}, not {parity}")

            elif choice == '3':
                high_low = input("Bet on (high/low) [high=above half]: ").lower()
                is_high = roll > (sides // 2)
                if (high_low == 'high' and is_high) or (high_low == 'low' and not is_high):
                    won = True
                    multiplier = 2
                    print(f"The roll is {high_low}! You win!")
                else:
                    print(f"The roll is {'high' if is_high else 'low'}, not {high_low}")

            if won:
                winnings = bet * multiplier
                chips += winnings
                print(f"You won {winnings} chips!")
            else:
                chips -= bet
                print(f"You lost {bet} chips")

        if chips <= 0:
            print("\nYou're out of chips! Game over!")
        else:
            print(f"\nYou ended with {chips} chips")

def main():
    """Main program loop"""
    game = DiceGame()

    print("\n" + "="*60)
    print("DICE ROLLING GAME")
    print("="*60)
    print("Available dice: D4, D6, D8, D10, D12, D20, D100")
    print("="*60)

    while True:
        print("\n" + "-"*50)
        print("OPTIONS:")
        print("  1. Roll dice")
        print("  2. Roll with advantage/disadvantage")
        print("  3. Show statistics")
        print("  4. Show roll history")
        print("  5. Probability calculator")
        print("  6. Betting mode (casino)")
        print("  7. Custom dice roll")
        print("  8. Exit")

        choice = input("\nYour choice (1-8): ").strip()

        if choice == '1':
            print("\nDice types: d4, d6, d8, d10, d12, d20, d100")
            dice_type = input("Enter dice type: ").lower()
            if dice_type not in game.dice_types:
                print("Invalid dice type")
                continue

            try:
                num_dice = int(input("Number of dice (1-10): "))
                num_dice = max(1, min(10, num_dice))
            except ValueError:
                num_dice = 1

            show_ascii = input("Show ASCII dice art? (yes/no): ").lower() == 'yes'
            game.roll_dice_with_display(dice_type, num_dice, show_ascii)

        elif choice == '2':
            print("\nDice types: d4, d6, d8, d10, d12, d20, d100")
            dice_type = input("Enter dice type: ").lower()
            if dice_type not in game.dice_types:
                print("Invalid dice type")
                continue

            num_dice = 1
            adv = input("Advantage or disadvantage? (a/d): ").lower()
            advantage = 1 if adv == 'a' else -1

            sides = game.dice_types[dice_type]
            all_rolls, final_rolls = game.roll_dice(sides, num_dice, advantage)

            print(f"\nRolled: {all_rolls}")
            print(f"Kept: {final_rolls[0]} ({'highest' if advantage > 0 else 'lowest'})")
            print(f"Total: {sum(final_rolls)}")

        elif choice == '3':
            game.show_statistics()

        elif choice == '4':
            limit = input("How many rolls to show? (default 10): ").strip()
            try:
                limit = int(limit)
            except ValueError:
                limit = 10
            game.show_history(limit)

        elif choice == '5':
            game.probability_calculator()

        elif choice == '6':
            try:
                chips = int(input("Starting chips (default 100): ") or 100)
            except ValueError:
                chips = 100
            game.betting_mode(chips)

        elif choice == '7':
            try:
                sides = int(input("Number of sides on custom die: "))
                num_dice = int(input("Number of dice: "))
                rolls = [random.randint(1, sides) for _ in range(num_dice)]
                print(f"\nResults: {rolls}")
                print(f"Total: {sum(rolls)}")
            except ValueError:
                print("Invalid input")

        elif choice == '8':
            print("\nThank you for playing!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()