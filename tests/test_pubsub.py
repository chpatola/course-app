# This works now, just to update into the real app!
from google.cloud import pubsub_v1
from datetime import datetime
import json

publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/etl-test-404717/topics/course-app-topic'

def publish_message(data):
    data = data.encode("utf-8")
    future = publisher.publish(topic_name, data)
    print(f"Published message ID: {future.result()}")
    
enrollment_time = datetime.now().astimezone().isoformat()
print(enrollment_time)
course_date = "2025-09-05"
first_name = "Eigteenth try"
last_name = "Time with new table"
email = "my_email@mail.com"
comment = "I want to get to BigQuery"
submission_details = {"enrollment_time": enrollment_time, "course_date": course_date, "first_name": first_name, "last_name": last_name, "email": email, "comment": comment if comment else "N/A"}

publish_message(json.dumps(submission_details))
print(submission_details)
