from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.cloud import secretmanager  
import os

# Only for manual testing of the container
#credential_path = "auth/application_default_credentials.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# initialize Connector object
connector = Connector()

#Initializesecret manager object
client = secretmanager.SecretManagerServiceClient()

# Function to access secrets
def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# function to return the database connection object
def getconn():
    conn = connector.connect(
        "etl-test-404717:europe-west3:course-app",
        "pymysql",
        user = access_secret("etl-test-404717","MYSQL_USER"),
        password = access_secret("etl-test-404717","MYSQL_PASSWORD"),
        db = access_secret("etl-test-404717","MYSQL_DB",version_id=3)
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html', title="Home Page")

@app.route('/list')
def show_list():
    """Renders a page with a list of all course enrollments.This is just for testing"""
    with pool.connect() as db_conn:
        query = sqlalchemy.text("SELECT * FROM course_enrollments")
        # The query must be executed inside the 'with' block, before the connection closes.
        database_values = db_conn.execute(query).fetchall()
    return render_template('list.html', list=database_values)

@app.route('/enrol', methods=['POST'])
def enrol():
    """Handles the course enrollment form submission."""
    if request.method == 'POST':
        course_date = request.form.get('course_date')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        comment = request.form.get('comment')
        
        # Insert statement using parameters to prevent SQL injection
        # Matches schema: id (autoincrement), enrollment_time (NOW), others nullable
        insert_stmt = sqlalchemy.text(
            """INSERT INTO course_enrollments (enrollment_time, course_date, first_name, last_name, email, comment)
               VALUES (NOW(), :course_date, :first_name, :last_name, :email, :comment)"""
        )
        
        try:
            with pool.connect() as db_conn:
                db_conn.execute(insert_stmt, parameters={
                    "course_date": course_date,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "comment": comment
                })
                db_conn.commit()
            
            submission_details = {"date": course_date, "first_name": first_name, "last_name": last_name, "email": email, "comment": comment if comment else "N/A"}
            return render_template('enrollment-confirmation.html', title="Enrollment Confirmation", submission_data=submission_details)
        
        except Exception as e:
            return render_template('error.html', title="Error", error_message="An unexpected error occurred."), 500

# This is essential for running the app directly from the script
if __name__ == '__main__':
    # debug=True is great for development as it enables the debugger and auto-reloads
    # For production, use a proper WSGI server like Gunicorn or uWSGI and set debug=False
    app.run(host='0.0.0.0', port=5000, debug=True)
    