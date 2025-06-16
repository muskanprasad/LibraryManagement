import json
import os

BOOKS_FILE = 'books.json'
MEMBERS_FILE = 'members.json'
ISSUED_BOOKS_FILE = 'issued_books.json'

class Book:
    # Encapsulation
    def __init__(self, title, author, isbn, quantity):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title cannot be empty.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Book author cannot be empty.")
        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError("Book ISBN cannot be empty.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Book quantity must be a positive integer.")

        self._title = title.strip()
        self._author = author.strip()
        self._isbn = isbn.strip()
        self._total_quantity = quantity
        self._available_quantity = quantity

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_isbn(self):
        return self._isbn

    def get_total_quantity(self):
        return self._total_quantity

    def get_available_quantity(self):
        return self._available_quantity

    def set_available_quantity(self, quantity):
        if not isinstance(quantity, int) or quantity < 0 or quantity > self._total_quantity:
            raise ValueError("Available quantity must be non-negative and not exceed total quantity.")
        self._available_quantity = quantity

    def increment_available_quantity(self):
        if self._available_quantity < self._total_quantity:
            self._available_quantity += 1
            return True
        return False

    def decrement_available_quantity(self):
        if self._available_quantity > 0:
            self._available_quantity -= 1
            return True
        return False

    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "total_quantity": self._total_quantity,
            "available_quantity": self._available_quantity
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(
            data['title'],
            data['author'],
            data['isbn'],
            data['total_quantity']
        )
        book.set_available_quantity(data['available_quantity'])
        return book

    def __str__(self):
        return (f"Title: {self._title}, Author: {self._author}, ISBN: {self._isbn}, "
                f"Available: {self._available_quantity}/{self._total_quantity}")

class Member:
    _next_id = 1001

    def __init__(self, name, member_id=None):
        # Encapsulation: Attributes initialized and managed within the class.
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name cannot be empty.")
        self._name = name.strip()
        if member_id is None:
            self._member_id = Member._next_id
            Member._next_id += 1
        else:
            if not isinstance(member_id, int) or member_id <= 0:
                raise ValueError("Member ID must be a positive integer.")
            self._member_id = member_id
            if member_id >= Member._next_id:
                Member._next_id = member_id + 1

    def get_member_id(self):
        return self._member_id

    def get_name(self):
        return self._name

    def get_max_books_allowed(self):
        # Polymorphism
        # It forces derived classes to define their specific borrowing limit.
        raise NotImplementedError("Subclasses must implement get_max_books_allowed()")

    def to_dict(self):
        return {
            "member_id": self._member_id,
            "name": self._name,
            "type": self.__class__.__name__
        }

    def __str__(self):
        return f"Member ID: {self._member_id}, Name: {self._name}"

class Student(Member):
    # Inheritance: Student class inherits from Member, gaining its attributes and methods.
    def __init__(self, name, student_id, member_id=None):
        super().__init__(name, member_id) 
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        self._student_id = student_id.strip() # Encapsulation
        self._max_books_allowed = 3 # Encapsulation
    def get_student_id(self):
        return self._student_id

    def get_max_books_allowed(self):
        # Polymorphism
        return self._max_books_allowed

    def to_dict(self):
        data = super().to_dict()
        data["student_id"] = self._student_id
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['student_id'], data['member_id'])

    def __str__(self):
        return f"{super().__str__()}, Type: Student, Student ID: {self._student_id}, Max Books: {self._max_books_allowed}"

class Faculty(Member):
    # Inheritance: Faculty class also inherits from Member.
    def __init__(self, name, department, member_id=None):
        super().__init__(name, member_id)
        if not isinstance(department, str) or not department.strip():
            raise ValueError("Department cannot be empty.")
        self._department = department.strip() # Encapsulation
        self._max_books_allowed = 10 # Encapsulation

    def get_department(self):
        return self._department

    def get_max_books_allowed(self):
        # Polymorphism
            return self._max_books_allowed

    def to_dict(self):
        data = super().to_dict()
        data["department"] = self._department
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['department'], data['member_id'])

    def __str__(self):
        return f"{super().__str__()}, Type: Faculty, Department: {self._department}, Max Books: {self._max_books_allowed}"


