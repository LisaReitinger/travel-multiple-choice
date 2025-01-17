import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import random
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track
from pyfiglet import Figlet
import re
import threading

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
# Open Google Sheet and define both worksheets
SHEET = CLIENT.open("QuizScores")
EASY_SCORES = SHEET.worksheet("Easy Scores")
HARD_SCORES = SHEET.worksheet("Hard Scores")

console = Console()

def clear_terminal():
    """
    Clears the terminal window prior to new content.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def title_screen():
    """
    Display a title screen using pyfiglet.
    """
    f = Figlet(font="big", width=80)
    clear_terminal()
    rendered_text = f.renderText("TRAVEL QUIZ").splitlines()  # Split text into lines
    for line in rendered_text:
        print(line.center(80))
    print("Welcome to the Travel & Geography Quiz!".center(80))
    print("Test your knowledge and see how well you score.\n".center(80))
    print("\nInstructions:")
    print("1. Answer each question by typing the number of your choice.")
    print("2. Your final score will be displayed at the end.")
    print("3. View the leaderboard to compare scores with others.\n")
    console.print("[bold cyan]Press Enter to start the quiz...[/bold cyan]")
    input()
    clear_terminal()

class Quiz:
    """A class to manage the Travel & Geography Quiz."""
    
    def validate_name(self, name):
        """Validate that the name is alphabetic and has a reasonable length."""
        name = name.strip()

        # Check if name contains only alphabetic characters and spaces
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", name):
            console.print("[red]Invalid name. Use only alphabetic characters (A-Z, a-z) and spaces.[/red]")
            return False

        # Ensure name is between 2 and 20 characters
        if len(name) < 2 or len(name) > 20:
            console.print("[red]Invalid name length. Must be between 2 and 20 characters.[/red]")
            return False

        # Prevent multiple consecutive spaces
        if "  " in name:
            console.print("[red]Invalid name. No consecutive spaces allowed.[/red]")
            return False

        return True

    def get_user_info(self):
        """Collect and validate user information."""
        while True:
            name = input("Enter your name:\n").strip()
            if self.validate_name(name):
                self.name = name
                clear_terminal()
                break

        # Ask user for difficulty mode
        while True:
            console.print("\n[bold cyan]Choose Difficulty Level:[/bold cyan]")
            console.print("1. Easy Mode (No Timer)\n2. Hard Mode (5-second Timer)")
            choice = input("Enter 1 for Easy or 2 for Hard:\n").strip()

            if choice == "1":
                self.difficulty = "Easy"
                self.sheet = EASY_SCORES
                break
            elif choice == "2":
                self.difficulty = "Hard"
                self.sheet = HARD_SCORES
                break
            else:
                console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")
        
        clear_terminal() 
        console.print(f"[green]Welcome, {self.name}! Playing in {self.difficulty} Mode.[/green]\n")

    def load_questions(self):
        """Load questions for the quiz"""
        self.questions = [
            {
                "question": "Where can you find the Christ the Redeemer statue?",
                "options": ["Argentina", "Brazil", "Chile", "Mexico"],
                "answer": "Brazil",
            },
            {
                "question": "What is the capital of Canada?",
                "options": ["Toronto", "Vancouver", "Ottawa", "Montreal"],
                "answer": "Ottawa",
            },
            {
                "question": "Which country has a red circle on a white background in its flag?",
                "options": ["South Korea", "Japan", "Bangladesh", "Switzerland"],
                "answer": "Japan",
            },
            {
                "question": "Which country has the most islands in the world?",
                "options": ["Indonesia", "Sweden", "Philippines", "Canada"],
                "answer": "Sweden",
            },
            {
                "question": "I am the highest mountain in the world. What am I?",
                "options": ["K2", "Mount Kilimanjaro", "Mount Everest", "Mount McKinley"],
                "answer": "Mount Everest",
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
                "answer": "Pacific Ocean",
            },
            {
                "question": "What is the capital city of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "answer": "Canberra",
            },
            {
                "question": "In which country can you find Machu Picchu?",
                "options": ["Peru", "Chile", "Mexico", "Brazil"],
                "answer": "Peru",
            },
            {
                "question": "What is the longest river in the world?",
                "options": ["Nile", "Amazon", "Yangtze", "Mississippi"],
                "answer": "Nile",
            },
            {
                "question": "Which country is known as the 'Land of the Rising Sun'?",
                "options": ["China", "Japan", "South Korea", "Thailand"],
                "answer": "Japan",
            },
        ]

        # Shuffle the questions
        random.shuffle(self.questions)

    def run_quiz(self):
        """Run the quiz by presenting questions to the user."""
        self.score = 0  # Reset score at the start of the quiz
        summary = []

        for idx, question in enumerate(self.questions, start=1):
            clear_terminal()
            console.print(f"\n[bold yellow]Question {idx}: {question['question']}[/bold yellow]")
            for i, option in enumerate(question["options"], start=1):
                console.print(f"[bright_cyan]{i}. {option}[/bright_cyan]")

            # Timer function (only for Hard mode)
            def timeout():
                console.print("\n[red]Time's up! Moving to the next question...[/red]")
                self.timeout_flag = True

            self.timeout_flag = False
            selected_option = None

            if self.difficulty == "Hard":
                timer = threading.Timer(5.0, timeout) 
                timer.start()

            while True:
                try:
                    choice = input("Enter the number of your choice:\n").strip()
                    
                    if self.timeout_flag:  # If timer ran out, break out of input loop
                        break
                    
                    if choice.isdigit():
                        choice = int(choice)
                        if 1 <= choice <= len(question["options"]):
                            selected_option = question["options"][choice - 1]
                            break
                        else:
                            console.print("[red]Invalid choice. Please select a valid option.[/red]")
                    else:
                        console.print("[red]Invalid input. Please enter a number.[/red]")
                except ValueError:
                    console.print("[red]Invalid input. Please enter a number.[/red]")

            if self.difficulty == "Hard":
                timer.cancel()  # Stop the timer if the user answered in time

            # Determine if answer is correct or if user ran out of time
            if not selected_option:
                result = "Timeout"
            elif selected_option == question["answer"]:
                self.score += 1
                result = "Correct"
            else:
                result = "Wrong"

            summary.append({
                "question": question["question"],
                "your_answer": selected_option if selected_option else "No Answer",
                "correct_answer": question["answer"],
                "result": result
            })

            # Provide immediate feedback
            if result == "Correct":
                console.print("[green]Correct![/green]")
            elif result == "Timeout":
                console.print(f"[red]You ran out of time! The correct answer was: {question['answer']}[/red]")
            else:
                console.print(f"[red]Wrong! The correct answer was: {question['answer']}[/red]")

        clear_terminal()
        # Show the final score
        console.print(f"\n[bold green]Quiz Complete![/bold green] You scored {self.score}/{len(self.questions)}.")

        # Display the summary in chunks 
        chunk_size = 4 
        for i in range(0, len(summary), chunk_size):
            clear_terminal()
            chunk = summary[i:i + chunk_size]
            console.print("\n[bold cyan]Quiz Summary[/bold cyan]")
            for idx, item in enumerate(chunk, start=i + 1):
                console.print(f"\n[bold yellow]Question {idx}:[/bold yellow] {item['question']}")
                console.print(f"Your Answer: [cyan]{item['your_answer']}[/cyan] | Correct Answer: [green]{item['correct_answer']}[/green]")
                console.print(f"Result: [bold green]{item['result']}[/bold green]" if item["result"] == "Correct" else f"[bold red]{item['result']}[/bold red]")
            
            # Show message if more chunks remain
            if i + chunk_size < len(summary):
                input("\nPress Enter to see the rest of your results...")
    
        self.save_results()

    def save_results(self):
        """Save the user's quiz results to Google Sheets."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            self.sheet.append_row([self.name, self.score, timestamp])  # Save to correct sheet

            console.print("[bold green]Your results have been saved to the leaderboard![/bold green]")
        except Exception as e:
            console.print(f"[red]Failed to save results: {e}[/red]")

    def display_leaderboard(self):
        """Allow user to select which leaderboard to view (Easy or Hard)."""
        clear_terminal()

        # Select the correct sheet based on difficulty mode
        sheet_name = "Easy Scores" if self.difficulty == "Easy" else "Hard Scores" 

        try:
            leaderboard_sheet = SHEET.worksheet(sheet_name)

            console.print(f"\n[bold cyan]Showing {sheet_name} Leaderboard[/bold cyan]")

            data = leaderboard_sheet.get_all_values()[1:]  # Skip the header row
            if not data:  # Check if leaderboard is empty
                console.print("[bold red]No scores available yet![/bold red]")
                return

            sorted_data = sorted(data, key=lambda x: int(x[1]), reverse=True)[:10]

            table = Table(title=f"{self.difficulty} Mode Leaderboard", style="cyan")
            table.add_column("Name", justify="left", style="bright_magenta", no_wrap=True)
            table.add_column("Score", justify="center", style="green")
            table.add_column("Date", justify="left", style="yellow")

            for row in sorted_data:
                table.add_row(row[0], row[1], row[2])

            console.print(table)
        except Exception as e:
            console.print(f"[red]Failed to fetch leaderboard: {e}[/red]")

def main():
    """Main function to handle the program execution."""
    title_screen()  # Display the title and welcome message

    while True:
        quiz = Quiz() 
        quiz.get_user_info() 
        quiz.load_questions() 
        quiz.run_quiz()

        while True:
            console.print("\n[bold cyan]What would you like to do next?[/bold cyan]")
            console.print("1. Play Again\n2. View Leaderboard\n3. Exit")
            choice = input("Enter your choice (1/2/3):\n").strip()

            if choice == "1":  # Play again
                clear_terminal()
                break  # Exit inner loop and restart the quiz
            elif choice == "2":  # View leaderboard
                clear_terminal()
                quiz.display_leaderboard()
                # Stay in the loop for further options after leaderboard
            elif choice == "3":  # Exit
                console.print("[bold green]Thank you for playing! Goodbye![/bold green]")
                return  # Exit the program entirely
            else:  # Invalid input
                console.print("[red]Invalid input. Please enter 1, 2, or 3.[/red]")
                # Re-prompt without exiting the loop

if __name__ == "__main__":
    main()