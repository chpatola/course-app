from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import secretmanager
import sqlalchemy
from sqlalchemy import text
import os

# Only for manual testing of the container
#credential_path = "auth/application_default_credentials.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Initialize secret manager
client = secretmanager.SecretManagerServiceClient()

def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here' # Important for session management, flash messages etc.

# Database
# https://flask-sqlalchemy.readthedocs.io/en/stable/config/ How the connection can be set, without using fgcloud lask_sqlalchemy
# app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f'mysql+pymysql://{access_secret("etl-test-404717","MYSQL_USER")}:{access_secret("etl-test-404717","MYSQL_PASSWORD")}@{access_secret("etl-test-404717","MYSQL_PUBLIC_IP_ADDRESS",version_id=4)}/{access_secret("etl-test-404717","MYSQL_DB",version_id=3)}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False 
app.config["INSTANCE_UNIX_SOCKET"] = "/cloudsql/etl-test-404717:europe-west3:course-app"
app.config["DB_USER"] = access_secret("etl-test-404717","MYSQL_USER")
app.config["DB_PASS"] = access_secret("etl-test-404717","MYSQL_PASSWORD")
app.config["DB_NAME"]  = access_secret("etl-test-404717","MYSQL_DB",version_id=3)
app.config["INSTANCE_CONNECTION_NAME"] = "etl-test-404717:europe-west3:course-app"

def connect_tcp() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    db_user = access_secret("etl-test-404717","MYSQL_USER")
    db_pass = access_secret("etl-test-404717","MYSQL_PASSWORD")
    db_name =  access_secret("etl-test-404717","MYSQL_DB",version_id=3)
    db_host = access_secret("etl-test-404717","MYSQL_PUBLIC_IP_ADDRESS",version_id=4)
    db_port = 3306         # Default port for MySQL

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port,
        ),
    )
    return pool


db = SQLAlchemy(app)
pool = connect_tcp()

# User ORM for SQLAlchemy
class Course_enrollments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable = False)
    enrollment_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    course_date = db.Column(db.Date, nullable = True)
    first_name = db.Column(db.String(50), nullable = True)
    last_name = db.Column(db.String(50), nullable = True)
    email = db.Column(db.String(50), nullable = True)
    comment = db.Column(db.String(500), nullable = True)

    def __repr__(self):
        """Returns a string representation of the Course_enrollments object. This is useful for debugging and logging."""
        return f"<Course_enrollments(id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}')>"

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html', title="Home Page")

@app.route('/list')
def show_list():
    """Renders a page with a list of all course enrollments.This is just for testing"""
    with pool.connect() as db_conn:
        query = text("SELECT * FROM course_enrollments")
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
        
        try:
            # creating Students object
            student = Course_enrollments(
                course_date = course_date,
                first_name = first_name,
                last_name = last_name,
                email = email,
                comment = comment   
            )
            # adding the fields to table
            db.session.add(student)
            db.session.commit()
            # Show the user what info he/she entered
            submission_details = {
                "date": course_date,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "comment": comment if comment else "N/A" # Handle empty comment
            }
            
            return render_template('enrollment-confirmation.html', title="Enrollment Confirmation", submission_data=submission_details)
            # After this is done, we also want to send it to pubsub
       
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"An unexpected error occurred during enrollment: {e}")
            error_message = "An unexpected error occurred. Please try again later."
            return render_template('error.html', title="Error", error_message=error_message), 500   
        

# This is essential for running the app directly from the script
if __name__ == '__main__':
    # debug=True is great for development as it enables the debugger and auto-reloads
    # For production, use a proper WSGI server like Gunicorn or uWSGI and set debug=False
    app.run(host='0.0.0.0', port=5000, debug=True)
    
