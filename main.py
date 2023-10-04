from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


"Знайти 5 студентів із найбільшим середнім балом з усіх предметів"
def select_one():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))\
                    .select_from(Grade).join(Student).group_by(Student.id).order_by(desc("avg_grade")).limit(5).all()    # label дозволяє перейменувати змінну
    return result


"Знайти студента із найвищим середнім балом з певного предмета"
def select_two(discipline_id):
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"), Discipline.fullname)\
                    .select_from(Grade).join(Student).join(Discipline).where(Discipline.id == discipline_id)\
                    .group_by(Student.id, Discipline.id).order_by(desc("avg_grade")).first()
    return result


"Знайти середній бал у групах з певного предмета"
def select_three(discipline_id):
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"), Discipline.fullname)\
                    .select_from(Grade).join(Student).join(Group).join(Discipline).where(Discipline.id == discipline_id)\
                    .group_by(Group.id, Discipline.id).order_by(desc("avg_grade")).all()
    return result


"Знайти середній бал на потоці (по всій таблиці оцінок)"
def select_four():
    result = session.query(func.round(func.avg(Grade.grade), 2)).select_from(Grade).first()
    return result


"Знайти які курси читає певний викладач"
def select_five(teacher_id):
    result = (session.query(Teacher.fullname, Discipline.fullname).select_from(Discipline).join(Teacher).where(Teacher.id == teacher_id).all())
    return result


"Знайти список студентів у певній групі"
def select_six(group_id):
    result = session.query(Group.name, Student.fullname).select_from(Student).join(Group).where(Group.id == group_id).all()
    return result


"Знайти оцінки студентів у окремій групі з певного предмета"
def select_seven(group_id, discipline_id):
    result = session.query(Group.name, Student.fullname, Grade.grade, Discipline.fullname).select_from(Grade).join(Student)\
                    .join(Group).join(Discipline).where(and_(Group.id == group_id, Discipline.id == discipline_id))\
                    .order_by(desc(Grade.grade)).all()
    return result


"Знайти середній бал, який ставить певний викладач зі своїх предметів"
def select_eight(teacher_id):
    result = (session.query(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"), Discipline.fullname).select_from(Grade)\
                    .join(Discipline).join(Teacher).where(Teacher.id == teacher_id).group_by(Teacher.id, Discipline.id)\
              .order_by(desc("avg_grade")).all())
    return result


"Знайти список курсів, які відвідує певний студент"
def select_nine(student_id):
    result = (session.query(Student.fullname, Discipline.fullname).select_from(Grade).join(Student).join(Discipline)\
              .where(Student.id == student_id)).group_by(Discipline.id, Student.id).all()
    return result


"Список курсів, які певному студенту читає певний викладач"
def select_ten(student_id, teacher_id):
    result = (session.query(Student.fullname, Discipline.fullname, Teacher.fullname).select_from(Grade).join(Student)\
                    .join(Discipline).join(Teacher).where(and_(Teacher.id == teacher_id, Student.id == student_id))\
                    .group_by(Teacher.id, Student.id, Discipline.id).all())
    return result


"Середній бал, який певний викладач ставить певному студентові"
def select_eleven(student_id, teacher_id):
    result = (session.query(Student.fullname, func.round(func.avg(Grade.grade), 2), Discipline.fullname, Teacher.fullname)\
                    .select_from(Grade).join(Student).join(Discipline).join(Teacher)\
                    .where(and_(Teacher.id == teacher_id, Student.id == student_id)).group_by(Teacher.id, Student.id, Discipline.id).all())
    return result


"Оцінки студентів у певній групі з певного предмета на останньому занятті"
def select_twelve(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    result = (session.query(Discipline.fullname, Student.fullname, Group.name, Grade.date_of, Grade.grade)\
                .select_from(Grade).join(Student).join(Discipline).join(Group)\
                .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)))\
                .order_by(desc(Grade.date_of)).all()
    return result


if __name__ == '__main__':
    print(select_one())
    print(select_two(4))
    print(select_three(6))
    print(select_four())
    print(select_five(5))
    print(select_six(1))
    print(select_seven(1, 6))
    print(select_eight(5))
    print(select_nine(35))
    print(select_ten(48, 5))
    print(select_eleven(1, 4))
    print(select_twelve(6, 1))