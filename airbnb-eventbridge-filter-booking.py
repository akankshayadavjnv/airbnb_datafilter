import json
from datetime import datetime
def lambda_handler(event,context):
    try:
        print("event = " , event)
        filtered_records = []
        for record in event:
            message = record["body"]
            print(f"message = {message} ")
            st_date = message["start_date"]
            ed_date = message["end_date"]
            start_date = datetime.strptime(st_date,"%Y-%m-%d")
            end_date = datetime.strptime(ed_date,"%Y-%m-%d")
            duration = (end_date - start_date).days
            if duration > 1:
                filtered_records.append(message)
            
        print(f"filtered_records = {filtered_records}")
        if len(filtered_records) == 0:
            return {}

        return filtered_records
    except Exception as e:
        print(f"error = {e}")
        return {
            "Error message": str(e)
            
        }
        
