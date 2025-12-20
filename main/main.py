import streamlit as st

import json as js 
from datetime import datetime, timedelta
st.title["Library Management "]
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



class Library:
    DATA_FILE = "library_data.json"

    def __init__(self):
        self.books = {}
        self.borrow_records = []
        self.load_data()

    def save_data(self):
        data = {
            "books": {bid: b.to_dict() for bid, b in self.books.items()},
            "borrow_records": self.borrow_records
        }
        with open(self.DATA_FILE, "w") as f:
            js.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as f:
                data = js.load(f)
                self.books = {bid: Book.from_dict(b) for bid, b in data["books"].items()}
                self.borrow_records = data["borrow_records"]
        except FileNotFoundError:
            pass

    def add_book(self, book):
        self.books[book.book_id] = book
        self.save_data()
        print("\nBook added successfully!\n")

    def search_by_title(self, title):
        print("\n--- Search Results (Title) ---")
        found = False
        for book in self.books.values():
            if title.lower() in book.title.lower():
                print(book)
                found = True
        if not found:
            print("No book found with this title.")
        print()

    def search_by_author(self, author):
        print("\n--- Search Results (Author) ---")
        found = False
        for book in self.books.values():
            if author.lower() in book.author.lower():
                print(book)
                found = True
        if not found:
            print("No book found with this author.")
        print()

    def search_by_category(self, category):
        print("\n--- Search Results (Category) ---")
        found = False
        for book in self.books.values():
            if category.lower() in book.category.lower():
                print(book)
                found = True
        if not found:
            print("No books found in this category.")
        print()

    # -------- ADVANCED: BORROW + DUE DATE --------
    def borrow_book(self, user, book_id):
        if book_id not in self.books:
            print("\nInvalid Book ID.\n")
            return

        book = self.books[book_id]
        if book.available_copies <= 0:
            print("\nSorry! This book is not available.\n")
            return

        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        book.available_copies -= 1

        self.borrow_records.append({
            "user": user,
            "book_id": book_id,
            "book_title": book.title,
            "borrow_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date
        })

        self.save_data()
        print(f"\nBook borrowed successfully! Return by: {due_date}\n")
    def return_book(self, book_id, user_name):
        # find record
        record = None
        for r in self.borrow_records:
            if r["book_id"] == book_id and r["user"] == user_name:
                record = r
                break

        if not record:
            print("\nNo matching borrow record found.\n")
            return

        book = self.books[book_id]

        # Calculate fine
        due_date = datetime.strptime(record["due_date"], "%Y-%m-%d")
        today = datetime.now()
        fine = 0

        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * 10  # Rs. 10 per day
            print(f"\nBook returned late by {days_late} days. Fine = Rs. {fine}")
        else:
            print("\nBook returned on time. No fine!")

        # update copies
        book.available_copies += 1

        # remove record
        self.borrow_records.remove(record)
        self.save_data()

    # -------- VIEW --------
    def view_books(self):
        print("\n--- All Library Books ---")
        for b in self.books.values():
            print(b)
        print()

    def view_records(self):
        print("\n--- Borrow Records ---")
        for r in self.borrow_records:
            print(f"{r['user']} borrowed '{r['book_title']}' | Due: {r['due_date']}")

        

class Admin:
    USERNAME = "admin"
    PASSWORD = "1234"

    @staticmethod
    def login():
        print("\n------ Admin Login ------")
        u = input("Enter Username: ")
        p = input("Enter Password: ")

        if u == Admin.USERNAME and p == Admin.PASSWORD:
            print("\nLogin Successful!\n")
            return True
        else:
            print("\nInvalid Credentials!\n")
            return False



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


class Admin:
    USERNAME = "admin"
    PASSWORD = "1234"

    @staticmethod
    def login():
        print("\n------ Admin Login ------")
        u = input("Enter Username: ")
        p = input("Enter Password: ")

        if u == Admin.USERNAME and p == Admin.PASSWORD:
            print("\nLogin Successful!\n")
            return True
        else:
            print("\nInvalid Credentials!\n")
            return False



library = Library()

while True:
        
        print("1. Admin Login")
        print("2. Search Book by Title")
        print("3. Search Book by Author")
        print("4. Search Book by Category")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. View All Books")
        print("8. View Borrow Records")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            if Admin .login():
               
                while True:
               
                    print("1. Add Book")
                    print("2. View All Books")
                    print("3. Exit Admin")

                    c = input("Enter choice: ")
                    if c == "1":
                        title = input("Book Title: ")
                        author = input("Author: ")
                        book_id = input("Book ID: ")
                        category = input("Category: ")
                        copies = int(input("Total Copies: "))
                        book = Book({title}, {author}, {book_id}, {category}, {copies})
                        library.add_book(book)
                    elif c == "2":
                        library.view_books()
                    elif c == "3":
                        break
                    else:
                        print("Invalid choice.")
    
        elif choice == "2":
            d = input("Enter choice: ")
            if d =="1" :
                library.search_by_title(input("Enter title: "))
            elif d == "2":
                library.search_by_author(input("Enter author: "))
            elif d =="3":
                library.search_by_category(input("Enter category: "))
            

        elif choice == "4":
            user = input("Your Name: ")
            book_id = input("Book ID: ")
            library.borrow_book(user, book_id)

        elif choice == "5":
            user = input("Your Name: ")
            book_id = input("Book ID: ")
            library.return_book(book_id, user)

        elif choice == "6":
            library.view_books()

        elif choice == "7":
            library.view_records()

        elif choice == "8":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option: \n")
