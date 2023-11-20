<h1 style="text-align: center;">Clash-Free Timetable Generator</h1>
Welcome to the Clash-Free Timetable Generator! This Python application provides a user-friendly interface to view course details, add new sections, generate a clash-free timetable, and export the timetable to a CSV file.

## Dev Features

- [x] Tried to maintain modularity and separation of concerns
- [x] Mostly OOP implementation with dependency injection
- [x] Regular and regex validation for user input
- [x] Full error handling
- [x] Colored outputs
- [x] Admin key (it's `admin`, defined in `.env`)
- [x] ASCII art

## General Features

- [x] View Courses and Sections:

  - Enter the course code to view details about the course, including its name, incharge, midsem date, compre date, and credits.
  - View all sections or a specific section type (lecture, lab, tutorial) for a given course.
  - View details of a specific section using its section code.

- [x] Add New Sections:

  - An administrator can add new sections to a course, providing details such as section type, section code, instructors, days of the week, start time, and end time.

- [x] Generate Clash-Free Timetable:

  - Enroll in a course and section to generate a clash-free timetable.
  - The application checks for timetable clashes.

- [x] Export to CSV:
  - Export the generated timetable to a CSV file.

## Run this project

- Clone this repo
- Create a virtualenv and activate it
  ```
  python3 -m venv venv
  ./venv/Scripts/activate.bat or source venv/bin/activate
  ```
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Run the project
  ```
  python main.py
  ```

## File Structure

```
timetable-manager-dvm-rec1/
├─ .env
├─ .gitignore
├─ app/
│ ├─ __init__.py
│ ├─ course.py
│ ├─ sections.py
│ └─ timetable.py
├─ main.py
├─ manager.db
├─ README.md
├─ requirements.txt
└─ utils/
   ├─ __init__.py
   ├─ color_input.py
   ├─ colors.py
   ├─ excel_helper.py
   ├─ subjects.xlsx
   └─ word_art.py
```
