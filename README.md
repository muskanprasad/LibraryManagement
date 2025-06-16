# Library Management System (Python)

A console-based Library Management System developed in Python, demonstrating **Object-Oriented Programming (OOP)** principles like **encapsulation**, **inheritance**, and **polymorphism**. It supports book and member management, book issuance, returns, and uses **JSON files** for persistent data storage.

---

## Features

### Book Management
- Add new books (handles existing ISBNs by updating quantity)
- View all books in the library
- Search for books by title, author, or ISBN

### Member Management
- Add new members (Students and Faculty)
- View all registered members with details and borrowed books

### Issue/Return Books
- Issue books to members (checks availability and limits)
- Return books from members

### Data Persistence
- All data is stored in `books.json`, `members.json`, and `issued_books.json`
- Data is loaded/saved automatically after relevant operations

### User-Friendly Interface
- Menu-driven CLI for easy interaction

---

## Object-Oriented Design

### `Book`
- Represents a single book
- **Encapsulation:** `_title`, `_author`, `_isbn`, `_total_quantity`, `_available_quantity`
- **Serialization:** `to_dict()` and `from_dict()`

### `Member` (Abstract Base Class)
- Base for `Student` and `Faculty`
- **Attributes:** `_member_id`, `_name`
- **Polymorphism:** `get_max_books_allowed()` (overridden)
- **Serialization:** `to_dict()` with class name

### `Student` (Inherits Member)
- Adds `_student_id`
- Borrow limit: 3 books

### `Faculty` (Inherits Member)
- Adds `_department`
- Borrow limit: 10 books

### `LibrarySystem`
- Manages `_books`, `_members`, `_issued_books`
- Loads/saves data from JSON
- Handles operations: `add_book()`, `issue_book()`, `return_book()`, etc.
- Provides menu-driven CLI interface (`run()` method)

---

## 'Data Persistence'
The system uses three JSON files to store data persistently:

### 'books.json': Stores a list of dictionaries, where each dictionary represents a Book object.

### 'members.json': Stores a dictionary with two keys: "students" and "faculty". Each key maps to a list of dictionaries, representing Student and Faculty objects respectively. This provides clear separation of member types in the persistent storage.

### 'issued_books.json': Stores a dictionary where keys are member IDs (as strings for JSON compatibility) and values are lists of ISBNs of books issued to that member.

Data is loaded automatically when the LibrarySystem is initialized and saved after every significant operation (adding/updating books/members, issuing/returning books).
---
## 'Example Usage'
