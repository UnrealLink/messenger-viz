from datetime import datetime

class Message:
    def __init__(self, content : str, author : str, date : datetime):
        self.content = content
        self.author = author
        self.date = date
    
    def __repr__(self):
        return f"{self.date} - {self.author}: {self.content}"