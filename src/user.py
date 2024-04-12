class User:
    def __init__(self, name):
        self.name = name
        self.performance = 1
        self.completed_courses = set()
        self.interested_courses = set()

    def update_performance(self, level):
        self.performance = level

    def add_completed_course(self, course_name):
        self.completed_courses.add(course_name)

    def add_interested_course(self, course_name):
        self.interested_courses.add(course_name)

    def __str__(self):
        return f"User name: {self.name}"
