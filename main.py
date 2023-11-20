from app.course import Course
from app.sections import Section
from app.timetable import Timetable
from utils.excel_helper import populate_course
from utils.colors import colors
from utils.word_art import wordart_first, wordart_second
from utils.color_input import color_input
import sqlite3
from dotenv import load_dotenv
import os
import re

load_dotenv()
ADMIN_KEY = os.getenv("ADMIN_KEY")


def main():
    try:
        con = sqlite3.connect("manager.db")
    except:
        print("Error opening database")
        return
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        course_name TEXT,
        midsem_date TEXT,
        compre_date TEXT,
        incharge TEXT,
        credits INTEGER
    );
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS sections (
        section_id TEXT PRIMARY KEY,
        course_code TEXT,
        instructors TEXT,
        section_type TEXT,
        days_of_week TEXT,
        start_time TEXT,
        end_time TEXT,
        FOREIGN KEY (course_code) REFERENCES courses (course_code));
"""
    )
    print(f"{wordart_first}\n{wordart_second}\n")
    print("---------------------------------------------")
    if color_input("Do you want to populate the database? (y/n): ").strip() == "y":
        db_populate_key = color_input("Enter the admin key: ")
        if db_populate_key.strip() == ADMIN_KEY:
            print("Running course population...")
            populate_course(cur, con)
            print("Done!\n")

    menu_main = {
        1: "View courses/sections and add new sections",
        2: "Generate a clash-free timetable",
        3: "Exit",
    }

    while True:
        print(f"{colors.HEADER}-----------\n Main Menu\n-----------{colors.ENDC}")
        for key in menu_main:
            print(str(key) + ". " + menu_main[key])
        choice = int(color_input("Enter your choice: "))
        print()
        if choice == 1:
            course_code = color_input("Enter course code: ")
            course = Course(course_code, cur, con)
            if not course.exists:
                break
            else:
                submenu = {
                    1: "View course details",
                    2: "View a particular section",
                    3: "View all sections",
                    4: "Add new section",
                    5: "Back",
                }
                while True:
                    print()
                    for key in submenu:
                        print(str(key) + ". " + submenu[key])
                    course_subchoice = int(color_input("Enter your choice: "))
                    print()
                    if course_subchoice == 1:
                        print(course)
                    elif course_subchoice == 2:
                        section_id = color_input("Enter section code (eg T1, P6, L1): ")
                        if re.match(r"^[TPL]\d+$", section_id.strip()):
                            course.get_section(section_id.strip())
                        else:
                            print(f"{colors.FAIL}Invalid section code!{colors.ENDC}")
                    elif course_subchoice == 3:
                        section_type = color_input(
                            "Enter section type (all, lecture, lab, tutorial): "
                        )
                        course.get_all_sections(section_type.strip())
                    elif course_subchoice == 4:
                        admin_key = color_input("Enter the admin key: ")
                        course.auth_populate_sections(admin_key.strip(), ADMIN_KEY)
                    elif course_subchoice == 5:
                        break
        elif choice == 2:
            timetable = Timetable(cur)
            timetable_submenu = {
                1: "Add a course & section",
                2: "Remove a course & section",
                3: "View timetable",
                4: "Parse timetable to CSV",
                5: "Back",
            }
            while True:
                for key in timetable_submenu:
                    print(str(key) + ". " + timetable_submenu[key])
                timetable_subchoice = int(color_input("Enter your choice: "))
                if timetable_subchoice == 1:
                    course_code = color_input("Enter course code: ")
                    section_id = color_input("Enter section code (eg T1, P6, L1): ")
                    if re.match(r"^[TPL]\d+$", section_id.strip()):
                        timetable.enroll_subject(
                            Course(course_code, cur, con), section_id
                        )
                    else:
                        print(f"{colors.FAIL}Invalid section code!{colors.ENDC}")
                elif timetable_subchoice == 2:
                    pass
                elif timetable_subchoice == 3:
                    pass
                elif timetable_subchoice == 4:
                    pass
                elif timetable_subchoice == 5:
                    break
        elif choice == 3:
            print("Thank you for using the clash-free timetable generator!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
