from database import initialize_db
from models.library import Library

def print_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. Register Member")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Search Book")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. Exit")

def main():
    initialize_db()
    library = Library()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            quantity = int(input("Quantity: "))
            library.add_book(title, author, isbn, quantity)

        elif choice == "2":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            library.register_member(name, email, phone)

        elif choice == "3":
            book_id = int(input("Book ID: "))
            member_id = int(input("Member ID: "))
            library.issue_book(book_id, member_id)

        elif choice == "4":
            txn_id = int(input("Transaction ID: "))
            library.return_book(txn_id)

        elif choice == "5":
            keyword = input("Search (title/author): ")
            library.search_book(keyword)

        elif choice == "6":
            library.view_all_books()

        elif choice == "7":
            library.view_all_members()

        elif choice == "8":
            library.overdue_report()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()