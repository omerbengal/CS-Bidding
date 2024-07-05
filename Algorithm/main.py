import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from abc import ABC


"""
✅ - Course should have only one language (same course different language = new course)

✅ - new method that adds a forced constraints to all students for
    (
        1. courses that appear twice because of different languages
        2. courses that by default could not be enrolled in if you took other courses
    )

✅ - new course field - English capacity (only for courses with language "English")
✅ - change course's language to str with the values "Hebrew" or "English"
    ! check hebrew students trying to enroll in English courses and vice versa:
    TODO: if student is Hebrew and enrolled in English course - subtract 1 from general "1st" capacity
    TODO: if student is English and enrolled in Hebrew course - subtract 1 from general "1st" capacity AND from English capacity

- new DegreeType: "MLDS" - they should be able to enroll in courses with degreeType "2nd" (as well as "MLDS" of course)

- 2nd round for hebrew students who got rejected in the first round for English courses (due to english capacity being more than the actual english students who enrolled)

✅ - change course's "allowedDegrees" to int with the values (1 - 1st, 2 - 2nd, 3 - advanced [1st and 2nd])
    * if student is 1st - show him 1 and 3
    * if student is 2nd - show him 2 and 3

-----
"""


"""
Student's degree 3 should maybe not be MLDS... wait for Tami's answer
"""


@dataclass
class Course(ABC):
    code: int
    name: str
    allowedDegree: int  # 1 - 1st, 2 - 2nd, 3 - advanced [1st and 2nd]
    type: str  # theoretical or practical
    capacity: int  # capacity of the course


@dataclass
class HebrewCourse(Course):
    pass


@dataclass
class EnglishCourse(Course):
    englishCapacity: int  # capacity saved for English students


@dataclass
class Constraint:
    courses_codes: List[int]  # list of courses codes
    counter: int  # number of courses from this constraint


@dataclass
class Student:
    id: int
    name: str
    email: str
    degree: int  # 1 - 1st, 2 - 2nd, 3 - MLDS
    language: str
    preferences_courses_codes: List[int]  # list of courses codes - the student's preferences - ordered by priority # nopep8
    desired_courses_number: int  # number of courses the student wants to enroll in
    enrolled_courses: List[int] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)


def createStudents():
    students = [
        Student(id=1, name='student1', email='student1@post.runi.ac.il', degree=1, language='Hebrew', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=2),  # nopep8
        Student(id=2, name='student2', email='student2@post.runi.ac.il', degree=2, language='English', preferences_courses_codes=[4, 3, 2, 1], desired_courses_number=3),  # nopep8
        Student(id=3, name='student3', email='student3@post.runi.ac.il', degree=3, language='Hebrew', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=4, name='student4', email='student4@post.runi.ac.il', degree=1, language='English', preferences_courses_codes=[1, 3, 4, 2], desired_courses_number=2),  # nopep8
        Student(id=5, name='student5', email='student5@post.runi.ac.il', degree=3, language='English', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=6, name='student6', email='student6@post.runi.ac.il', degree=2, language='Hebrew', preferences_courses_codes=[3, 2], desired_courses_number=1),  # nopep8
        Student(id=7, name='student7', email='student7@post.runi.ac.il', degree=1, language='English', preferences_courses_codes=[3, 1, 4, 2], desired_courses_number=2),  # nopep8
        Student(id=8, name='student8', email='student8@post.runi.ac.il', degree=3, language='Hebrew', preferences_courses_codes=[2, 1, 3, 4], desired_courses_number=1),  # nopep8
        Student(id=9, name='student9', email='student9@post.runi.ac.il', degree=2, language='English', preferences_courses_codes=[2, 4, 1, 3], desired_courses_number=2),  # nopep8
        Student(id=10, name='student10', email='student10@post.runi.ac.il', degree=3, language='English', preferences_courses_codes=[1, 2, 3, 4], desired_courses_number=1),  # nopep8
    ]
    return students


def auto_constraint(students: List[Student], courses: List[Course]):
    """
    Method that adds a forced constraint to all students.
    The constraint is that they can only enroll in one course from the list of courses.
    """
    constraint = Constraint(courses_codes=[course.code for course in courses], counter=1)  # nopep8
    for student in students:
        student.constraints.append(constraint)


