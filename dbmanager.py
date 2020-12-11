from pymongo import MongoClient


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DbManager(metaclass=MetaSingleton):
    def __init__(self):
        client = MongoClient('mongodb+srv://admin:admin@cluster0.pwmrs.mongodb.net/messenger?retryWrites=true&w=majority')
        db = client.messenger
        self.collection = db.messenger

    def add(self, message):
        add_dict = message.as_dict()
        add_dict['id'] = self.next_id()
        self.collection.insert_one(add_dict)

    def find(self, filter, limit=20):
        return self.collection.find(filter).limit(limit)

    def update(self, filter, message):
        self.collection.update(filter, {'$set': message.as_dict()})

    def delete(self, message):
        msg_dict = message.as_dict()
        msg_dict.pop('id')
        self.collection.remove(msg_dict)

    def next_id(self):
        return self.collection.aggregate([
            {
                '$group': {
                    '_id': None,
                    'maxQuantity': {'$max': "$id"}
                }
            }
        ]).next()['maxQuantity'] + 1
