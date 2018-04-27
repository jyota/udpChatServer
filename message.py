class ChatMessage(object):
    def __init__(self, sender_id, recipient_id, message):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message = message

    def get_dict(self):
        return {'sender_id': self.sender_id, 'recipient_id': self.recipient_id, 'message': self.message}


