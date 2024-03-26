import json
import random
import uuid

import boto3

sqs_client = boto3.client("sqs")
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/403526594903/airbnb-booking-data-sqs"


def airbnb_booking_data():
    cities = ["Canberra", "Los Angeles", "Thimphu", "Delhi", "Tokyo"]
    
    countries = ["Australia", "USA", "Bhutan", "India", "Japan"]
    city = random.choice(cities)
    country = countries[cities.index(city)]
    
    start_date = ["2023-02-01","2023-02-02","2023-02-03","2023-02-04","2023-02-05"]
    
    end_date = ["2023-02-02","2023-02-03","2023-02-04","2023-02-05","2023-02-06"]



    return {
        "booking_id": str(uuid.uuid4()),
        "user_id": random.randint(100, 999),
        "property_id": random.randint(1, 100),
        "location": f"{city},{country}",
        "start_date": random.choice(start_date),
        "end_date": random.choice(end_date),
        "price": f"{round(random.uniform(10.0, 500.0), 2)}",
    }


def lambda_handler(event, context):
    i = 0
    while i < 50:
        booking_data = airbnb_booking_data()
        print(booking_data)
        json_booking_data = json.dumps(booking_data)
        sqs_client.send_message(QueueUrl=QUEUE_URL, MessageBody=json_booking_data)
        i += 1
    return {
        "statusCode": 200,
        "body": json.dumps("Airbnb booking data published to SQS!"),
    }
