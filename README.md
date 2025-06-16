#Library Management System
This is a console-based Library Management System developed in Python, demonstrating Object-Oriented Programming (OOP) principles such as encapsulation, inheritance, and polymorphism. The system allows for managing books, library members (students and faculty), and tracking book issuance and returns. All data is persistently stored using JSON files.

##Features
###Book Management:

Add new books (including handling existing ISBNs to update quantity).

View all books in the library.

Search for books by title, author, or ISBN.

###Member Management:

Add new members, distinguishing between Students and Faculty.

View all registered members, with a detailed breakdown including books currently borrowed by each member.

###Issue/Return Books:

Issue books to members (checks for availability and member borrowing limits).

Return books from members.

###Data Persistence:

All book, member, and issue/return data is automatically saved to and loaded from JSON files (books.json, members.json, issued_books.json).

User-Friendly Interface:

Menu-driven interface for easy navigation and interaction.