def createCourses():
    courses = [
        HebrewCourse(code=1, name='course1', allowedDegree=1, type='theoretical', capacity=2),  # nopep8
        EnglishCourse(code=2, name='course2', allowedDegree=2, type='practical', capacity=2, englishCapacity=2),  # nopep8
        HebrewCourse(code=3, name='course3', allowedDegree=3, type='theoretical', capacity=2),  # nopep8
        HebrewCourse(code=4, name='course4', allowedDegree=2, type='theoretical', capacity=2),  # nopep8
    ]
    return courses


def bidding_course_match(students: List[Student], courses: List[Course]) -> Tuple[List[Student], Dict[int, Course]]:
    """
    1. Draw a random order of the students. Let's denote by L the list of students in the random order.
    2. Go over L, enroll every student i to the first course in his preferences list that still has capacity. Make sure to mark the course as full once the student is enrolled. Also make sure to mark out the course from the student's preferences list.
    Each student should only be enrolled to one course in each round.
    3. Remove from L students that have been enrolled in their desired number of courses, or those that their preferences list is all marked out.
    4. If L is not empty, REVERSE it, and go back to step 2.
    """

    courses_dict: Dict[int, Course] = {course.code: course for course in courses}  # nopep8
    L: List[Student] = random.sample(students, len(students))
    students_id_list = [student.id for student in L]
    print(f"Students' ids: {students_id_list}")

    while L:
        next_round_students = []

        for student in L:
            print("student", student.id)
            got_enrolled = False

            for preferred_course_code in list(student.preferences_courses_codes):
                print("course", preferred_course_code)

                # TODO: MAYBE THIS NEEDS TO BE REMOVED (because "we do not mess with the students decisions")
                # check if the student's degree is allowed to enroll in the course
                if courses_dict[preferred_course_code].allowedDegree != student.degree:
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    continue
                # TODO: MAYBE THIS NEEDS TO BE REMOVED (because "we do not mess with the students decisions")

                # check if there exists a constraint that contains the preferred course and that the number in this constraint is 0 # nopep8
                constraint_with_course_and_number_is_zero_exists = False
                for constraint in student.constraints:
                    if preferred_course_code in constraint.courses_codes and constraint.counter == 0:
                        constraint_with_course_and_number_is_zero_exists = True
                        break

                # if the student has a constraint that contains the preferred course and the number in this constraint is 0, he can't be enrolled in this course # nopep8
                if constraint_with_course_and_number_is_zero_exists:
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    continue

                # check if the course has capacity
                if courses_dict[preferred_course_code].capacity > 0:
                    # decrease the capacity of the course by 1
                    courses_dict[preferred_course_code].capacity -= 1
                    # decrease the number in the constraints that contains the preferred course # nopep8
                    for constraint in student.constraints:
                        if preferred_course_code in constraint.courses_codes:
                            constraint.counter -= 1
                    # enroll the student in the course
                    student.enrolled_courses.append(preferred_course_code)
                    # remove the course from the student's preferences list
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    got_enrolled = True
                    print("student", student.id, "enrolled in", preferred_course_code)  # nopep8
                    break

            # if the student needs to be enrolled in more courses and he has more courses to enroll in # nopep8
            if len(student.enrolled_courses) < student.desired_courses_number and student.preferences_courses_codes:
                # if the student got enrolled in a course, add him to the next round
                if got_enrolled:
                    next_round_students.append(student)
                # if the student didn't get enrolled in any course, add him to the next round
                else:
                    print(f"Student {student.id} couldn't be enrolled in any more courses.")  # nopep8

        # if L is the same as next_round_students, break the loop (because nothing changed)
        if next_round_students == L:
            break

        # put in L the reversed next_round_students
        L = list(reversed(next_round_students))

    return students, courses_dict


def main():
    students = createStudents()
    courses = createCourses()

    enrolled_students, courses_after_enrollment = bidding_course_match(students, courses)  # nopep8

    # print("Enrolled students:")
    # for student in enrolled_students:
    #     print(f"{student.name}: {student.enrolled_courses}")

    # print("Courses' capacities:")
    # for course in courses_after_enrollment.values():
    #     print(f"{course.name}: {course.capacity}")


if __name__ == '__main__':
    main()
