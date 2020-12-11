from datetime import datetime


class Message:
    def __init__(self, name, message, time=None, id=None, _id=None):
        self.id = id
        self.name = name
        self.message = message
        self.time = time or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        for field in self.__dict__.keys():
            if not getattr(self, field) and field != 'id':
                raise Warning()

    def __lt__(self, other):
        return self.id < other.id

    def get(self, field):
        return self.__getattribute__(field)

    def as_dict(self):
        return self.__dict__
