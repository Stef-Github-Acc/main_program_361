import requests
import json
import time
import os


def get_book_info(isbn):
    clean_isbn = isbn.strip().replace('-', '').replace(' ', '')
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{clean_isbn}&format=json&jscmd=data"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        book_key = f"ISBN:{clean_isbn}"
        if book_key in data:
            book = data[book_key]
            return {
                "title": book.get('title', 'Unknown'),
                "author": ', '.join([author.get('name', '') for author in book.get('authors', [])]) or 'Unknown',
                "publisher": ', '.join([pub.get('name', '') for pub in book.get('publishers', [])]) or 'Unknown',
                "publish_date": book.get('publish_date', 'Unknown'),
                "isbn": clean_isbn
            }
    except Exception as e:
        print(f"Error fetching book info: {e}")

    return None


def process_request():
    if not os.path.exists('request.txt'):
        return

    try:
        with open('request.txt', 'r') as f:
            isbn = f.read().strip()

        if not isbn:
            return

        open('request.txt', 'w').close()

        print(f"Processing ISBN: {isbn}")
        book_info = get_book_info(isbn)

        if book_info:
            with open('response.txt', 'w') as f:
                json.dump(book_info, f, indent=2)
            print(f"Book info written to response.txt: {book_info['title']}")
        else:
            error_response = {
                "title": "Not Found",
                "author": "Unknown",
                "publisher": "Unknown",
                "publish_date": "Unknown",
                "isbn": isbn
            }
            with open('response.txt', 'w') as f:
                json.dump(error_response, f, indent=2)
            print(f"Book not found for ISBN: {isbn}")

    except Exception as e:
        print(f"Error processing request: {e}")


def main():
    print("BookInfo microservice started. Checking for requests every 5 seconds...")
    print("Waiting for ISBN numbers in request.txt...")

    while True:
        try:
            process_request()
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nBookInfo service stopped.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()