from queue import Queue
from collections import defaultdict
from message import ChatMessage

# simple in-memory database for this project.
class SimpleDb(object):
    def __init__(self, user_cache_size=10):
        self.username_lookup = dict()
        self.username_cnt = 0
        self.user_messages = defaultdict(lambda: Queue(maxsize=user_cache_size))

    def get_user_id_from_username(self, username):
        for user_id, user_info in self.username_lookup.items():
            if username == user_info.get('username'):
                return {'status': 'ok', 'value': user_id}
        return {'status': 'error', 'status_msg': 'User not found'}

    def register_user(self, username, ip_address):
        for user_id, user_info in self.username_lookup.items():
            if username == user_info.get('username'):
                return {'status': 'error', 'status_msg': 'User already exists'}
        self.username_lookup[self.username_cnt] = {'username': username, 'ip': ip_address}
        self.username_cnt += 1
        return {'status': 'ok', 'value': self.username_cnt - 1} 

    def get_user_list(self):
        return [item.get('username') for item in self.username_lookup.values()]

    def assign_message_to_user_id(self, sending_user_id, user_id, message):
        if user_id not in self.username_lookup:
            return {'status': 'error', 'status_msg': 'User does not exist'}
        elif self.user_messages[user_id].full():
            return {'status': 'error', 'status_msg': 'User message queue is full'}
        else:
            self.user_messages[user_id].put(ChatMessage(sending_user_id, user_id, message))
            return {'status': 'ok', 'status_msg': 'assigned'}

    def get_message_for_user_id(self, user_id):
        if user_id not in self.username_lookup:
            return {'status': 'error', 'status_msg': 'User does not exist, please register'}
        elif self.user_messages[user_id].empty():
            return {'status': 'ok', 'status_msg': 'no messages'}
        else:
            return {'status': 'ok', 'value': self.user_messages[user_id].get()}
 
