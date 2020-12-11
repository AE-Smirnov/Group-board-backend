from dbmanager import DbManager
from message import Message


def list_returner(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if result:
            return result
        else:
            return [dict()]
    return wrapper


class Messenger:
    def __init__(self, messages_count=20):
        self.messages_count = messages_count
        self.message_manager = DbManager()

    def add_message(self, message):
        self.message_manager.add(message)

    @list_returner
    def get_room_messages(self):
        messages = []
        i = 6
        found_messages = []
        for message in self.message_manager.find({}, self.messages_count):
            found_messages.append(Message(**message))
        for message in sorted(found_messages):
            message_dict = message.as_dict()
            message_dict['id'] = i
            messages.append(message_dict)
            i += 1
        return messages

    def read_messages(self):
        output = list()
        messages = self.get_room_messages()
        output.append('[' + ', '.join([str(message).replace("'", '"') for message in messages]) + ']')
        return output

    def delete_message(self, message):
        try:
            self.message_manager.delete(message)
        except:
            print('No message')

    def update_message(self, old_message, message):
        self.message_manager.update(old_message, message)
