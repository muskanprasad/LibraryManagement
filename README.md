# Library Management System

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

## Object-Oriented Principles

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

## Data Persistence
The system uses three JSON files to store data persistently:

### books.json: 
Stores a list of dictionaries, where each dictionary represents a Book object.

### members.json: 
Stores a dictionary with two keys: "students" and "faculty". Each key maps to a list of dictionaries, representing Student and Faculty objects respectively. This provides clear separation of member types in the persistent storage.

### issued_books.json: 
Stores a dictionary where keys are member IDs (as strings for JSON compatibility) and values are lists of ISBNs of books issued to that member.

Data is loaded automatically when the LibrarySystem is initialized and saved after every significant operation (adding/updating books/members, issuing/returning books).


---
## Example Usage

### Library Management System
![1](https://github.com/user-attachments/assets/1e2476bd-72bf-4815-88ea-aded3d489729)

### Book Management Options 
![2](https://github.com/user-attachments/assets/ef5e9659-2414-43e3-917c-efb786bddc81)

### Member Management Options
![3](https://github.com/user-attachments/assets/3f5f24a9-dc15-4b63-af6c-24d0f29bb963)

### Issue/Return Books Options 
![4](https://github.com/user-attachments/assets/54d9dd56-0405-4689-bdeb-9eefd5046494)

### Exit 
![5](https://github.com/user-attachments/assets/09b2fe3b-e111-4ab6-800b-83cd5f682d5e)

### Viewing Available Books
![6](https://github.com/user-attachments/assets/087699bc-0643-4654-a171-9a31ea9ad7ab)

### Viewing all Members
![7](https://github.com/user-attachments/assets/33d80af5-4ce7-4c08-a0d6-630f4a89c815)

### Issuing a Book
![8](https://github.com/user-attachments/assets/5b0b9998-243f-4b76-b6ab-367ccb6162dd)