class LibrarySystem:
    # Encapsulation: _books, _members, _issued_books are internal state, managed by the class's methods.
    def __init__(self):
        self._books = {}
        self._members = {}
        self._issued_books = {}
        self._load_data()

    def _load_data(self):
        if os.path.exists(BOOKS_FILE):
            try:
                with open(BOOKS_FILE, 'r') as f:
                    books_data = json.load(f)
                    for data in books_data:
                        try:
                            book = Book.from_dict(data)
                            self._books[book.get_isbn()] = book
                        except (ValueError, KeyError) as e:
                            print(f"Error loading book data: {data} - {e}")
            except json.JSONDecodeError:
                print(f"Warning: {BOOKS_FILE} is corrupted or empty. Starting with no books.")
            except Exception as e:
                print(f"An unexpected error occurred while loading {BOOKS_FILE}: {e}")

        if os.path.exists(MEMBERS_FILE):
            try:
                with open(MEMBERS_FILE, 'r') as f:
                    members_data_structured = json.load(f)
                    students_data = members_data_structured.get("students", [])
                    for data in students_data:
                        try:
                            member = Student.from_dict(data) # Polymorphism: Creates Student objects
                            self._members[member.get_member_id()] = member
                            if member.get_member_id() >= Member._next_id:
                                Member._next_id = member.get_member_id() + 1
                        except (ValueError, KeyError) as e:
                            print(f"Error loading student data: {data} - {e}")

                    faculty_data = members_data_structured.get("faculty", [])
                    for data in faculty_data:
                        try:
                            member = Faculty.from_dict(data) # Polymorphism: Creates Faculty objects
                            self._members[member.get_member_id()] = member
                            if member.get_member_id() >= Member._next_id:
                                Member._next_id = member.get_member_id() + 1
                        except (ValueError, KeyError) as e:
                            print(f"Error loading faculty data: {data} - {e}")

            except json.JSONDecodeError:
                print(f"Warning: {MEMBERS_FILE} is corrupted or empty. Starting with no members.")
            except Exception as e:
                print(f"An unexpected error occurred while loading {MEMBERS_FILE}: {e}")

        if os.path.exists(ISSUED_BOOKS_FILE):
            try:
                with open(ISSUED_BOOKS_FILE, 'r') as f:
                    self._issued_books = json.load(f)
                    self._issued_books = {int(k): v for k, v in self._issued_books.items()}
            except json.JSONDecodeError:
                print(f"Warning: {ISSUED_BOOKS_FILE} is corrupted or empty. Starting with no issued records.")
            except Exception as e:
                print(f"An unexpected error occurred while loading {ISSUED_BOOKS_FILE}: {e}")

    def _save_data(self):
        try:
            with open(BOOKS_FILE, 'w') as f:
                json.dump([book.to_dict() for book in self._books.values()], f, indent=4)
        except Exception as e:
            print(f"Error saving books data: {e}")

        try:
            students_to_save = []
            faculty_to_save = []
            for member in self._members.values():
                # Polymorphism: Checks the type of member at runtime to save them to the correct section.
                if isinstance(member, Student):
                    students_to_save.append(member.to_dict())
                elif isinstance(member, Faculty):
                    faculty_to_save.append(member.to_dict())

            members_data_structured = {
                "students": students_to_save,
                "faculty": faculty_to_save
            }

            with open(MEMBERS_FILE, 'w') as f:
                json.dump(members_data_structured, f, indent=4)
        except Exception as e:
            print(f"Error saving members data: {e}")

        try:
            with open(ISSUED_BOOKS_FILE, 'w') as f:
                json.dump({str(k): v for k, v in self._issued_books.items()}, f, indent=4)
        except Exception as e:
            print(f"Error saving issued books data: {e}")

    def add_book(self):
        print("\n--- Add New Book ---")
        while True:
            title = input("Enter book title: ").strip()
            if title:
                break
            print("Title cannot be empty. Please try again.")

        while True:
            author = input("Enter book author: ").strip()
            if author:
                break
            print("Author cannot be empty. Please try again.")

        while True:
            isbn = input("Enter book ISBN (e.g., 978-0321765723): ").strip()
            if not isbn:
                print("ISBN cannot be empty. Please try again.")
                continue
            if isbn in self._books:
                print(f"A book with ISBN '{isbn}' already exists. Updating its quantity.")
                existing_book = self._books[isbn]
                while True:
                    try:
                        add_qty = int(input(f"Current total quantity for '{existing_book.get_title()}': {existing_book.get_total_quantity()}. Enter additional quantity to add: "))
                        if add_qty > 0:
                            existing_book._total_quantity += add_qty
                            existing_book._available_quantity += add_qty
                            print(f"Quantity updated successfully for '{existing_book.get_title()}'. New total: {existing_book.get_total_quantity()}")
                            self._save_data()
                            return
                        else:
                            print("Additional quantity must be positive.")
                    except ValueError:
                        print("Invalid quantity. Please enter a number.")
            else:
                break

        while True:
            try:
                quantity = int(input("Enter total quantity: "))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a number for quantity.")

        try:
            new_book = Book(title, author, isbn, quantity)
            self._books[isbn] = new_book
            print(f"Book '{title}' (ISBN: {isbn}) added successfully.")
            self._save_data()
        except ValueError as e:
            print(f"Error adding book: {e}")

    def view_all_books(self):
        print("\n--- All Books in Library ---")
        if not self._books:
            print("No books available in the library.")
            return

        for book in self._books.values():
            print(book)
        print("-" * 30)

    def search_book(self):
        print("\n--- Search Book ---")
        if not self._books:
            print("No books available to search.")
            return

        search_term = input("Enter title, author, or ISBN to search: ").strip().lower()
        found_books = []
        for book in self._books.values():
            if (search_term in book.get_title().lower() or
                search_term in book.get_author().lower() or
                search_term == book.get_isbn().lower()):
                found_books.append(book)

        if found_books:
            print("\n--- Search Results ---")
            for book in found_books:
                print(book)
            print("-" * 30)
        else:
            print("No books found matching your search term.")

    def add_member(self):
        print("\n--- Add New Member ---")
        while True:
            member_type = input("Enter member type (Student/Faculty): ").strip().capitalize()
            if member_type in ["Student", "Faculty"]:
                break
            else:
                print("Invalid member type. Please enter 'Student' or 'Faculty'.")

        while True:
            name = input("Enter member name: ").strip()
            if name:
                break
            print("Name cannot be empty. Please try again.")

        new_member = None
        if member_type == "Student":
            while True:
                student_id = input("Enter student ID: ").strip()
                if student_id:
                    if any(isinstance(m, Student) and m.get_student_id() == student_id for m in self._members.values()):
                        print(f"A student with ID '{student_id}' already exists. Please use a unique ID.")
                    else:
                        try:
                            new_member = Student(name, student_id)
                            break
                        except ValueError as e:
                            print(f"Error creating student: {e}")
                else:
                    print("Student ID cannot be empty. Please try again.")
        elif member_type == "Faculty":
            while True:
                department = input("Enter department: ").strip()
                if department:
                    try:
                        new_member = Faculty(name, department)
                        break
                    except ValueError as e:
                        print(f"Error creating faculty member: {e}")
                else:
                    print("Department cannot be empty. Please try again.")

        if new_member:
            self._members[new_member.get_member_id()] = new_member
            print(f"{member_type} '{name}' (ID: {new_member.get_member_id()}) added successfully.")
            self._save_data()
        else:
            print("Failed to add member due to invalid input.")

    def view_all_members(self):
        print("\n--- All Members ---")
        if not self._members:
            print("No members registered in the system.")
            return

        for member in self._members.values():
            print(member)
            borrowed_isbns = self._issued_books.get(member.get_member_id())
            if borrowed_isbns:
                print("  Borrowed Books:")
                for i, isbn in enumerate(borrowed_isbns):
                    book = self._books.get(isbn)
                    if book:
                        print(f"    {i+1}. {book.get_title()} by {book.get_author()} (ISBN: {isbn})")
                    else:
                        print(f"    {i+1}. Unknown Book (ISBN: {isbn}) - Data might be missing.")
            else:
                print("  No books currently borrowed.")
            print("-" * 30)

    def issue_book(self):
        print("\n--- Issue Book ---")
        if not self._books:
            print("No books available to issue.")
            return
        if not self._members:
            print("No members registered to issue books to.")
            return

        while True:
            try:
                member_id = int(input("Enter Member ID: "))
                if member_id in self._members:
                    member = self._members[member_id]
                    break
                else:
                    print("Member not found. Please enter a valid Member ID.")
            except ValueError:
                print("Invalid Member ID. Please enter a number.")

        while True:
            isbn = input("Enter ISBN of the book to issue: ").strip()
            if isbn in self._books:
                book = self._books[isbn]
                break
            else:
                print("Book not found. Please enter a valid ISBN.")

        if book.get_available_quantity() <= 0:
            print(f"'{book.get_title()}' (ISBN: {isbn}) is currently out of stock.")
            return

        issued_by_member = self._issued_books.get(member_id, [])
        # Polymorphism
        if len(issued_by_member) >= member.get_max_books_allowed():
            print(f"{member.get_name()} (ID: {member_id}) has reached their borrowing limit ({member.get_max_books_allowed()} books).")
            return

        if book.decrement_available_quantity():
            issued_by_member.append(isbn)
            self._issued_books[member_id] = issued_by_member
            print(f"Book '{book.get_title()}' issued to {member.get_name()} (ID: {member_id}) successfully.")
            self._save_data()
        else:
            print("Failed to issue book. Unexpected error: Book not available.")

    def return_book(self):
        print("\n--- Return Book ---")
        if not self._issued_books:
            print("No books are currently issued.")
            return

        while True:
            try:
                member_id = int(input("Enter Member ID: "))
                if member_id in self._members:
                    member = self._members[member_id]
                    break
                else:
                    print("Member not found. Please enter a valid Member ID.")
            except ValueError:
                print("Invalid Member ID. Please enter a number.")

        issued_by_member = self._issued_books.get(member_id)
        if not issued_by_member:
            print(f"{member.get_name()} (ID: {member_id}) currently has no books issued.")
            return

        print(f"\nBooks issued to {member.get_name()} (ID: {member_id}):")
        for i, isbn in enumerate(issued_by_member):
            book = self._books.get(isbn)
            if book:
                print(f"{i+1}. {book.get_title()} (ISBN: {isbn})")
            else:
                print(f"{i+1}. Unknown Book (ISBN: {isbn}) - Data might be missing.")

        while True:
            isbn_to_return = input("Enter ISBN of the book to return: ").strip()
            if isbn_to_return in issued_by_member:
                break
            else:
                print("This book is not listed as issued to this member. Please enter a correct ISBN from the list above.")

        book = self._books.get(isbn_to_return)
        if not book:
            print(f"Error: Book with ISBN '{isbn_to_return}' not found in library inventory.")
            return

        if book.increment_available_quantity():
            issued_by_member.remove(isbn_to_return)
            if not issued_by_member:
                del self._issued_books[member_id]
            else:
                self._issued_books[member_id] = issued_by_member
            print(f"Book '{book.get_title()}' returned by {member.get_name()} (ID: {member_id}) successfully.")
            self._save_data()
        else:
            print("Failed to return book. Unexpected error: Book quantity already at max.")

    def display_main_menu(self):
        print("\n===== Library Management System =====")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Issue/Return Books")
        print("4. Exit")
        print("===================================")

    def display_book_menu(self):
        print("\n--- Book Management ---")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Back to Main Menu")
        print("-----------------------")

    def display_member_menu(self):
        print("\n--- Member Management ---")
        print("1. Add New Member")
        print("2. View All Members")
        print("3. Back to Main Menu")
        print("-------------------------")

    def display_issue_return_menu(self):
        print("\n--- Issue/Return Books ---")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Back to Main Menu")
        print("--------------------------")

    def run(self):
        while True:
            self.display_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                while True:
                    self.display_book_menu()
                    book_choice = input("Enter your choice: ").strip()
                    if book_choice == '1':
                        self.add_book()
                    elif book_choice == '2':
                        self.view_all_books()
                    elif book_choice == '3':
                        self.search_book()
                    elif book_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice == '2':
                while True:
                    self.display_member_menu()
                    member_choice = input("Enter your choice: ").strip()
                    if member_choice == '1':
                        self.add_member()
                    elif member_choice == '2':
                        self.view_all_members()
                    elif member_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice == '3':
                while True:
                    self.display_issue_return_menu()
                    issue_return_choice = input("Enter your choice: ").strip()
                    if issue_return_choice == '1':
                        self.issue_book()
                    elif issue_return_choice == '2':
                        self.return_book()
                    elif issue_return_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice == '4':
                print("Exiting Library Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    library = LibrarySystem()
    library.run()
