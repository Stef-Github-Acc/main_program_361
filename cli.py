books = {}

def show_menu():
    print("\n=== Book Management CLI ===")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Delete Book")
    print("4. Help")
    print("5. Exit")
    print("6. List All Books")

def add_book():
    print("\n--- Add a New Book ---")
    isbn = input("Enter ISBN number (unique): ").strip()

    if isbn in books:
        print("A book with this ISBN already exists.")
        return

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    publisher = input("Enter publisher: ").strip()
    publish_date = input("Enter publish date (YYYY-MM-DD): ").strip()
    user_note = input("Enter a note about the book: ").strip()
    location = input("Enter location in your in-home library: ").strip()

    books[isbn] = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "publish_date": publish_date,
        "user_note": user_note,
        "location": location
    }

    print(f"Book '{title}' added successfully.")

def update_book():
    print("\n--- Update a Book ---")
    isbn = input("Enter ISBN of the book to update: ").strip()

    if isbn not in books:
        print("Book not found.")
        return

    book = books[isbn]
    print("Leave a field blank to keep the current value.\n")

    for key in book:
        current_value = book[key]
        new_value = input(f"{key.replace('_', ' ').capitalize()} [{current_value}]: ").strip()
        if new_value:
            book[key] = new_value

    print("Book updated successfully.")

def delete_book():
    print("\n--- Delete a Book ---")
    isbn = input("Enter ISBN of the book to delete: ").strip()

    if isbn not in books:
        print("Book not found.")
        return

    book = books[isbn]
    print(f"You're about to delete the book: {book['title']} by {book['author']}")
    confirm = input("This will erase all existing book data. CONFIRM DELETION? (Y/N): ").strip().upper()

    if confirm == 'Y':
        del books[isbn]
        print("Book deleted successfully.")
    else:
        print("Deletion canceled.")

def list_books():
    if not books:
        print("\nNo books stored yet.")
        return

    print("\nHow would you like to view the books?")
    print("1. Brief summaries (title, author, note)")
    print("2. Detailed info (all metadata)")
    print("3. Locations only (title, location)")

    option = input("Enter your choice (1-3): ").strip()

    if option == '1':
        print("\n--- Book Summaries ---")
        for book in books.values():
            print(f"- Title: {book['title']}")
            print(f"  Author: {book['author']}")
            print(f"  Note: {book['user_note']}\n")
    elif option == '2':
        print("\n--- Detailed Book Info ---")
        for isbn, book in books.items():
            print(f"- ISBN: {isbn}")
            for key, value in book.items():
                print(f"  {key.replace('_', ' ').capitalize()}: {value}")
            print()
    elif option == '3':
        print("\n--- Book Locations ---")
        for book in books.values():
            print(f"- Title: {book['title']}")
            print(f"  Location: {book['location']}\n")
    else:
        print("Invalid option. Returning to main menu.")

def help_menu():
    print("\nHelp Menu:")
    print("1 - Add a new book to the system.")
    print("2 - Update an existing book's details.")
    print("3 - Delete a book from the system.")
    print("4 - Show this help menu.")
    print("5 - Exit the program.")
    print("6 - List all books with viewing options.")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            help_menu()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        elif choice == '6':
            list_books()
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
