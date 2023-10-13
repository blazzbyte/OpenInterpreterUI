import json

class Conversation:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    def to_json(self):
        return json.dumps(self.to_dict())

class Chat:
    def __init__(self, conversation_id, role, content):
        self.conversation_id = conversation_id
        self.role = role
        self.content = content

    def to_dict(self):
        return {"conversation_id": self.conversation_id, "role": self.role, "content": self.content}

    def to_json(self):
        return json.dumps(self.to_dict())
