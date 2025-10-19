# These things you can try in another path. And try in local first
from google.cloud import secretmanager
import sqlalchemy
from sqlalchemy import text

# Initialize secret manager
client = secretmanager.SecretManagerServiceClient()

def access_secret(project_id, secret_id, version_id=1):
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def connect_tcp() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_user = access_secret("etl-test-404717","MYSQL_USER")
    db_pass = access_secret("etl-test-404717","MYSQL_PASSWORD")
    db_name =  access_secret("etl-test-404717","MYSQL_DB")
    db_host = access_secret("etl-test-404717","MYSQL_PUBLIC_IP_ADDRESS",version_id=2)
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

# When running on your local machine, use the TCP connector function.
# The Cloud SQL Auth Proxy must be running in a separate terminal.
pool = connect_tcp()
print(pool)



# The 'pool' object is an Engine. You can get a connection from it.
# Using a 'with' statement ensures the connection is properly closed and returned to the pool.
with pool.connect() as db_conn:
    # Construct a SQL query. Using text() is a good practice for raw SQL.
    # The database name ('course_app') is specified when creating the connection pool.
    # This means any queries on this connection are run against that database by default,
    # so you only need to specify the table name. Using the fully qualified name
    # `course_app`.`course_enrollments` would also work but is redundant here.
    query = text("SELECT * FROM course_enrollments")

    # Execute the query and fetch all results
    results = db_conn.execute(query).fetchall()

    # Print the results
    print(f"\nFound {len(results)} records in 'course_enrollments':")
    for row in results:
        # Each 'row' is a RowProxy object, which can be accessed like a tuple or by column name
        print(row)
