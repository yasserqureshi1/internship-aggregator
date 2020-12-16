import sqlite3
import sys

conn = sqlite3.connect('init.db')
cursor = conn.cursor()


def create_db():
    choice = input("WARNING: WILL OVERWRITE ANY SAVED DATA ARE YOU SURE YOU WANT TO RUN? [y/n]")
    if choice == "y":
        confirm = input("ARE YOU SURE? [y/n]")
        if confirm == "y":
            print("proceeding")
        else:
            sys.exit(0)
    else:
        sys.exit(0)

    return


# Create Companies TABLE with the following columns:
#       - Company name
#       - Company description

# Create Position Table with following columns
#       - Position
#       - Division
#       - Internship/placement/graduate
#       - Timescale
#       - Date posted
#       - Company

