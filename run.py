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

if __name__ == "__main__":
    main()