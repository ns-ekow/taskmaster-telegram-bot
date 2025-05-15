from datetime import datetime
import gspread
import time
import os
from google.oauth2.service_account import Credentials
from google.auth.exceptions import TransportError
from typing import List, Dict, Tuple

# Constants
DATE_FORMAT = "%d-%m-%Y"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Load Google Sheets client with retry logic
def get_sheet(sheet_name: str = "ROADMAP") -> gspread.Worksheet:
    from config.settings import SERVICE_ACCOUNT_PATH, SPREADSHEET_ID

    # Verify that the service account file exists
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        raise FileNotFoundError(f"Service account file not found at {SERVICE_ACCOUNT_PATH}")

    # Retry logic for network issues
    for attempt in range(MAX_RETRIES):
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
            return sheet
        except TransportError as e:
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                print(f"Google Sheets connection error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
        except gspread.exceptions.SpreadsheetNotFound:
            raise ValueError(f"Spreadsheet with ID {SPREADSHEET_ID} not found. Check your SPREADSHEET_ID in .env file.")
        except gspread.exceptions.WorksheetNotFound:
            raise ValueError(f"Worksheet '{sheet_name}' not found in the spreadsheet.")
        except Exception as e:
            raise Exception(f"Error connecting to Google Sheets: {str(e)}")


# Convert a row into a dictionary
def row_to_dict(header: List[str], row: List[str]) -> Dict:
    return {header[i]: row[i] if i < len(row) else "" for i in range(len(header))}


# Fetch all tasks from the sheet
def fetch_all_tasks() -> Tuple[List[Dict], gspread.Worksheet, List[str]]:
    sheet = get_sheet()

    # Retry logic for fetching data
    for attempt in range(MAX_RETRIES):
        try:
            rows = sheet.get_all_values()
            if not rows:
                raise ValueError("No data found in the spreadsheet")

            header = rows[0]
            if not header:
                raise ValueError("Header row is empty in the spreadsheet")

            tasks = [row_to_dict(header, row) for row in rows[1:]]
            return tasks, sheet, header
        except TransportError as e:
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)
                print(f"Error fetching data: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            raise Exception(f"Error fetching data from spreadsheet: {str(e)}")


# Get tasks starting today
def get_today_tasks(today: str) -> List[Dict]:
    tasks, _, _ = fetch_all_tasks()
    return [t for t in tasks if t.get("Start Date") == today]


# Get tasks with deadline today
def get_today_deadlines(today: str) -> List[Dict]:
    tasks, _, _ = fetch_all_tasks()
    return [t for t in tasks if t.get("Deadline") == today]


# Mark previous pending tasks as missed
def mark_previous_pending_as_missed(today: datetime):
    tasks, sheet, header = fetch_all_tasks()
    status_col = header.index("Status") + 1  # 1-indexed

    print("⚠️ Marking previous 'Pending' tasks as 'Missed'...")

    for i, row in enumerate(tasks):
        try:
            start_date_str = row.get("Start Date", "")
            status = row.get("Status", "").strip()

            if not start_date_str or status != "Pending":
                continue

            start_date = datetime.strptime(start_date_str, DATE_FORMAT)
            if start_date < today:
                sheet.update_cell(i + 2, status_col, "Missed")  # +2 for header offset
                print(f"  - Marked '{row.get('Topic')}' as Missed (was Pending)")
        except Exception as e:
            print(f"  - Error processing task {i+1}: {str(e)}")
            continue


# Update task status
def update_task_status(start_date: str, topic: str, new_status: str) -> bool:
    try:
        tasks, sheet, header = fetch_all_tasks()

        # Make sure Status column exists
        try:
            status_col = header.index("Status") + 1
        except ValueError:
            print(f"Error: 'Status' column not found in spreadsheet")
            return False

        # Find and update the matching task
        for i, row in enumerate(tasks):
            if row.get("Start Date") == start_date and row.get("Topic") == topic:
                try:
                    sheet.update_cell(i + 2, status_col, new_status)
                    print(f"✅ Marking first task as {new_status} → {start_date}::{topic}")
                    return True
                except Exception as e:
                    print(f"Error updating cell: {str(e)}")
                    return False

        print(f"Task not found: {start_date}::{topic}")
        return False

    except Exception as e:
        print(f"Error in update_task_status: {str(e)}")
        return False


# Helper: Generate unique key
def task_key(task: Dict):
    return f"{task.get('Start Date')}::{task.get('Topic')}"
