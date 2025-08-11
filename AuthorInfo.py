import zmq
import requests
import json
from urllib.parse import quote


def search_author_in_open_library(author_name):
    clean_name = author_name.strip()
    encoded_name = quote(clean_name)

    url = f"https://openlibrary.org/search/authors.json?q={encoded_name}"
    print(f"Search URL for author: {url}")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    docs = data.get('docs', [])

    for doc in docs:
        doc_name = doc.get('name', '').lower()
        search_name = clean_name.lower()

        if doc_name == search_name or search_name in doc_name:
            return doc.get('key')

    return None


def get_author_details(author_key):
    if not author_key:
        return None

    if not author_key.startswith('/authors/'):
        author_key = f"/authors/{author_key}"

    url = f"https://openlibrary.org{author_key}.json"
    
    print(f"Search URL for author key: {url}")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    birth_date = data.get('birth_date', '')
    bio = data.get('bio', '')

    return {
        'birth_date': birth_date,
        'bio': bio if isinstance(bio, str) else bio.get('value', '') if isinstance(bio, dict) else ''
    }


def get_author_info(request_data):
    request = request_data.get("request", {})
    request_id = request.get("id", "req-1")

    author_name = request.get("author", "")

    print(f"Searching for author: {author_name}")

    author_key = search_author_in_open_library(author_name)

    if not author_key:
        return {
            "api_type": "AUTHOR_INFO",
            "status": "error",
            "response": {
                "id": request_id,
                "error": f"Author '{author_name}' not found in Open Library"
            }
        }

    print(f"Found author key: {author_key}")

    author_details = get_author_details(author_key)

    if not author_details:
        return {
            "api_type": "AUTHOR_INFO",
            "status": "error",
            "response": {
                "id": request_id,
                "error": f"Could not retrieve details for author '{author_name}'"
            }
        }

    return {
        "api_type": "AUTHOR_INFO",
        "status": "success",
        "author_info": {
            "id": request_id,
            "birth_date": author_details.get('birth_date', 'Unknown'),
            "bio": author_details.get('bio', '')
        }
    }


if __name__ == "__main__":
    result = {}

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("AuthorInfo Microservice is running on port 5556...")

    while True:
        message = socket.recv_json()
        print(f"Received request:\n{json.dumps(message, indent=2)}")

        result = get_author_info(message)

        print(f"Sending response:\n{json.dumps(result, indent=2)}")
        socket.send_json(result)