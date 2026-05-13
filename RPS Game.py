"""
Rock Paper Scissors - Classic Hand Game

A simple command-line implementation of Rock Paper Scissors where you play against the computer.
The computer makes random choices, and the game follows traditional rules.

WHAT IT DOES:
- Player chooses rock, paper, or scissors
- Computer randomly selects its choice
- Determines winner based on classic rules:
  * Rock crushes Scissors
  * Scissors cuts Paper
  * Paper covers Rock
- Tracks game statistics (wins, losses, ties)
- Allows multiple rounds until player quits

HOW TO PLAY:
Run the script and enter your choice when prompted:
- 'r' or 'rock' for Rock
- 'p' or 'paper' for Paper
- 's' or 'scissors' for Scissors
- 'q' to quit the game

FEATURES:
- Input validation (handles typos and invalid choices)
- Score tracking across multiple rounds
- Visual feedback with ASCII art (optional)
- Clear win/loss messages
- Simple and intuitive interface

REQUIREMENTS: Python 3.6+ (uses random module, no external dependencies)
"""

import random

class RockPaperScissors:
    def __init__(self):
        self.choices = {
            'r': {'name': 'Rock', 'beats': 's'},
            'p': {'name': 'Paper', 'beats': 'r'},
            's': {'name': 'Scissors', 'beats': 'p'}
        }
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0

    def get_player_choice(self):
        """Get and validate player's choice"""
        print("\nChoose:")
        print("  [r] Rock")
        print("  [p] Paper")
        print("  [s] Scissors")
        print("  [q] Quit")

        while True:
            choice = input("\nYour choice: ").lower().strip()

            if choice == 'q':
                return None
            elif choice in self.choices:
                return choice
            elif choice in ['rock', 'paper', 'scissors']:
                # Map full words to keys
                for key, value in self.choices.items():
                    if value['name'].lower() == choice:
                        return key
            else:
                print("Invalid choice! Please enter r, p, s, or q.")

    def get_computer_choice(self):
        """Generate random computer choice"""
        return random.choice(list(self.choices.keys()))

    def determine_winner(self, player, computer):
        """Determine winner based on choices"""
        if player == computer:
            return 'tie'
        elif self.choices[player]['beats'] == computer:
            return 'player'
        else:
            return 'computer'

    def display_choices(self, player_choice, computer_choice):
        """Show what each player chose"""
        print(f"\nYou chose: {self.choices[player_choice]['name']}")
        print(f"Computer chose: {self.choices[computer_choice]['name']}")

    def display_winner(self, winner):
        """Display winner message and update scores"""
        if winner == 'tie':
            print("🤝 It's a tie!")
            self.ties += 1
        elif winner == 'player':
            print("🎉 You win! 🎉")
            self.player_score += 1
        else:
            print("💻 Computer wins! 💻")
            self.computer_score += 1

        self.rounds_played += 1

    def display_scores(self):
        """Show current game statistics"""
        print("\n" + "="*40)
        print("SCOREBOARD")
        print("="*40)
        print(f"You:        {self.player_score}")
        print(f"Computer:   {self.computer_score}")
        print(f"Ties:       {self.ties}")
        print(f"Total Rounds: {self.rounds_played}")

        if self.rounds_played > 0:
            win_percentage = (self.player_score / self.rounds_played) * 100
            print(f"Win Rate:   {win_percentage:.1f}%")
        print("="*40)

    def display_ascii_art(self, choice):
        """Optional: Show ASCII art for choices"""
        art = {
            'r': """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
            'p': """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
            's': """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
        }
        return art.get(choice, "")

    def play_round(self, show_art=False):
        """Play a single round"""
        # Get choices
        player_choice = self.get_player_choice()
        if player_choice is None:
            return False

        computer_choice = self.get_computer_choice()

        # Show ASCII art if requested
        if show_art:
            print("\n" + self.display_ascii_art(player_choice))
            print("VS")
            print(self.display_ascii_art(computer_choice))

        # Display and determine winner
        self.display_choices(player_choice, computer_choice)
        winner = self.determine_winner(player_choice, computer_choice)
        self.display_winner(winner)
        self.display_scores()

        return True

    def run(self):
        """Main game loop"""
        print("\n" + "="*40)
        print("ROCK PAPER SCISSORS")
        print("="*40)
        print("Play ROCK PAPER SCISSORS against your computer. Created by Ravi Rizaei!")

        # Ask about ASCII art preference
        show_art = input("\nShow ASCII art? (yes/no): ").lower().strip() in ['yes', 'y']

        # Game loop
        while True:
            if not self.play_round(show_art):
                break

            # Ask if player wants to continue
            print("\n--- Next Round ---")

        # Game over - show final stats
        print("\n" + "="*40)
        print("GAME OVER - FINAL STATISTICS")
        print("="*40)
        self.display_scores()

        # Final message based on performance
        if self.player_score > self.computer_score:
            print("\n🏆 Congratulations! You're the champion! 🏆")
        elif self.computer_score > self.player_score:
            print("\n👑 Computer wins the match! Better luck next time! 👑")
        elif self.rounds_played > 0:
            print("\n🤝 It's a draw! Good match! 🤝")

        print("\nThanks for playing! 👋")

def main():
    """Main program entry point"""
    game = RockPaperScissors()
    game.run()

if __name__ == "__main__":
    main()