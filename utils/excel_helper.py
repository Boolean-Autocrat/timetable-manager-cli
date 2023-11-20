import os
import openpyxl


def populate_course(cursor, connection):
    file = os.path.join(os.path.dirname(__file__), "subjects.xlsx")
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2):
        course_code = row[0].value
        course_name = row[1].value
        course_ic = row[2].value
        course_credits = row[3].value
        course_midsem = row[4].value
        course_endsem = row[5].value

        cursor.execute(
            "REPLACE INTO courses (course_code, course_name, incharge, credits, midsem_date, compre_date) VALUES (?, ?, ?, ?, ?, ?)",
            (
                course_code,
                course_name,
                course_ic,
                course_credits,
                course_midsem,
                course_endsem,
            ),
        )
        connection.commit()
