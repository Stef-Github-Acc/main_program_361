import zmq
import json
import os
import time

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
    print("Choose how you want to add the book:")
    print("1. Manually enter book details")
    print("2. Look up book by ISBN (via BookInfo API)")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == '1':
        add_book_manually()
    elif choice == '2':
        add_book_via_api()


def add_book_manually():
    print("\n--- Manual Book Entry ---")
    isbn = input("Enter ISBN number (unique): ").strip()

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    publisher = input("Enter publisher: ").strip()
    publish_date = input("Enter publish date (YYYY-MM-DD): ").strip()
    user_note = input("Enter a note about the book: ").strip()
    location = input("Enter location in your in-home library: ").strip()

    print("Fetching author information...")
    author_info = fetch_author_info(author)

    print("Getting timestamp information...")
    time_info = fetch_time_info()

    print("Fetching book review...")
    review_info = fetch_book_review(isbn, title, author)

    books[isbn] = {
        "title": title,
        "author": author,
        "author_bio": author_info.get('bio', 'Unknown') if author_info else 'Unknown',
        "author_birth_date": author_info.get('birth_date', 'Unknown') if author_info else 'Unknown',
        "publisher": publisher,
        "publish_date": publish_date,
        "utc_time": time_info.get('utc_time', 'Unknown') if time_info else 'Unknown',
        "local_time": time_info.get('local_time', 'Unknown') if time_info else 'Unknown',
        "book_review": review_info.get('review', 'No review available') if review_info else 'No review available',
        "user_note": user_note,
        "location": location
    }

    print(f"Book '{title}' added successfully.")


def add_book_via_api():
    print("\n--- Add Book via ISBN Lookup ---")
    isbn = input("Enter ISBN number to look up: ").strip()

    book_info = fetch_book_info_from_api(isbn)

    print("\n--- Retrieved Book Information ---")
    print(f"Title: {book_info.get('title', 'N/A')}")
    print(f"Author: {book_info.get('author', 'N/A')}")
    print(f"Publisher: {book_info.get('publisher', 'N/A')}")
    print(f"Publish Date: {book_info.get('publish_date', 'N/A')}")
    print("\n(Author birth information, timestamps, and book review will be fetched from microservices)")

    confirm = input("\nIs this information correct? (Y/N): ").strip().upper()
    if confirm != 'Y':
        print("Book addition canceled.")
        return

    user_note = input("Enter a note about the book: ").strip()
    location = input("Enter location in your in-home library: ").strip()

    print("Fetching author information...")
    author_info = fetch_author_info(book_info.get('author', ''))

    print("Getting timestamp information...")
    time_info = fetch_time_info()

    print("Fetching book review...")
    review_info = fetch_book_review(isbn, book_info.get('title', ''), book_info.get('author', ''))

    books[isbn] = {
        "title": book_info.get('title', ''),
        "author": book_info.get('author', ''),
        "author_bio": author_info.get('bio', 'Unknown') if author_info else 'Unknown',
        "author_birth_date": author_info.get('birth_date', 'Unknown') if author_info else 'Unknown',
        "publisher": book_info.get('publisher', ''),
        "publish_date": book_info.get('publish_date', ''),
        "utc_time": time_info.get('utc_time', 'Unknown') if time_info else 'Unknown',
        "local_time": time_info.get('local_time', 'Unknown') if time_info else 'Unknown',
        "book_review": review_info.get('review', 'No review available') if review_info else 'No review available',
        "user_note": user_note,
        "location": location
    }

    print(f"Book '{book_info.get('title', 'Unknown')}' added successfully.")


def fetch_author_info(author_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://localhost:5556")
    
    request = {
        "api_type": "AUTHOR_INFO",
        "request": {
            "author": author_name
        }
    }

    socket.send_string(json.dumps(request))

    response = socket.recv_string()
    author_data = json.loads(response)

    socket.close()
    context.term()

    if author_data.get("status") == "success":
        return author_data.get("author_info")
    else:
        return None


def fetch_time_info():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://localhost:5557")

    request = {
        "api_type": "TIME_INFO"
    }
    

    socket.send_string(json.dumps(request))

    response = socket.recv_string()
    time_data = json.loads(response)

    socket.close()
    context.term()

    if time_data.get("status") == "success":
        return time_data.get("time_info")
    else:
        return None


def fetch_book_review(isbn, title, author):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://localhost:5558")

    request = {
        "api_type": "BOOK_REVIEW_INFO",
        "request": {
            "title": title,
            "author": author
        }
    }

    socket.send_string(json.dumps(request))

    response = socket.recv_string()
    review_data = json.loads(response)

    socket.close()
    context.term()

    if review_data.get("status") == "success":
        return review_data.get("response")
    else:
        return None

def fetch_book_info_from_api(isbn):
    if os.path.exists('response.txt'):
        open('response.txt', 'w').close()

    with open('request.txt', 'w') as f:
        f.write(isbn)

    print("Request sent to BookInfo service, waiting for response...")

    timeout = 30
    elapsed = 0

    while elapsed < timeout:
        if os.path.exists('response.txt') and os.path.getsize('response.txt') > 0:
            with open('response.txt', 'r') as f:
                response_data = f.read().strip()

            if response_data:
                book_data = json.loads(response_data)

                if book_data.get("title") != "Not Found":
                    return book_data
                else:
                    return None

        time.sleep(5)
        elapsed += 5
        print(f"Still waiting for response... ({elapsed}s)")

    return None

def update_book():
    print("\n--- Update a Book ---")
    isbn = input("Enter ISBN of the book to update: ").strip()

    book = books[isbn]
    print("Leave a field blank to keep the current value.\n")

    editable_fields = ["title", "author", "publisher", "publish_date", "user_note", "location"]

    for key in editable_fields:
        if key in book:
            current_value = book[key]
            new_value = input(f"{key.replace('_', ' ').capitalize()} [{current_value}]: ").strip()
            if new_value:
                book[key] = new_value

    print("Book updated successfully.")
    print(
        "\nNote: Author birth information, timestamps, and book reviews cannot be updated as they are managed by microservices.")


def delete_book():
    print("\n--- Delete a Book ---")
    isbn = input("Enter ISBN of the book to delete: ").strip()

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


def help_menu():
    print("\nHelp Menu:")
    print("1 - Add a new book to the system (manually or via ISBN lookup).")
    print("2 - Update an existing book's details.")
    print("3 - Delete a book from the system.")
    print("4 - Show this help menu.")
    print("5 - Exit the program.")
    print("6 - List all books with viewing options.")


def main():
    first_run = True
    while True:
        if first_run:
            print("\nWelcome to the Home Library Book Management App! Catalog your books with details and in-home locations,")
            print("so you can easily check what you own and where to find it.")
            first_run = False

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


if __name__ == "__main__":
    main()