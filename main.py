import random
from dataclasses import dataclass
from typing import List, Dict


"""

What is the difference between courses' allowedDegrees "advanced" or "2nd" and courses' capacities "MLDS"?

"""


@dataclass
class Course:
    code: int
    name: str
    allowedDegrees: List[str]
    type: str  # theoretical or practical
    language: str  # Hebrew or English
    capacities: Dict[str, int]  # {degree: capacity} where degree is '1st', '2nd', 'advanced' # nopep8


@dataclass
class Constraint:
    courses: List[int]  # list of courses codes
    number: int  # number of courses from this constraint


@dataclass
class Student:
    id: int
    name: str
    email: str
    degree: str
    language: str
    preferences_courses_codes: List[int]  # list of courses codes - the student's preferences - ordered by priority # nopep8
    desired_courses_number: int  # number of courses the student wants to enroll in
    enrolled_courses: List[int] = None
    constraints: List[Constraint] = None

    # Initialize the student's enrolled courses and constraints
    def __post_init__(self):
        self.enrolled_courses = []
        self.constraints = []


def createStudents():
    students = [
        Student(id=1, name='student1', email='student1@post.runi.ac.il', degree='1st', language='Hebrew', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=2),  # nopep8
        Student(id=2, name='student2', email='student2@post.runi.ac.il', degree='2nd', language='English', preferences_courses_codes=[4, 3, 2, 1], desired_courses_number=3),  # nopep8
        Student(id=3, name='student3', email='student3@post.runi.ac.il', degree='advanced', language='Hebrew', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=4, name='student4', email='student4@post.runi.ac.il', degree='1st', language='English', preferences_courses_codes=[1, 3, 4, 2], desired_courses_number=2),  # nopep8
        Student(id=5, name='student5', email='student5@post.runi.ac.il', degree='advanced', language='English', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=6, name='student6', email='student6@post.runi.ac.il', degree='2nd', language='Hebrew', preferences_courses_codes=[3, 2], desired_courses_number=1),  # nopep8
        Student(id=7, name='student7', email='student7@post.runi.ac.il', degree='1st', language='English', preferences_courses_codes=[3, 1, 4, 2], desired_courses_number=2),  # nopep8
        Student(id=8, name='student8', email='student8@post.runi.ac.il', degree='advanced', language='Hebrew', preferences_courses_codes=[2, 1, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=9, name='student9', email='student9@post.runi.ac.il', degree='2nd', language='English', preferences_courses_codes=[2, 4, 1, 3], desired_courses_number=2),  # nopep8
        Student(id=10, name='student10', email='student10@post.runi.ac.il', degree='advanced', language='English', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
    ]
    return students


def createCourses():
    courses = [
        Course(code=1, name='course1', allowedDegrees=['1st', '2nd', 'advanced'], type='theoretical', language='Hebrew', capacities={'1st': 2, '2nd': 2, 'advanced': 2}),  # nopep8
        Course(code=2, name='course2', allowedDegrees=['1st', '2nd'], type='practical', language='English', capacities={'1st': 2, '2nd': 2}),  # nopep8
        Course(code=3, name='course3', allowedDegrees=['1st'], type='theoretical', language='English', capacities={'1st': 2}),  # nopep8
        Course(code=4, name='course4', allowedDegrees=['2nd'], type='theoretical', language='Hebrew', capacities={'2nd': 2}),  # nopep8
    ]
    return courses


def bidding_course_match(students, courses):
    """
    1. Draw a random order of the students. Let's denote by L the list of students in the random order.
    2. Go over L, enroll every student i to the first course in his preferences list that still has capacity. Make sure to mark the course as full once the student is enrolled. Also make sure to mark out the course from the student's preferences list.
    Each student should only be enrolled to one course in each round.
    3. Remove from L students that have been enrolled in their desired number of courses, or those that their preferences list is all marked out.
    4. If L is not empty, REVERSE it, and go back to step 2.
    """

    courses_dict: Dict[int, Course] = {course.code: course for course in courses}  # nopep8
    L: List[Student] = random.sample(students, len(students))

    while L:
        next_round_students = []

        for student in L:
            got_enrolled = False

            for preferred_course_code in list(student.preferences_courses_codes):
                if courses_dict[preferred_course_code].capacities.get(student.degree, 0) > 0:
                    courses_dict[preferred_course_code].capacities[student.degree] -= 1
                    student.enrolled_courses.append(preferred_course_code)
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    got_enrolled = True
                    break

            if len(student.enrolled_courses) < student.desired_courses_number and student.preferences_courses_codes:
                if got_enrolled:
                    next_round_students.append(student)
                else:
                    print(f"Student {student.id} couldn't be enrolled in any more courses.")  # nopep8

        if next_round_students == L:
            break

        L = list(reversed(next_round_students))

    return students, courses_dict


def main():
    students = createStudents()
    courses = createCourses()

    enrolled_students, courses_after_enrollment = bidding_course_match(students, courses)  # nopep8

    print("Enrolled students:")
    for student in enrolled_students:
        print(f"{student.name}: {student.enrolled_courses}")

    print("Courses' capacities:")
    for course in courses_after_enrollment.values():
        print(f"{course.name}: {course.capacities}")


if __name__ == '__main__':
    main()
