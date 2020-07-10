from timetable import Timetable
from lesson import Lesson
from dbmanager import DbManager


def add_lesson(timetable, lesson_dict):
    lesson = Lesson.init_by_dict(lesson_dict)
    if not lesson.id and lesson.free():
        timetable.add_lesson(lesson)
    elif lesson.free(lesson.id):
        timetable.update_lesson(DbManager().find({'id': lesson.id})[0], lesson)
    return lesson.as_dict()

def delete_lesson(timetable, lesson_dict):
    lesson = Lesson.init_by_dict(lesson_dict)
    timetable.delete_lesson(lesson)


def init_timetable(**kwargs):
    return Timetable(kwargs)


def get_all(timetable):
    return timetable.read_timetable({})
