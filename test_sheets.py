import sys
from sheets.roadmap import (
    get_today_tasks,
    get_today_deadlines,
    mark_previous_pending_as_missed,
    update_task_status,
    task_key
)
from datetime import datetime
from google.auth.exceptions import TransportError

def run_test():
    try:
        # Format today's date as in the sheet
        today_str = datetime.now().strftime("%d-%m-%Y")
        today_dt = datetime.strptime(today_str, "%d-%m-%Y")

        print(f"🔎 Testing for today: {today_str}")
        print(f"🔄 Testing Google Sheets connection...")

        # --- 1. Get tasks starting today
        try:
            tasks_today = get_today_tasks(today_str)
            print("\n✅ Tasks starting today:")
            for task in tasks_today:
                print("-", task_key(task), "→", task.get("Status", "No status"))
        except Exception as e:
            print(f"\n❌ Error getting today's tasks: {str(e)}")
            return False

        # --- 2. Get tasks with deadline today
        try:
            deadlines_today = get_today_deadlines(today_str)
            print("\n⏰ Deadlines today:")
            if deadlines_today:
                for task in deadlines_today:
                    print("-", task_key(task))
            else:
                print("- None")
        except Exception as e:
            print(f"\n❌ Error getting today's deadlines: {str(e)}")
            return False

        # --- 3. Mark previous pending tasks as missed
        try:
            mark_previous_pending_as_missed(today_dt)
        except Exception as e:
            print(f"\n❌ Error marking previous tasks as missed: {str(e)}")
            return False

        # --- 4. (Optional) Update a sample task's status
        if tasks_today:
            first = tasks_today[0]
            task_id = task_key(first)
            print(f"\nAttempting to mark task as Done: {task_id}")
            success = update_task_status(first["Start Date"], first["Topic"], "Done")
            if not success:
                print(f"❌ Failed to update task status")
                return False
        else:
            print("\nNo tasks to mark as Done.")

        print("\n✅ All tests completed successfully!")
        return True

    except TransportError as e:
        print(f"\n❌ Google Sheets connection error: {str(e)}")
        print("Please check your internet connection and try again.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
