import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def get_file_name(start_date, end_date):
    # Format start and end dates as YYYY-MM-DD
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    # Generate file name
    file_name = f"{start_date_formatted}-{end_date_formatted}.json"
    return file_name

def lambda_handler(event, context):
    for record in event:
        print(f"record = {record}")
        start_date = record['start_date']
        end_date = record['end_date']
        file_name = get_file_name(start_date, end_date)
        print(f"file_name = {file_name}")
        try:
            # Check if file exists
            s3.head_object(Bucket='airbnb-booking-records-s3', Key=file_name)
            # If file exists, append event data to it
            existing_data = s3.get_object(Bucket='airbnb-booking-records-s3', Key=file_name)['Body'].read().decode('utf-8')
            events = json.loads(existing_data)
            events.append(record)
            print(f"events = {events}")
            updated_data = json.dumps(events)
            s3.put_object(Body=updated_data, Bucket='airbnb-booking-records-s3', Key=file_name)
        except:
            # If file does not exist, create new file and write event data to it
            events = [record]
            print(f"in exception new file events = {events}")
            json_data = json.dumps(events)
            s3.put_object(Body=json_data, Bucket='airbnb-booking-records-s3', Key=file_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Event data processed successfully!')
    }
