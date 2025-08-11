import zmq
import random
import json


def get_book_review(request_data):

    request = request_data.get("request", {})
    request_id = request.get("id", "req-1")
    title = request.get("title", "")
    author = request.get("author", "")
    print(f"Generating book review for - Title: {title}, Author: {author}")

    templates = [
        f"'{title}' by {author} is a compelling read that showcases the author's distinctive voice. The narrative is well-crafted and engaging, making it a worthwhile addition to any reader's collection.",
        f"{author}'s work in '{title}' demonstrates remarkable storytelling ability. The book offers thoughtful insights and maintains reader interest throughout.",
        f"This book presents {author}'s unique perspective in an accessible and engaging manner. '{title}' is recommended for readers interested in quality literature.",
        f"'{title}' is a solid work by {author} that delivers on its promises. The writing is clear and the subject matter is handled with care and expertise.",
        f"A well-executed book by {author}. '{title}' combines good storytelling with meaningful content, making it an enjoyable read for its target audience.",
        f"In '{title}', {author} creates an engaging narrative that captivates readers from start to finish. The author's skill in character development and plot construction is evident throughout.",
        f"{author} delivers a thoughtful and well-researched work in '{title}'. The book provides valuable insights and is written in an accessible style that appeals to a broad audience."
    ]

    review_text = random.choice(templates)

    return {
        "status": "success",
        "response": {
            "id": request_id,
            "review": review_text
        }
    }


if __name__ == "__main__":
    result = {}
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")
    print("BookReviewInfo Microservice is running on port 5558...")

    while True:
        message = socket.recv_json()
        print(f"Received request:\n{json.dumps(message, indent=2)}")

        result = get_book_review(message)

        print(f"Sending response:\n{json.dumps(result, indent=2)}")
        socket.send_json(result)