import heapq
from course import Course


class Platform:
    def __init__(self):
        self.courses = {}  # Dictionary to store courses with name as key and Course object as value
        self.prerequisite_map = {}  # Graph representation with courses as keys and list of dependent courses as values

    def add_course(self, course_name, level, duration, prerequisites={}, ):
        if course_name in self.courses:
            raise ValueError(f"Course '{course_name}' already exists")
        course = Course(course_name, level, duration)
        self.courses[course_name] = course
        self.prerequisite_map[course_name] = []
        for prerequisite in prerequisites:
            if prerequisite not in self.courses:
                raise ValueError(f"Prerequisite '{prerequisite}' not found")
            self.prerequisite_map[course_name].append(prerequisite)
        course.add_prerequisite(prerequisites)  # Add prerequisite directly to the course object

    def course_enroll(self, course_name, completed, area_interests, performance):
        if course_name not in self.courses:
            raise ValueError(f"Course '{course_name}' not found")
        visited = set()  # Track visited courses
        processed = set()  # Track Processed courses to avoid processing it again if a different prerequisite lead to the same node
        # Check for circular dependencies using difficulty-aware topological sort
        regular_course_path, personalized_course_path = self._can_enroll_helper(course_name, visited, processed,
                                                                               completed)
        if not regular_course_path:
            raise ValueError(
                f"Course '{course_name}' circular dependency detected. Consider revising course prerequisites.")
        if not personalized_course_path:
            raise ValueError(
                f"Course '{course_name}' and its prerequisites has been already completed by the user.")
        # return regular_course_path
        print("Initial course path: ", regular_course_path, "and duration",
              sum([self.courses[c].duration for c in regular_course_path]))
        personalized_course_path, parallel_courses = self._generate_personalized_learning_path(personalized_course_path,
                                                                                          area_interests, completed,
                                                                                          performance)

        return personalized_course_path, sum([self.courses[c].duration for c in personalized_course_path]), parallel_courses

    def _can_enroll_helper(self, course_name, visited, processed, completed):
        if course_name in visited:
            return []  # Cycle detected, return empty list
        visited.add(course_name)
        regular_course_path = []
        personalized_course_path = []
        for dependent in self.prerequisite_map[course_name]:
            # Recursively check if dependent courses can be enrolled in
            if dependent not in processed:
                start_courses_for_dependent, start_personalized_course_path = self._can_enroll_helper(dependent, visited,
                                                                                                 processed, completed)
                if start_courses_for_dependent:
                    # If dependent can be enrolled in, add it as a potential starting point
                    regular_course_path.extend(start_courses_for_dependent)
                    personalized_course_path.extend(start_personalized_course_path)
                else:
                    # If dependent has a circular dependency, return empty list
                    return []
        # if course_name not in completed:
        regular_course_path.append(course_name)
        if course_name not in completed:
            personalized_course_path.append(course_name)
        # Remove course_name from visited only after processing all dependents
        visited.remove(course_name)
        processed.add(course_name)
        return regular_course_path, personalized_course_path

    def _generate_personalized_learning_path(self, courses, area_interests, completed, performance):
        interested_course, independent_courses, personalized_path = self.get_personalized_enrollable_courses(completed,
                                                                                                             area_interests,
                                                                                                             courses)
        # for course in personalized_path[:]:
        #     if self.prerequisite_map[course] == []:
        #         if course in area_interests:
        #             interested_course.append(course)
        #         else:
        #             independent_courses.append(course)
        #         personalized_path.remove(course)
        #     else:
        #         is_independent = True
        #         for prereq in self.prerequisite_map[course]:
        #             if prereq not in completed:
        #                 is_independent = False
        #                 break
        #         if is_independent:
        #             if course in area_interests:
        #                 interested_course.append(course)
        #             else:
        #                 independent_courses.append(course)
        #             personalized_path.remove(course)

        h = []
        for course in interested_course:
            if performance < 4:
                h.append((self.courses[course].level, course))
            else:
                h.append((-self.courses[course].level, course))
        heapq.heapify(h)

        updated_interested_course = []
        for level, course in h:
            updated_interested_course.append(course)
        # print("updated_interested_course", updated_interested_course, "interested_course", interested_course)
        # print("independent_courses:", independent_courses, "Reminder:", personalized_path)
        updated_path = updated_interested_course + independent_courses + personalized_path
        parallel_courses = updated_interested_course + independent_courses
        return updated_path, parallel_courses

    def get_personalized_enrollable_courses(self, completed, interested_courses, courses=[]):
        # Returns a list of all enrollable courses (no outstanding prerequisites)
        is_remove = True
        if not courses:
            courses = list(self.courses)
            is_remove = False
        enrollable_interested = []
        enrollable_rest = []
        for course_name in courses[:]:
            enrollable_course = None
            if not self.prerequisite_map[course_name] and course_name not in completed:
                enrollable_course = course_name
                if is_remove:
                    courses.remove(course_name)
            elif self.prerequisite_map[course_name]:
                is_independent = True
                for prereq in self.prerequisite_map[course_name]:
                    if prereq not in completed:
                        is_independent = False
                        break
                if is_independent:
                    enrollable_course = course_name
                    if is_remove:
                        courses.remove(course_name)
            if enrollable_course:
                if enrollable_course in interested_courses:
                    enrollable_interested.append(enrollable_course)
                else:
                    enrollable_rest.append(enrollable_course)

        if is_remove:
            return enrollable_interested, enrollable_rest, courses
        return enrollable_interested + enrollable_rest

    # def get_parallel_enrollable_courses(self, enrollable_courses):
    #     """Identifies courses from the list that can be enrolled in parallel (no common dependencies)."""
    #     independent_courses = {}
    #     for course in enrollable_courses:
    #         independent_courses[course] = set(self.prerequisite_map[course])
    #     for course1, dependencies1 in independent_courses.items():
    #         for course2, dependencies2 in independent_courses.items():
    #             if course1 != course2 and not dependencies1.intersection(dependencies2):
    #                 # No common dependencies, so they can be enrolled in parallel
    #                 yield course1, course2
