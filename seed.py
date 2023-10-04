from datetime import date, datetime, timedelta
from random import randint
import faker

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


fake = faker.Faker("uk-UA")

NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
MAX_NUMBERS_OF_GRADES = 20

disciplines = [
    "Вища математика",
    "Дискретна математика",
    "Лінійна алгебра",
    "Програмування",
    "Теорія імовірності",
    "Історія України",
    "Англійська мова"
]

groups = ["42-ЄС1", "42-ЛЗ2", "12-ЄС3"]

"""
Створюємо свою ф-цію для отримання списку дат, у які відбувається навчальний процес.
Для спрощення викидаємо тільки дні, які потрапляють на вихідні.
"""


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def seed_groups():
    for group_name in groups:
        group = Group(name=group_name)
        session.add(group)
    session.commit()


def seed_teachers():
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    session.commit()


def seed_disciplines():
    for discipline in disciplines:
        discipline_to_add = Discipline(fullname=discipline, teacher_id=randint(1, NUMBER_TEACHERS))
        session.add(discipline_to_add)
    session.commit()


def seed_students():
    for _ in range(NUMBER_STUDENTS):
        student = Student(fullname=fake.name(), group_id=randint(1, len(groups)))
        session.add(student)
    session.commit()


def seed_grades():
    all_dates = date_range(start=datetime(year=2022, month=9, day=1), end=datetime(year=2023, month=6, day=15))
    student_grades_count = {}

    for day in all_dates:
        random_discipline = randint(1, len(disciplines))
        random_students = [randint(1, NUMBER_STUDENTS) for _ in range(4)]
        for student in random_students:
            if student not in student_grades_count:
                student_grades_count[student] = 0
            if student_grades_count[student] < MAX_NUMBERS_OF_GRADES:
                grade = Grade(grade=randint(1, 12), date_of=day, student_id=student, discipline_id=random_discipline)
                session.add(grade)
                student_grades_count[student] += 1
    session.commit()


if __name__ == '__main__':
    seed_groups()
    seed_teachers()
    seed_disciplines()
    seed_students()
    seed_grades()
