import json
import logging
import sys

from openai import OpenAI, PermissionDeniedError

from config import settings
from models import Amenities, Amenity
from utils import load_json, write_to_json


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
                    "text": f"{prompt}\nWhich of the amenities described above are shown in the photo? Specify only those amenities that can be clearly identified.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": img_url},
                },
            ],
        },
    ]
    return messages


def filter_amenities(hotel: dict[str, any], amenities: list[dict]) -> list[Amenity]:
    new_amenities = []
    for hotel_amenities in hotel["content"]["ru_RU"]["c_amenity"]:
        new_amenities.append(
            [
                am
                for am in amenities
                if am["c_amenity_id"] == int(hotel_amenities["id"]["$numberLong"])
            ]
        )
    return [
        Amenity(**max(amenity, key=lambda x: x.get("c_amenity_group_priority") or 0))
        for amenity in new_amenities
    ]


class HotelAmenitiesDetector:
    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        self.client = OpenAI(api_key=settings.LLM.OPENAI_API_KEY)

    def analyze_image(self, messages: list[dict]) -> Amenities:
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model, messages=messages, response_format=Amenities
            )
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        return completion.choices[0].message.parsed


def main():
    detector = HotelAmenitiesDetector()
    all_amenities = load_json(settings.FILES_PATHS.JSON_AMENITIES_FILE_PATH)
    all_hotels = load_json(settings.FILES_PATHS.JSON_HOTELS_FILE_PATH)

    for hotel in all_hotels[:3]:
        hotel_to_json = {
            "name": hotel["content"]["ru_RU"]["name"],
            "amenities": [],
            "images": [],
        }
        fitered_amenities = filter_amenities(hotel, all_amenities)

        for images in hotel["images"][:4]:
            hotel_to_json["images"].append(images["orig"])
            messages = create_messages(fitered_amenities, images["orig"])
            amenities = detector.analyze_image(messages)

            for amenity in amenities.amenities:
                if amenity.model_dump() in hotel_to_json["amenities"]:
                    continue
                hotel_to_json["amenities"].append(amenity.model_dump())

            logging.info("The image has been successfully processed!")

        write_to_json(settings.FILES_PATHS.JSON_OUTPUT_FILE_PATH, hotel_to_json)


if __name__ == "__main__":
    main()
