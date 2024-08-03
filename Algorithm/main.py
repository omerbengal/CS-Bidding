import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from abc import ABC
import logging


logging.basicConfig(
    level=logging.INFO,
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    format='%(message)s',
    handlers=[
        logging.FileHandler('my_log_file.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Language codes
HEBREW_LANGUAGE_CODE = 1
ENGLISH_LANGUAGE_CODE = 2

# Degree codes
FIRST_DEGREE_CODE = 1
SECOND_DEGREE_CODE = 2
SECOND_DEGREE_MLDS_CODE = 22
ADVANCED_DEGREE_CODE = 3


"""
✅ - Course should have only one language (same course different language = new course)

✅ - new method that adds a forced constraints to all students for
    (
        1. courses that appear twice because of different languages
        2. courses that by default could not be enrolled in if you took other courses
    )

✅ - new course field - English capacity (only for courses with language "English")
✅ - change course's language to str with the values "Hebrew" or "English"
    ✅
    ! check hebrew students trying to enroll in English courses and vice versa:
    TODO: if student is Hebrew and enrolled in English course - subtract 1 from general "1st" capacity
    TODO: if student is English and enrolled in Hebrew course - subtract 1 from general "1st" capacity AND from English capacity
    ✅

✅ - new DegreeType: "MLDS" - they should be able to enroll in courses with degreeType "2nd" (as well as "MLDS" of course)

- 2nd round for hebrew students who got rejected in the first round for English courses (due to english capacity being more than the actual english students who enrolled)

✅ - change course's "allowedDegrees" to int with the values (1 - 1st, 2 - 2nd, 3 - advanced [1st and 2nd])
    * if student is 1st - show him 1 and 3
    * if student is 2nd - show him 2 and 3

"""


"""
✅ Student's degree 3 should maybe not be MLDS... wait for Tami's answer
"""


@dataclass
class Course(ABC):
    code: int
    name: str
    allowedDegree: int  # 1 - 1st, 2 - 2nd, 22 - 2nd MLDS, 3 - advanced [1st and 2nd] # nopep8
    type: str  # Theoretical or practical
    capacity: int  # Capacity of the course
    semester: int  # 1 - winter, 2 - spring


@dataclass
class HebrewCourse(Course):
    pass


@dataclass
class EnglishCourse(Course):
    englishCapacity: int  # Capacity saved for English students


@dataclass
class Constraint:
    courses_codes: List[int]  # List of courses codes
    counter: int  # Number of courses from this constraint


@dataclass
class Student:
    id: int
    name: str
    email: str
    degree: int  # 1 - 1st, 2 - 2nd, 22 - 2nd MLDS, 3 - advanced [1st and 2nd]
    language: int  # 1 - Hebrew, 2 - English
    preferences_courses_codes: List[int]  # List of courses codes - the student's preferences - ordered by priority # nopep8
    winter_desired_courses_number: int  # Number of courses the student wants to enroll in
    spring_desired_courses_number: int  # Number of courses the student wants to enroll in
    enrolled_courses: List[int] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)


# def createStudents():
#     students = [
#         Student(id=1, name='student1', email='student1@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[3, 2, 4, 1, 5], winter_desired_courses_number=2, spring_desired_courses_number=1),  # nopep
#         # more students
#     ]
#     return students


def createStudents():
    students = [
        Student(id=1, name='student1', email='student1@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[3, 2, 4], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=2, name='student2', email='student2@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 4, 3, 6, 8], winter_desired_courses_number=3, spring_desired_courses_number=2),
        Student(id=3, name='student3', email='student3@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 6], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=4, name='student4', email='student4@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[3, 7, 1, 5], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=5, name='student5', email='student5@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 5, 3, 4, 7], winter_desired_courses_number=2, spring_desired_courses_number=2),
        Student(id=6, name='student6', email='student6@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 8], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=7, name='student7', email='student7@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 1, 5, 6], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=8, name='student8', email='student8@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[4, 2, 6], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=9, name='student9', email='student9@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[3, 7, 2, 6, 8], winter_desired_courses_number=2, spring_desired_courses_number=2),
        Student(id=10, name='student10', email='student10@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 3], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=11, name='student11', email='student11@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 6, 8, 3], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=12, name='student12', email='student12@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 5, 3], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=13, name='student13', email='student13@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 4, 6, 8, 1], winter_desired_courses_number=2, spring_desired_courses_number=2),
        Student(id=14, name='student14', email='student14@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[3, 7], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=15, name='student15', email='student15@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 1, 5], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=16, name='student16', email='student16@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[4, 1, 3, 5], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=17, name='student17', email='student17@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 6, 8], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=18, name='student18', email='student18@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[4, 2, 6, 8], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=19, name='student19', email='student19@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[3, 7, 2], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=20, name='student20', email='student20@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 3, 5, 4], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=21, name='student21', email='student21@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 6], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=22, name='student22', email='student22@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 5, 3, 4, 7], winter_desired_courses_number=3, spring_desired_courses_number=1),
        Student(id=23, name='student23', email='student23@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 4], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=24, name='student24', email='student24@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[3, 7, 1], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=25, name='student25', email='student25@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 1, 5, 6], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=26, name='student26', email='student26@post.runi.ac.il', degree=SECOND_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[4, 1], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=27, name='student27', email='student27@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[2, 6, 8, 3, 7], winter_desired_courses_number=2, spring_desired_courses_number=2),
        Student(id=28, name='student28', email='student28@post.runi.ac.il', degree=SECOND_DEGREE_MLDS_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[4, 2], winter_desired_courses_number=1, spring_desired_courses_number=1),
        Student(id=29, name='student29', email='student29@post.runi.ac.il', degree=ADVANCED_DEGREE_CODE, language=ENGLISH_LANGUAGE_CODE, preferences_courses_codes=[3, 7, 2, 6], winter_desired_courses_number=2, spring_desired_courses_number=1),
        Student(id=30, name='student30', email='student30@post.runi.ac.il', degree=FIRST_DEGREE_CODE, language=HEBREW_LANGUAGE_CODE, preferences_courses_codes=[1, 3, 5], winter_desired_courses_number=2, spring_desired_courses_number=1),
    ]
    return students


