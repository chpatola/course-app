from flask import Flask, render_template, url_for, request, abort
from google.cloud import secretmanager
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


# Initialize secret manager
client = secretmanager.SecretManagerServiceClient()

def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Initialize the Flask application
app = Flask(__name__)

print("succes libraries and init of app")
print(app)
app.config["SQLALCHEMY_DATABASE_URI"]= f'mysql+pymysql://{access_secret("etl-test-404717","MYSQL_USER")}:{access_secret("etl-test-404717","MYSQL_PASSWORD")}@{access_secret("etl-test-404717","MYSQL_PUBLIC_IP_ADDRESS",version_id=3)}/{access_secret("etl-test-404717","MYSQL_DB",version_id=3)}'  


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False 


db = SQLAlchemy(app)
print(db)
print("succes db")

class course_enrollments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_date = db.Column(db.Date, nullable = True)
    first_name = db.Column(db.String(50), nullable = True)
    last_name = db.Column(db.String(50), nullable = True)
    email = db.Column(db.String(50), nullable = True)
    comment = db.Column(db.String(500), nullable = True)
    
print("success course_enrollments object")    