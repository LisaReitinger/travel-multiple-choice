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

def welcome_user():
    """Display a welcome message to the user.
    """
    print("=====================================")
    print("Welcome to the Travel & Geography Quiz!")
    print("Test your knowledge and see how well you score.")
    print("=====================================")

def validate_name(name):
    """Validate that the name is alphabetic and has a reasonable length."""
    if not name.replace(" ", "").isalpha() or len(name) < 2 or len(name) > 50:
        console.print("[red]Invalid name. Please enter a name with alphabetic characters only (2-50 characters).[/red]")
        return False
    return True

def validate_age(age):
    """Validate that age is numeric and within a reasonable range."""
    if not age.isdigit():
        console.print("[red]Invalid age. Please enter numbers only.[/red]")
        return False
    age = int(age)
    if age < 10 or age > 120:
        console.print("[red]Invalid age. Please enter an age between 10 and 120.[/red]")
        return False
    return True

def main():
    """Main function to handle the program execution."""
    pass

if __name__ == "__main__":
   main()