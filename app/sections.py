class Section:
    def __init__(self, section, cursor, courseDependency):
        self.section = section
        self.cursor = cursor
        self.course = courseDependency
        self.datetime = self.__get_timeslot()

    def __get_timeslot(self):
        self.cursor.execute(
            "SELECT days_of_week, start_time, end_time FROM sections WHERE section = ?",
            (self.section,),
        )
        result = [i for i in self.cursor.fetchone()]
        result.insert(1, self.course.get_course_code())
        result.extend([self.course.get_mid_sem(), self.course.get_end_sem()])
        return result

    def get_datetime(self):
        return self.datetime