def auto_constraint(students: List[Student], courses: List[Course]):
    """
    Method that adds a forced constraint to all students.
    The constraint is that they can only enroll in one course from the list of courses.
    For example - all courses that has a Hebrew AND English versions - each student can only enroll in one of them
    """
    constraint = Constraint(courses_codes=[course.code for course in courses], counter=1)  # nopep8
    for student in students:
        student.constraints.append(constraint)


def createCourses():
    courses = [
        HebrewCourse(code=1, name='course1', allowedDegree=1, type='theoretical', capacity=17, semester=1),  # nopep8
        EnglishCourse(code=2, name='course2', allowedDegree=2, type='practical', capacity=20, englishCapacity=15, semester=1),  # nopep8
        HebrewCourse(code=3, name='course3', allowedDegree=3, type='theoretical', capacity=18, semester=1),  # nopep8
        HebrewCourse(code=4, name='course4', allowedDegree=2, type='theoretical', capacity=20, semester=1),  # nopep8
        HebrewCourse(code=5, name='course5', allowedDegree=1, type='theoretical', capacity=15, semester=2),  # nopep8
        EnglishCourse(code=6, name='course6', allowedDegree=2, type='practical', capacity=20, englishCapacity=10, semester=2),  # nopep8
        HebrewCourse(code=7, name='course7', allowedDegree=3, type='theoretical', capacity=18, semester=2),  # nopep8
        EnglishCourse(code=8, name='course8', allowedDegree=2, type='theoretical', capacity=20, englishCapacity=13, semester=2),  # nopep8
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

    id_in_order = [student.id for student in L]
    print(f"Students' ids acording to the random order: {id_in_order}")

    while L:
        next_round_students = []

        for student in L:
            logger.info("")
            logger.info(f"Proccessing student {student.id} (degree: {student.degree}, language: {student.language}, winter desired courses: {student.winter_desired_courses_number}, spring desired courses: {student.spring_desired_courses_number})")
            logger.info(f"Student's preferences: {student.preferences_courses_codes}")
            got_enrolled = False

            for preferred_course_code in list(student.preferences_courses_codes):
                logger.info(f"-->Proccessing course {courses_dict[preferred_course_code].code} (allowed degree: {courses_dict[preferred_course_code].allowedDegree}, capacity: {courses_dict[preferred_course_code].capacity}, semester: {courses_dict[preferred_course_code].semester})")
                if courses_dict[preferred_course_code] is EnglishCourse:
                    logger.info(f"-->(and English capacity: {courses_dict[preferred_course_code].englishCapacity})")
                # Make sure the student's degree is allowed to enroll in the course
                if courses_dict[preferred_course_code].allowedDegree != student.degree:
                    # If the student is 2nd MLDS and the course is 2nd, DO NOT remove the course from the student's preferences list
                    if not (courses_dict[preferred_course_code].allowedDegree == SECOND_DEGREE_CODE and student.degree == SECOND_DEGREE_MLDS_CODE):
                        # The course's allowed degree is not the student's degree, and we are not in the 2nd MLDS case
                        logger.info(f"----->Course {courses_dict[preferred_course_code].code}'s allowed degree is not the student's degree, and we are not in the 2nd MLDS case")
                        student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                        # TODO - check if the remove AND continue don't skip a course
                        continue

                # Check if there exists a constraint that contains the preferred course and that the number in this constraint is 0 # nopep8
                constraint_with_course_and_number_is_zero_exists = False
                for constraint in student.constraints:
                    if preferred_course_code in constraint.courses_codes and constraint.counter == 0:
                        constraint_with_course_and_number_is_zero_exists = True
                        break

                # If the student has a constraint that contains the preferred course and the number in this constraint is 0, he can't be enrolled in this course # nopep8
                if constraint_with_course_and_number_is_zero_exists:
                    logger.info(f"----->Constraint with course {courses_dict[preferred_course_code].code} and number 0 exists")
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    # TODO - check if the remove AND continue don't skip a course
                    continue

                # If the student's desired number of courses in the current course's semester is 0, remove the course from the student's preferences list # nopep8
                if courses_dict[preferred_course_code].semester == 1 and student.winter_desired_courses_number == 0 \
                or courses_dict[preferred_course_code].semester == 2 and student.spring_desired_courses_number == 0:
                    logger.info(f"----->Desired number of courses in the current course's semester ({courses_dict[preferred_course_code].semester}) is 0")
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    # TODO - check if the remove AND continue don't skip a course
                    continue

                # Check if the course has capacity
                if courses_dict[preferred_course_code].capacity > 0:
                    """🥳HORRAY - the student can be enrolled in the course!🥳"""
                    # Decrease the general capacity of the course by 1
                    courses_dict[preferred_course_code].capacity -= 1
                    # If the student is an English student - decrease the English capacity of the English course by 1
                    if courses_dict[preferred_course_code] is EnglishCourse and student.language == ENGLISH_LANGUAGE_CODE:
                        courses_dict[preferred_course_code].englishCapacity -= 1
                    # Decrease the number in the constraints that contains the preferred course
                    for constraint in student.constraints:
                        if preferred_course_code in constraint.courses_codes:
                            constraint.counter -= 1
                    # Enroll the student in the course
                    student.enrolled_courses.append(preferred_course_code)
                    # Remove the course from the student's preferences list
                    student.preferences_courses_codes.remove(preferred_course_code)  # nopep8
                    # Decrease the number of courses the student wants to enroll in, depending on the semester
                    if courses_dict[preferred_course_code].semester == 1:
                        student.winter_desired_courses_number -= 1
                    else:
                        student.spring_desired_courses_number -= 1
                    # Mark the flag
                    got_enrolled = True
                    logger.info(f"----->Student {student.id} got enrolled in course {courses_dict[preferred_course_code].code}")
                    break
                else:
                    logger.info(f"----->No capacity...")

            # If the student needs to be enrolled in more courses # nopep8
            if student.winter_desired_courses_number > 0 or student.spring_desired_courses_number > 0:
                # If the student got enrolled in a course, add him to the next round
                if got_enrolled:
                    logger.info(f"-->Student {student.id} has made it to the next round")
                    next_round_students.append(student)
                # If the student didn't get enrolled in any course, don't add him to the next round because he is "stuck"
                else:
                    logger.info(f"-->Student {student.id} couldn't be enrolled in any more courses.")  # nopep8
                    # print(f"Student {student.id} couldn't be enrolled in any more courses.")  # nopep8

        # If L is the same as next_round_students, break the loop (because nothing changed)
        if next_round_students == L:
            break
        # Put in L the reversed next_round_students
        L = list(reversed(next_round_students))

    return students, courses_dict


def main():
    students = createStudents()
    courses = createCourses()

    enrolled_students, courses_after_enrollment = bidding_course_match(students, courses)  # nopep8

    for course in courses_after_enrollment.values():
        students = []
        for student in enrolled_students:
            if course.code in student.enrolled_courses:
                students.append(student)
        print(f"{course.name}: {[student.id for student in students]}")


if __name__ == '__main__':
    main()
