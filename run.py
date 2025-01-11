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
            name = input("Enter your name (2-50 characters, alphabetic only): ").strip()
            if self.validate_name(name):
                self.name = name
                break
        
        while True:
            age = input("Enter your age (10-120): ").strip()
            if self.validate_age(age):
                self.age = int(age)
                break
        clear_terminal() # Clear the terminal after collecting user information
        console.print(f"[green]Welcome, {self.name}! Let's get started.[/green]")

def main():
    """Main function to handle the program execution."""
    quiz = Quiz() # Create an instance of Quiz
    quiz.welcome_user() # Show the welcome message
    quiz.get_user_info() 

if __name__ == "__main__":
    main()