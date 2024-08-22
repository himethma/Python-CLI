# model.py

import datetime

class Book:
    def __init__(self, title: str, author: str, genre: str, date_added: str = None, 
                 date_read: str = None, status: int = 0, position: int = 0):
        self.title = title
        self.author = author
        self.genre = genre
        self.date_added = date_added if date_added else datetime.datetime.now().isoformat()
        self.date_read = date_read
        self.status = status  # 0 = not read, 1 = reading, 2 = read
        self.position = position

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.genre}', '{self.date_added}', '{self.date_read}', {self.status}, {self.position})"
