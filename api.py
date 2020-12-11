from message import Message
from messenger import Messenger
from dbmanager import DbManager


def get_messages(messenger):
    return messenger.read_messages()


def init_messenger():
    return Messenger()


def delete_message(messenger, message_json):
    message = Message(**message_json)
    messenger.delete_message(message)


def add_or_update_message(messenger, message_info):
    message = Message(**message_info)
    if not message.id:
        messenger.add_message(message)
    else:
        messenger.update_message(DbManager().find({'id': message.id})[0], message)
    message._id = None
    return message.as_dict()
