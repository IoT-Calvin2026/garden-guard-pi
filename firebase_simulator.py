import argparse
import os
import random
from datetime import datetime, timezone

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore


load_dotenv()


def initialize_firestore():
    service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if not service_account:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT must be set in .env")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(service_account))
    return firestore.client()


def generate_event():
    event_id = random.randint(1, 2_147_483_647)
    event = {
        "eventId": event_id,
        "createdAt": datetime.now(timezone.utc),
        "temp": random.randint(-10, 45),
        "nws_conditions": random.choice([
            "Clear",
            "Cloudy",
            "Rain",
            "Thunderstorms",
            "Sunny",
            "Fog",
        ]),
    }
    return event


def generate_soil_moisture(event_id):
    return {
        "id": random.randint(1, 2_147_483_647),
        "eventId": event_id,
        "type": random.choice(["Moisture", "Soil"]),
        "soilMoisture": random.randint(0, 100),
    }


def clear_collections(db):
    for collection_name in ("events", "soil_moisture", "motion"):
        for document in db.collection(collection_name).stream():
            document.reference.delete()
        print(f"Cleared {collection_name}")


def delete_documents(db, collection_name, count):
    documents = list(db.collection(collection_name).stream())
    oldest_first = sorted(
        documents,
        key=lambda document: document.create_time,
    )
    targets = oldest_first[:count]
    for document in targets:
        document.reference.delete()
        print(f"Deleted {collection_name}/{document.id}")
    print(f"Deleted {len(targets)} document(s) from {collection_name}")


def add_pair(db):
    event = generate_event()
    soil_moisture = generate_soil_moisture(event["eventId"])

    _, event_ref = db.collection("events").add(event)
    _, soil_ref = db.collection("soil_moisture").add(soil_moisture)
    print(f"Added events/{event_ref.id} and soil_moisture/{soil_ref.id}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate random Garden Guard Event and Soil Moisture data."
    )
    parser.add_argument("--clear", action="store_true", help="Clear both collections")
    parser.add_argument(
        "--create",
        type=int,
        help="Number of Event and Soil Moisture pairs to create",
    )
    parser.add_argument(
        "--delete",
        type=int,
        nargs="?",
        const=-1,
        help="Number of oldest documents to delete from each collection",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompts",
    )
    args = parser.parse_args()

    db = initialize_firestore()

    if args.clear:
        if not args.yes:
            print(
                "WARNING: This permanently deletes ALL documents from "
                "events, soil_moisture, and motion."
            )
            response = input("Type DELETE to continue: ").strip()
            if response != "DELETE":
                print("Clear cancelled.")
                return
        clear_collections(db)
        return

    if args.delete is not None:
        delete_count = args.delete
        if delete_count == -1:
            try:
                delete_count = int(
                    input("How many oldest documents do you want to delete from each collection? ").strip()
                )
            except ValueError:
                parser.error("Delete count must be an integer")
        if delete_count < 0:
            parser.error("--delete must be zero or greater")
        for collection_name in ("events", "soil_moisture"):
            delete_documents(db, collection_name, delete_count)
        return

    create_count = args.create
    if create_count is None:
        create_count = input("How many Event and Soil Moisture pairs do you want to create? ").strip()
        try:
            create_count = int(create_count)
        except ValueError:
            parser.error("Create count must be an integer")
    if create_count < 0:
        parser.error("Create count must be zero or greater")

    for _ in range(create_count):
        add_pair(db)


if __name__ == "__main__":
    main()
