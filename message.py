class Message:
    def __init__(self, role, content):
        if role is None or content is None:
            raise ValueError("role and content cannot be None")

        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }