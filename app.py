"""Module providing a access to local variables"""
import os
import json
from datetime import datetime
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
from google.cloud import secretmanager
from google.cloud import pubsub_v1
import sqlalchemy

# Only for manual testing of the container
#CREDENTIAL_PATH = "auth/application_default_credentials.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

# initialize Connector object
connector = Connector()

# Initialize secret manager object
client = secretmanager.SecretManagerServiceClient()

# Initialize pubsub publisher object
publisher = pubsub_v1.PublisherClient()

# Define Functions
def access_secret(project_id, secret_id, version_id=1):
    """Function to access secrets"""
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def publish_message(data):
    """Function to publish message to pubsub topic"""
    topic_name = 'projects/etl-test-404717/topics/course-app-topic'
    data = data.encode("utf-8")
    future = publisher.publish(topic_name, data)
    print(f"Published message ID: {future.result()}")
    
def getconn():
    """Function to return the database connection object"""
    conn = connector.connect(
        "etl-test-404717:europe-west3:course-app",
        "pymysql",
        user=access_secret("etl-test-404717", "MYSQL_USER"),
        password=access_secret("etl-test-404717", "MYSQL_PASSWORD"),
        db=access_secret("etl-test-404717", "MYSQL_DB", version_id=3),
    )
    return conn


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Initialize the Flask application
app = Flask(__name__)

# Define endpoints
@app.route("/")
def home():
    """Renders the home page."""
    return render_template("index.html", title="Home Page")

@app.route("/enrol", methods=["POST"])
def enrol():
    """Handles the course enrollment form submission."""
    if request.method == "POST":
        enrollment_time = datetime.now().astimezone().isoformat()
        course_date = request.form.get("course_date")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        comment = request.form.get("comment")

        insert_stmt = sqlalchemy.text(
            """INSERT INTO course_enrollments (enrollment_time, course_date, first_name, last_name, email, comment)
               VALUES (:enrollment_time, :course_date, :first_name, :last_name, :email, :comment)"""
        )

        try:
            with pool.connect() as db_conn:
                db_conn.execute(
                    insert_stmt,
                    parameters={
                        "enrollment_time": enrollment_time,
                        "course_date": course_date,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "comment": comment,
                    },
                )
                db_conn.commit()

            submission_details = {
                "enrollment_time": enrollment_time,
                "course_date": course_date,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "comment": comment if comment else "N/A",
            }
            publish_message(json.dumps(submission_details))
            return render_template(
                "enrollment-confirmation.html",
                title="Enrollment Confirmation",
                submission_data=submission_details,
            )

        except Exception as e:
            return render_template("error.html", title="Error", error_message=e), 500

# This is essential for running the app directly from the script
if __name__ == "__main__":
    # debug=True is great for development as it enables the debugger and auto-reloads
    # For production, use a proper WSGI server like Gunicorn or uWSGI and set debug=False
    app.run(host="0.0.0.0", port=5000, debug=True)
