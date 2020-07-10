from datetime import time
from dbmanager import DbManager
from lesson import Lesson


def list_returner(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if result:
            return result
        else:
            return [dict()]
    return wrapper


class Timetable:
    def __init__(self, begin_time=time(hour=8), lessons_count=8, between_lessons_break=time(minute=5)):
        self.begin_time = begin_time
        self.lessons_count = lessons_count
        self.between_classes_break = between_lessons_break
        self.lessons_manager = DbManager()

    def add_lesson(self, lesson):
        self.lessons_manager.add(lesson)

    def update_lesson(self, old_lesson, lesson):
        self.lessons_manager.update(old_lesson, lesson)

    def delete_lesson(self, lesson):
        try:
            self.lessons_manager.delete(lesson)
        except:
            print('No lesson')

    @list_returner
    def get_filtered_lessons(self, filter):
        lessons = []
        i = 6
        filtered_lessons = []
        for lesson in self.lessons_manager.find(filter):
            filtered_lessons.append(Lesson.init_by_dict(lesson))
        for lesson in sorted(filtered_lessons):
            lesson_dict = lesson.as_dict()
            lesson_dict['_id'] = i
            lessons.append(lesson_dict)
            i += 1
        return lessons

    def read_timetable(self, filter):
        output = list()
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            filter['week_day'] = day
            lessons = self.get_filtered_lessons(filter)
            output.append('[' + ', '.join([str(lesson) for lesson in lessons]) + ']')
        if output:
            return ('[' + ', '.join(output) + ']').replace('None', 'null')
        return '[]'
