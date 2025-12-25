# If this works, we have to figure out how to use it in the app file with the object model
from google.cloud.sql.connector import Connector
import sqlalchemy
from google.cloud import secretmanager

#Initiate secret manager object
client = secretmanager.SecretManagerServiceClient()


# initialize Connector object
connector = Connector()

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
  (4844654,
  now(),
    "2025-09-05",
    "Alla",
    "Iva",
    "eae_ii2@mail.com",
    "Secret managbhjjhb") """,
)

# connect to connection pool
with pool.connect() as db_conn:

  db_conn.execute(insert_stm)

  # commit transaction (SQLAlchemy v2.X.X is commit as you go)
  db_conn.commit()


  # query and fetch ratings table
  results = db_conn.execute(sqlalchemy.text("SELECT * from course_app.course_enrollments")).fetchall()

  # show results
  for row in results:
    print(row)