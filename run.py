import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import random
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("QuizScores").worksheet("Scores")

console = Console()

def clear_terminal():
    """
    Clears the terminal window prior to new content.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

class Quiz:
    """A class to manage the Travel & Geography Quiz."""

    def welcome_user(self):
        """Display a welcome message to the user.
        """
        clear_terminal()
        print("=====================================")
        print("Welcome to the Travel & Geography Quiz!")
        print("Test your knowledge and see how well you score.")
        print("=====================================")

    def validate_name(self, name):
        """Validate that the name is alphabetic and has a reasonable length."""
        if not name.replace(" ", "").isalpha() or len(name) < 2 or len(name) > 50:
            console.print("[red]Invalid name. Please enter a name with alphabetic characters only (2-50 characters).[/red]")
            return False
        return True

    def validate_age(self, age):
        """Validate that age is numeric and within a reasonable range."""
        if not age.isdigit():
            console.print("[red]Invalid age. Please enter numbers only.[/red]")
            return False
        age = int(age)
        if age < 10 or age > 120:
            console.print("[red]Invalid age. Please enter an age between 10 and 120.[/red]")
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
        
        while True:
            age = input("Enter your age (10-120):\n").strip()
            if self.validate_age(age):
                self.age = int(age)
                clear_terminal()
                break
        clear_terminal() # Clear the terminal after collecting user information
        console.print(f"[green]Welcome, {self.name}! Let's get started.[/green]")

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

    def run_quiz(self):
        """Run the quiz by presenting questions to the user."""
        self.score = 0  # Reset score at the start of the quiz
        summary = []

        for idx, question in enumerate(self.questions, start=1):
            clear_terminal()
            console.print(f"\n[bold yellow]Question {idx}: {question['question']}[/bold yellow]")
            for i, option in enumerate(question["options"], start=1):
                console.print(f"{i}. {option}", style="cyan")

            while True:
                try:
                    choice = int(input("Enter the number of your choice:\n").strip())
                    if 1 <= choice <= len(question["options"]):
                        break
                    else:
                        console.print("[red]Invalid choice. Please select a valid option.[/red]")
                except ValueError:
                    console.print("[red]Invalid input. Please enter a number.[/red]")

            selected_option = question["options"][choice - 1]
            if selected_option == question["answer"]:
                self.score += 1
                result = "Correct"
            else:
                result = "Wrong"

            # Add question details to the summary
            summary.append({
                "question": question["question"],
                "your_answer": selected_option,
                "correct_answer": question["answer"],
                "result": result
            })

            # Provide immediate feedback to the user
            if result == "Correct":
                console.print("[green]Correct![/green]")
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
            SHEET.append_row([self.name, self.score, timestamp])
            console.print("[bold green]Your results have been saved to the leaderboard![/bold green]")
        except Exception as e:
            console.print(f"[red]Failed to save results: {e}[/red]")

    def display_leaderboard(self):
        """Prompt the user and display the leaderboard from Google Sheets"""
        while True: 
            console.print("\n[bold cyan]Would you like to view the leaderboard? (y/n)[/bold cyan]")
            choice = input("Enter your choice:\n").strip().lower()

            if choice in ["y", "yes"]:
                clear_terminal()  # Clear the terminal
                try:
                    data = SHEET.get_all_values()[1:]  # Skip the header row
                    if not data:  # Check if data is empty
                        console.print("[bold red]No scores available on the leaderboard yet![/bold red]")
                        return

                    # Sort data by score (index 1), descending, and limit to top 10
                    sorted_data = sorted(data, key=lambda x: int(x[1]), reverse=True)[:10]

                    table = Table(title="Leaderboard", style="cyan")
                    table.add_column("Name", justify="left", style="magenta", no_wrap=True)
                    table.add_column("Score", justify="center", style="green")
                    table.add_column("Date", justify="left", style="yellow")
                
                    for row in sorted_data:
                        table.add_row(row[0], row[1], row[2])

                    console.print(table)
                except Exception as e:
                    console.print(f"[red]Failed to fetch leaderboard: {e}[/red]")
                break

            elif choice in ["n", "no"]:  # Redirect to beginning
                    clear_terminal()
                    console.print("[bold green]Redirecting to the beginning...[/bold green]")
                    main()  # Restart the program
                    break  # This line won't actually execute since `main()` restarts

            else:  # Invalid input
                    console.print("[red]Invalid input. Please enter 'y' or 'n'.[/red]")

def main():
    """Main function to handle the program execution."""
    while True:
        quiz = Quiz() 
        quiz.welcome_user() 
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