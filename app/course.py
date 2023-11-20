from utils.colors import colors
import inquirer
import re
from utils.color_input import color_input


class Course:
    """
    Course class to store course data
    """

    def __init__(self, course_code, cursor, connection):
        self.course_code = course_code
        self.connection = connection
        self.cursor = cursor
        self.sections = {}
        self.exists = True

        self.cursor.execute(
            """
            SELECT course_name, midsem_date, compre_date, incharge, credits FROM courses WHERE course_code = ?
            """,
            (self.course_code,),
        )

        result = self.cursor.fetchone()
        if result is None or len(result) == 0:
            print(f"{colors.FAIL}Course not found!{colors.ENDC}")
            self.exists = False
            return
        (
            self.course_name,
            self.midsem_date,
            self.compre_date,
            self.course_ic,
            self.credits,
        ) = result

        query = """
            SELECT section_id, instructors, section_type, days_of_week, start_time, end_time
            FROM sections
            WHERE course_code = ?
        """

        self.cursor.execute(query, (self.course_code,))
        result = self.cursor.fetchall()

        if result is not None:
            for section in result:
                if section[2] not in self.sections:
                    self.sections[section[2]] = []
                self.sections[section[2]].append(
                    {
                        "section_id": section[0],
                        "instructors": section[1],
                        "days_of_week": section[3],
                        "start_time": section[4],
                        "end_time": section[5],
                    }
                )

    def exists(self):
        return self.exists

    def get_course_code(self):
        return self.course_code

    def get_mid_sem(self):
        return self.midsem_date

    def get_end_sem(self):
        return self.compre_date

    def get_all_sections(self, section_type: str):
        if section_type.lower() not in ["lecture", "lab", "tutorial", "all"]:
            print(f"{colors.FAIL}Invalid section type{colors.ENDC}")

        elif section_type.lower() == "all":
            if len(self.sections) == 0:
                print(f"{colors.FAIL}No sections found!{colors.ENDC}")
                return
            print(f"{colors.OKCYAN}Sections for {self.course_code}{colors.ENDC}")
            for item in self.sections:
                print(f"{colors.OKGREEN}{item.title()}{colors.ENDC}")
                for section in self.sections[item]:
                    print(
                        f"  - {colors.OKBLUE}Section Code:{colors.ENDC} {section['section_id'].split('_')[1]}"
                    )
                    print(
                        f"  - {colors.OKBLUE}Instructors:{colors.ENDC} {', '.join(map(str.strip, section['instructors'].split(',')))}"
                    )
                    print(
                        f"  - {colors.OKBLUE}Days of week:{colors.ENDC} {' '.join(map(str.strip, section['days_of_week'].split(',')))}"
                    )
                    print(
                        f"  - {colors.OKBLUE}Time slot:{colors.ENDC} {section['start_time']} - {section['end_time']}"
                    )
                    print()
        else:
            if section_type not in self.sections:
                print(f"{colors.FAIL}No such section type{colors.ENDC}")
                return
            print(
                f"{colors.OKCYAN}{section_type.title()} Sections for {self.course_code}{colors.ENDC}\n"
            )
            for section in self.sections[section_type]:
                print(
                    f"  - {colors.OKBLUE}Section Code:{colors.ENDC} {section['section_id'].split('_')[1]}"
                )
                print(
                    f"  - {colors.OKBLUE}Instructors:{colors.ENDC} {', '.join(map(str.strip, section['instructors'].split(',')))}"
                )
                print(
                    f"  - {colors.OKBLUE}Days of week:{colors.ENDC} {' '.join(map(str.strip, section['days_of_week'].split(',')))}"
                )
                print(
                    f"  - {colors.OKBLUE}Time slot:{colors.ENDC} {section['start_time']} - {section['end_time']}"
                )
                print()

    def get_section(self, section_code: str):
        sections = []
        for section_type in self.sections:
            for section in self.sections[section_type]:
                sections.append(section["section_id"].split("_")[1])

        if section_code not in sections:
            print(f"{colors.FAIL}No such section!{colors.ENDC}")
            return
        else:
            for section_type in self.sections:
                for param in self.sections[section_type]:
                    if param["section_id"].split("_")[1] != section_code:
                        continue
                    else:
                        print(
                            f"{colors.OKCYAN}Section {section_code} - {self.course_code}{colors.ENDC}"
                        )
                        print(
                            f"  - {colors.OKBLUE}Instructors:{colors.ENDC} {', '.join(map(str.strip, param['instructors'].split(',')))}"
                        )
                        print(
                            f"  - {colors.OKBLUE}Days of week:{colors.ENDC} {' '.join(map(str.strip, param['days_of_week'].split(',')))}"
                        )
                        print(
                            f"  - {colors.OKBLUE}Time slot:{colors.ENDC} {param['start_time']} - {param['end_time']}"
                        )

    def __str__(self):
        statement = f"{colors.OKBLUE}Course name:{colors.ENDC} {self.course_name}\n{colors.OKBLUE}Course code:{colors.ENDC} {self.course_code}\n{colors.OKBLUE}Course incharge:{colors.ENDC} {self.course_ic}\n{colors.OKBLUE}Midsem date:{colors.ENDC} {self.midsem_date}\n{colors.OKBLUE}Compre date:{colors.ENDC} {self.compre_date}\n{colors.OKBLUE}Credits:{colors.ENDC} {self.credits}"
        return statement

    def __populate_sections(self, section_type: str, section_data: dict):
        self.cursor.execute(
            """
            INSERT INTO sections (section_id, course_code, instructors, section_type, days_of_week, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{self.course_code}_{section_data['section_id']}",
                self.course_code,
                section_data["instructors"],
                section_type,
                section_data["days_of_week"],
                section_data["start_time"],
                section_data["end_time"],
            ),
        )
        self.connection.commit()

    def auth_populate_sections(self, key: str, env_key):
        if key == env_key:
            questions = [
                inquirer.List(
                    "type",
                    message="Select section type: (use arrow keys to navigate)",
                    choices=["Lecture", "Lab", "Tutorial"],
                ),
            ]
            answers = inquirer.prompt(questions)
            section_code = color_input("Enter section code (T1, P6, L1 etc.): ")
            instructors = color_input("Enter instructors (comma separated): ")
            days_of_week = color_input(
                "Enter days of week (comma separated - M, T, W, Th, F, S): "
            )
            start_time = color_input("Enter the starting time: (HH:MM) ")
            end_time = color_input("Enter the ending time: (HH:MM) ")
            validate: bool = self.__validate_section_data(
                section_code, days_of_week, start_time, end_time, instructors
            )
            if not validate:
                return
            section_data = {
                "section_id": section_code,
                "instructors": ",".join(map(str.strip, instructors.split(","))),
                "days_of_week": ",".join(map(str.strip, days_of_week.split(","))),
                "start_time": start_time,
                "end_time": end_time,
            }
            self.__populate_sections(answers["type"].lower(), section_data)
            if answers["type"].lower() not in self.sections:
                self.sections[answers["type"].lower()] = []
            self.sections[answers["type"].lower()].append(section_data)
        else:
            print("Invalid key.")

    def __validate_section_data(
        self, section_code, days_of_week, start_time, end_time, instructors
    ):
        if section_code == "":
            print(f"{colors.FAIL}Section code cannot be empty!{colors.ENDC}")
            return False
        if days_of_week == "":
            print(f"{colors.FAIL}Days of week cannot be empty!{colors.ENDC}")
            return False
        if start_time == "":
            print(f"{colors.FAIL}Start time cannot be empty!{colors.ENDC}")
            return False
        if end_time == "":
            print(f"{colors.FAIL}End time cannot be empty!{colors.ENDC}")
            return False
        if instructors == "":
            print(f"{colors.FAIL}Instructors cannot be empty!{colors.ENDC}")
            return False
        for day in map(str.strip, days_of_week.split(",")):
            if day not in ["M", "T", "W", "Th", "F", "S"]:
                print(f"{colors.FAIL}Invalid days of week!{colors.ENDC}")
                return False
        section_code_regex = r"^[TPL]\d+$"
        time_regex = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
        if not re.match(time_regex, start_time):
            print(f"{colors.FAIL}Invalid start time!{colors.ENDC}")
            return False
        if not re.match(time_regex, end_time):
            print(f"{colors.FAIL}Invalid end time!{colors.ENDC}")
            return False
        if not re.match(section_code_regex, section_code):
            print(f"{colors.FAIL}Invalid section code!{colors.ENDC}")
            return False
        return True
