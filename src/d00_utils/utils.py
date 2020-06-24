import openpyxl
import os
import pandas as pd
import time


def print_file_date(FILE_DIR):
    """Print the last modification and creation date."""
    print("Last modified: %s" % time.ctime(os.path.getmtime(FILE_DIR)))
    print("Created: %s" % time.ctime(os.path.getctime(FILE_DIR)))


def create_folder(DIR):
    """Create directory if it does not exist."""
    if not os.path.exists(DIR):
        os.makedirs(DIR, exist_ok=True)


def verify_task_completion(question):
    """Checks whether a task was completed in a yes/no format."""
    if not "(y/n)" in question:
        question = question + " (y/n)"
    response = input(question)
    if response.lower() == "y":
        print("Please continue.")
    elif response.lower() == "n":
        print("Please complete the task.")
        exit()
    else:
        verify_task_completion(question)


def delete_excel_file(file_dir):
    file_exists = os.path.exists(file_dir)
    if file_exists:
        response = input("File already exists. Delete the file? (y/n)")
        response = response.lower()
        if response == "y":
            os.remove(file_dir)
            print("File deleted.")
        elif response == "n":
            print("Please delete the file manually.")
            pass
        else:
            create_excel_file(file_dir)


def add_excel_sheet(df, file_dir, sheet_name):
    """Create/adds sheets to specified excel file."""
    writer = pd.ExcelWriter(file_dir, engine="openpyxl")
    if os.path.exists(file_dir):
        writer = pd.ExcelWriter(file_dir, engine="openpyxl", mode="a")
        book = openpyxl.load_workbook(file_dir)
        writer.book = book

    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
    writer.close()


def make_percent(x):
    """Converts a decimal into a percent string."""
    return f"{x*100}%"