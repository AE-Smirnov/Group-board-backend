from pymongo import MongoClient


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DbManager(metaclass=MetaSingleton):
    def __init__(self):
        client = MongoClient('mongodb+srv://admin:admin@cluster0.pwmrs.mongodb.net/test?retryWrites=true&w=majority')
        db = client.test
        self.collection = db.collection

    def add(self, lesson):
        add_dict = lesson.as_dict()
        add_dict['id'] = self.next_id()
        self.collection.insert_one(add_dict)

    def find(self, filter):
        return self.collection.find(filter)

    def update(self, filter, lesson):
        self.collection.update(filter, {'$set': lesson.as_dict()})

    def delete(self, lesson):
        self.collection.remove(lesson.as_dict())

    def next_id(self):
        return self.collection.aggregate([
            {
                '$group': {
                    '_id': None,
                    'maxQuantity': {'$max': "$id"}
                }
            }
        ]).next()['maxQuantity'] + 1
