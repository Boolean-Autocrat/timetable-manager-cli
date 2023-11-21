class Section:
    def __init__(self, section, cursor, courseDependency):
        self.section = section
        self.cursor = cursor
        self.course = courseDependency
        self.datetime = self.__get_timeslot()

    def __get_timeslot(self):
        self.cursor.execute(
            "SELECT days_of_week, start_time, end_time FROM sections WHERE section_id = ?",
            (f"{self.course.get_course_code()}_{self.section}",),
        )
        pre_result = self.cursor.fetchone()
        if not pre_result:
            return None
        result = [i for i in pre_result]
        result.insert(1, f"{self.course.get_course_code()}_{self.section}")
        result.extend([self.course.get_mid_sem(), self.course.get_end_sem()])
        return result

    def get_datetime(self):
        return self.datetime
