from dbmanager import DbManager

class Lesson:
    def __init__(self, name, teacher, week_day, lesson_number, room, id=None):
        self.name = name
        self.teacher = teacher
        self.week_day = week_day
        self.lesson_number = int(lesson_number)
        self.room = room
        self.id = id
        for field in ['name', 'teacher', 'week_day', 'lesson_number', 'room', 'id']:
            if not getattr(self, field):
                raise Warning()

    def __lt__(self, other):
        if self.week_day != other.week_day:
            return self.week_day < other.week_day
        return self.lesson_number < other.lesson_number

    def get(self, field):
        return self.__getattribute__(field)

    def as_dict(self):
        res = {}
        for field in ['name', 'teacher', 'lesson_number', 'week_day', 'room', 'id']:
            res[field] = getattr(self, field)
        return res

    def free(self, id=None):
        search_filter = {'week_day': self.week_day, 'lesson_number': self.lesson_number}
        data = DbManager().find(search_filter)
        if data.count() and not data[0]['id'] == id:
            raise Warning('Busy!')
        return True

    def __str__(self):
        return f'{self.name}\nПреподаватель: {self.teacher}\nАудитория: {self.room}'

    @classmethod
    def init_by_dict(cls, lesson_dict):
        return cls(lesson_dict['name'], lesson_dict['teacher'], lesson_dict['week_day'],
                   lesson_dict['lesson_number'], lesson_dict['room'], lesson_dict.get('id'))