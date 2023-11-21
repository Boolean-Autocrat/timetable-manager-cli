from app.sections import Section
from datetime import datetime
from utils.colors import colors
import csv


class Timetable:
    def __init__(self, cursor):
        self.cursor = cursor
        self.timetable = {}
        self.exam_timetable = {}

    def initials_to_day(self, initials: str):
        if initials == "M":
            return "Monday"
        elif initials == "T":
            return "Tuesday"
        elif initials == "W":
            return "Wednesday"
        elif initials == "Th":
            return "Thursday"
        elif initials == "F":
            return "Friday"
        elif initials == "S":
            return "Saturday"
        else:
            return None

    def enroll_subject(self, course: object, section_id: str):
        if not course.exists():
            return
        course_section = Section(section_id, self.cursor, course)
        timeslot = course_section.get_datetime()
        if timeslot is None:
            print(
                "\n"
                + colors.FAIL
                + f"Section {section_id} not found for {course.get_course_code()}!"
                + colors.ENDC
                + "\n"
            )
            return
        timeslot[2] = datetime.strptime(timeslot[2], "%H:%M").time()
        timeslot[3] = datetime.strptime(timeslot[3], "%H:%M").time()
        days_of_week = timeslot[0].split(",")
        clash = self.check_clashes(days_of_week, timeslot)
        if not clash:
            for day in days_of_week:
                if day not in self.timetable:
                    self.timetable[day] = []
                    self.timetable[day].append(timeslot[1:4])
                else:
                    self.timetable[day].append(timeslot[1:4])
            print(
                "\n"
                + colors.OKGREEN
                + f"Successfully enrolled {course.get_course_code()} Section {section_id} into timetable!"
                + colors.ENDC
                + "\n"
            )

    def unenroll_subject(self, course, section_id):
        success = False
        if not course.exists:
            return
        course_section = Section(section_id, self.cursor, course)
        if not course_section.exists:
            return
        for day in self.timetable:
            for subject in self.timetable[day]:
                if subject[0] == f"{course.get_course_code()}_{section_id}":
                    self.timetable[day].remove(subject)
                    success = True
        if not success:
            print(
                "\n"
                + colors.FAIL
                + f"{course.get_course_code()} Section {section_id} not found in timetable!"
                + colors.ENDC
                + "\n"
            )
            return
        print(
            "\n"
            + colors.OKGREEN
            + f"Successfully unenrolled {course.get_course_code()} Section {section_id} from timetable!"
            + colors.ENDC
            + "\n"
        )
        return

    def display_timetable(self):
        self.__reorder_timetable()
        print("\n" + colors.BOLD + "Timetable" + colors.ENDC + "\n")
        for day in self.timetable:
            print(colors.BOLD + self.initials_to_day(day) + colors.ENDC)
            for subject in self.timetable[day]:
                print(
                    f"{subject[0].split('_')[0]} Section {subject[0].split('_')[1]}: {subject[1]} - {subject[2]}"
                )
            print("\n")

    def check_clashes(self, days_of_week: list, timeslot: list):
        for day in days_of_week:
            if day not in self.timetable:
                pass
            else:
                for subject in self.timetable[day]:
                    if subject[1] > timeslot[2] and subject[2] > timeslot[3]:
                        pass
                    elif subject[1] < timeslot[2] and subject[2] < timeslot[3]:
                        pass
                    else:
                        print(
                            "\n"
                            + colors.FAIL
                            + f"Clash detected with {subject[0].split('_')[0]} Section {subject[0].split('_')[1]} on {self.initials_to_day(day)}"
                            + colors.ENDC
                            + "\n"
                        )
                        return True
        return False

    def __reorder_timetable(self):
        for day in self.timetable:
            self.timetable[day].sort(key=lambda x: x[1])

    def export_to_csv(self):
        self.__reorder_timetable()
        with open(
            f"Timetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "w", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["Day", "Course", "Start Time", "End Time"])
            for day in self.timetable:
                for subject in self.timetable[day]:
                    writer.writerow(
                        [
                            self.initials_to_day(day),
                            subject[0].split("_")[0]
                            + " Section "
                            + subject[0].split("_")[1],
                            subject[1],
                            subject[2],
                        ]
                    )
        print(
            "\n"
            + colors.OKGREEN
            + f"Successfully exported timetable to {file.name}!"
            + colors.ENDC
            + "\n"
        )
