from google.cloud.sql.connector import Connector
# The outcommented lines are if using a local env file where the values are saved
#from dotenv import load_dotenv  
#load_dotenv()
import sqlalchemy
import os

from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

connector = Connector()

def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


# initialize SQLAlchemy connection pool with Connector
print("Initializing database connection pool")
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=lambda: connector.connect(
        "etl-test-404717:europe-west3:chpatola",
        "pymysql",
        user = access_secret("etl-test-404717","MYSQL_USER"),
        password = access_secret("etl-test-404717","MYSQL_PASSWORD"),
        db = access_secret("etl-test-404717","MYSQL_DB",version_id=3)
        #user=os.environ.get("MYSQL_USER"),
        #password=os.environ.get("MYSQL_PASSWORD"),
        #db=os.environ.get("MYSQL_DB")
    ),
)


# insert statement
insert_stm = sqlalchemy.text(
    """INSERT INTO course_app.course_enrollments (
    id,
    enrollment_time,
    course_date,
    first_name,
    last_name,
    email,
    comment)
VALUES
  (1,
  now(),
    "2025-09-05",
    "Al",
    "Iv",
    "ee_ii2@mail.com",
    "Secret manager 2") """,
)


with pool.connect() as db_conn:

    print("Opening connection to database")
 
    # insert into database
    db_conn.execute(insert_stm)
    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # query database
    result = db_conn.execute(sqlalchemy.text("SELECT * from course_app.course_enrollments")).fetchall()
    
    # Do something with the results
    for row in result:
        print(row)




    