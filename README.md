<div align="center">
<h1>📚 Clash-Free Timetable Generator</h1>
<h4>- By Suyash Handa</h6>
</div>

NOTES:

1. The sqlite3 database is already populated with some data. You can add more data by updating the `utlils/subjects.xlsx` file and supplying the admin key when prompted.
2. A sample generated timetable is already present in the working directory.
3. Check the `utils/subjects.xlsx` file for existing courses.

## Dev Features

- [x] Tried to maintain modularity and separation of concerns
- [x] Mostly OOP implementation with dependency injection
- [x] Regular and regex validation for user input
- [x] Tried maximum error handling coverage
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

## Screenshots

<details><summary><b>Images (Click to Expand)</b></summary>
![Screenshot 1](.github/images/Screenshot1)
![Screenshot 2](.github/images/Screenshot2)
![Screenshot 3](.github/images/Screenshot3)
![Screenshot 4](.github/images/Screenshot4)
![Screenshot 5](.github/images/Screenshot5)
![Screenshot 6](.github/images/Screenshot6)
![Screenshot 7](.github/images/Screenshot7)
![Screenshot 8](.github/images/Screenshot8)
![Screenshot 9](.github/images/Screenshot9)
</details>

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
