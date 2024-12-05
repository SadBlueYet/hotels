import json
from pprint import pprint
from models import Amenity


def create_messages(amenities: list[Amenity], img_url: str) -> list[dict]:
    prompt = json.dumps([amenity.model_dump() for amenity in amenities])

    messages = [
        {
            "role": "system",
            "content": "You are an assistant for analyzing photos of hotels.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Which of the sent amenities are shown in the photo? {prompt}",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": img_url},
                },
            ],
        },
    ]
    return messages


def main():
    ...


if __name__ == "__main__":
    main()
