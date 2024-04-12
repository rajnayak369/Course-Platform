class Course:
    def __init__(self, name, level, duration):
        self.name = name
        self.prerequisites = set()
        self.level = level
        self.duration = duration

    def add_prerequisite(self, prerequisite_course):
        self.prerequisites = prerequisite_course  # Adds a prerequisite course to this course

    def __str__(self):
        return f"Course: {self.name}"
