import streamlit as st
import json
from datetime import datetime, timedelta

# ------------------ BOOK CLASS ------------------
class Book:
    def __init__(self, title, author, book_id, category, total_copies, available_copies=None):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.category = category
        self.total_copies = total_copies
        self.available_copies = available_copies if available_copies is not None else total_copies

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Book(**data)


# ------------------ LIBRARY CLASS ------------------
class Library:
    DATA_FILE = "library_data.json"

    def __init__(self):
        self.books = {}
        self.borrow_records = []
        self.load_data()

    def save_data(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump({
                "books": {bid: b.to_dict() for bid, b in self.books.items()},
                "borrow_records": self.borrow_records
            }, f, indent=4)

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = {bid: Book.from_dict(b) for bid, b in data["books"].items()}
                self.borrow_records = data["borrow_records"]
        except FileNotFoundError:
            pass

    def add_book(self, book):
        self.books[book.book_id] = book
        self.save_data()

    def borrow_book(self, user, book_id):
        if book_id not in self.books:
            return "Invalid Book ID"

        book = self.books[book_id]
        if book.available_copies <= 0:
            return "Book not available"

        book.available_copies -= 1
        self.borrow_records.append({
            "user": user,
            "book_id": book_id,
            "book_title": book.title,
            "borrow_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        })
        self.save_data()
        return "Book borrowed successfully"

    def return_book(self, user, book_id):
        for r in self.borrow_records:
            if r["user"] == user and r["book_id"] == book_id:
                due = datetime.strptime(r["due_date"], "%Y-%m-%d")
                fine = max(0, (datetime.now() - due).days * 10)
                self.books[book_id].available_copies += 1
                self.borrow_records.remove(r)
                self.save_data()
                return fine
        return None


library = Library()

# ------------------ STREAMLIT UI ------------------
st.set_page_config(page_title="Library Management", layout="wide")
st.title("📚 Library Management System")

menu = st.sidebar.radio(
    "Menu",
    ["Admin", "Search Books", "Borrow Book", "Return Book", "View Records"]
)

# ------------------ ADMIN ------------------
if menu == "Admin":

    # ------------------ LOGIN PAGE ------------------
    if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

     if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.admin_logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")
else:
    st.success("Welcome Admin!")
    # ------------------ ADMIN DASHBOARD PAGE ------------------
    else:
        st.subheader("🛠️ Admin Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ➕ Add Book")
            title = st.text_input("Title")
            author = st.text_input("Author")
            book_id = st.text_input("Book ID")
            category = st.text_input("Category")
            copies = st.number_input("Total Copies", min_value=1)

            if st.button("Add Book"):
                if not title or not author or not book_id:
                    st.error("Please fill all required fields")
                elif book_id in library.books:
                    st.error("Book ID already exists")
                else:
                    book = Book(title, author, book_id, category, copies)
                    library.add_book(book)
                    st.success("Book Added Successfully")

        with col2:
            st.markdown("### 📚 Library Stats")
            st.write(f"📘 Total Books: {len(library.books)}")
            st.write(f"📄 Borrowed Books: {len(library.borrow_records)}")

            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()

# ------------------ SEARCH ------------------
elif menu == "Search Books":
    st.subheader("🔍 Search Books")
    search_type = st.selectbox("Search By", ["Title", "Author", "Category"])
    query = st.text_input("Search")

    if query:
        for book in library.books.values():
            if query.lower() in getattr(book, search_type.lower()).lower():
                st.write(
                    f"📖 **{book.title}** | {book.author} | {book.category} | "
                    f"Available: {book.available_copies}/{book.total_copies}"
                )

# ------------------ BORROW ------------------
elif menu == "Borrow Book":
    st.subheader("📥 Borrow Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")

    if st.button("Borrow"):
        result = library.borrow_book(user, book_id)
        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)

# ------------------ RETURN ------------------
elif menu == "Return Book":
    st.subheader("📤 Return Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")

    if st.button("Return"):
        fine = library.return_book(user, book_id)
        if fine is None:
            st.error("Record not found")
        elif fine > 0:
            st.warning(f"Returned late. Fine: Rs {fine}")
        else:
            st.success("Returned on time. No fine!")

# ------------------ RECORDS ------------------
elif menu == "View Records":
    st.subheader("📄 Borrow Records")
    for r in library.borrow_records:
        st.write(
            f"👤 {r['user']} | 📘 {r['book_title']} | Due: {r['due_date']}"
        )

