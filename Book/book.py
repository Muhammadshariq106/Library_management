import json 
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, book_id, category, total_copies, available_copies=None):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.category = category
        self.total_copies = total_copies
        self.available_copies = available_copies if available_copies is not None else total_copies

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "book_id": self.book_id,
            "category": self.category,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data["title"], data["author"], data["book_id"],
            data["category"], data["total_copies"], data["available_copies"]
        )

    def __str__(self):
        return f"{self.book_id} | {self.title} | {self.author} | {self.category} | Available: {self.available_copies}/{self.total_copies}"

