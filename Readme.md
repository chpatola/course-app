# What this app does
This is a flask app that hosts a course enrollment site for a traffic school.
The - very simple - web page saved the enrollments to course in a MySQL instance hosted on Google Cloud.
The app is deployed with Docker and run in a Google CLoud Run instance.

# How to use this app
The app can be spinned up locally or hosted in Google Cloud Run.

## Setup
1. Create a MySQl Instance on Google - choose settings that suit you. Make the instance public
2. Add your IP to the range of allowed IPs on the SQL instance page. Also add the vaule to the secret manager
3. Create a database via the UI and add the name to the env file and to the secret manager
4. Add a user via the UI and add the name and the password to the env file and to the secret manager.
5. Log in with the user you just created
6. Create the table needed with the sql in the setup folder


## Locally

### Without Docker
Use the virtual environment course_app in PS C:\Users\Ch_EP\OneDrive\Skrivbord\Repos\environments>ls
* Activate it with Scripts/activate

### With Docker
* Open docker desktop to start the docker engine
* In case you have made changes in the repo and need to update the image, do it with
`docker build . -t course_app`
* Create credentials with `auth application-default login` Go to the file and paste the content in the file named in application_default_credentials.json in the Repos/secrets folder
* Start the container with 
`docker run -it -v “C:\Users\Ch_EP\OneDrive\Skrivbord\Repos\secrets:/app/auth" -p 5000:5000 course_app`
docker run  -it -p 5000:5000 course_app`

## What to do next 
0. Restore the SQL Database
1. Make a new version of this repo where all stuff needed for App Engine is cleaned out
2. Destroy the old course_app docker image
3. Make sure the new repo deploys locally
4. Create a new course_app image
5. Make sure this new course app image runs normally locally
6. Push it to GitHub
7. Connect from GitHub to Cloud Run
8. Follow the steps from the auomate cloud run deployment on Medium




# TUTORIALS i USE
https://www.geeksforgeeks.org/sql/setting-up-google-cloud-sql-with-flask/
https://medium.com/@anukritj/a-step-by-step-guide-connecting-your-google-cloud-database-to-flask-c8a7df9d7da5

  * Read tutorials again and see if I really need a secretkey env varibale
  * In app, we are creating the student object like twice. Can we have it only once?
  * When everything works, we want to separate the database stuff to its own files. Like her https://github.com/chpatola/flask_db/blob/main/usermodule.py

# try to deploy in gcp with a database
* Google Info https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard
* There is one tutorial on Medium

* Google suggest one use a ADC https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account


Suggestion 1: it say that "All apps in this project are authorized by default" -> try just to deployThen update the app https://cloud.google.com/appengine/docs/standard/nodejs/building-app/updating-web-service

Suggestion 2: Is there not a way to manually pass env variables to the app? In heroku I just do heroku config:set SECRET_KEY=<yoursecretkeyhere> https://stackoverflow.com/questions/22669528/securely-storing-environment-variables-in-gae-with-app-yaml

Suggestion 3: Try
 to access the secret manager and do it from there.
 Kolla om secret manager faktiskt gar att använda. Lägg in det tidigare i app o build. Försök se hur man hittar error messages within the app:

Suggestion 4:
Check if your connections string has the right format 
# Config MySQL
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_UNIX_SOCKET'] = os.environ.get("MYSQL_UNIX_SOCKET")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_CURSORCLASS'] = os.environ.get("MYSQL_CURSORCLASS")
env_variables:
# SQL Configuration
MYSQL_UNIX_SOCKET: '/cloudsql/<GCP Project name>:<GCP region>:<Cloud SQL instance name>'
MYSQL_USER: '<Insert Database username>'
MYSQL_PASSWORD: '<insert Database password>'
MYSQL_DB: '<insert Database name>'
MYSQL_CURSORCLASS: 'DictCursor'
MYSQL_HOST: '<insert Database I.P. Address>'
# Google Keys
GOOGLE_OAUTH_CLIENT_ID: ''
GOOGLE_OAUTH_CLIENT_SECRET: ''
# Facebook Keys
FACEBOOK_OAUTH_CLIENT_ID: ''
FACEBOOK_OAUTH_CLIENT_SECRET: ''
# reCaptcha Keys
RECAPTCHA_SITE_KEY: ''
RECAPTCHA_SECRET_KEY: ''

mysql = MySQL(app)

-> also see the alterantve database under tests
 


# How to deploy to GCP
https://medium.com/@dmahugh_70618/deploying-a-flask-app-to-google-app-engine-faa883b5ffab
* Create a file app.yaml
* Set the name of the fiel contianing the app function and add that it uses gunicorn
* Set python as runtime
* Otheer settings: see example here https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/appengine/flexible/hello_world/app.yaml
Enable App Engine in console and follow steps

Whenever you have made updates to your app repo, you can deploy them to google like this 
gcloud app deploy
# Locally conenct to sql database

Install needed packages (for mysql)
* pip install SQLAlchemy
* pip install PyMySQL
* pip install "cloud-sql-python-connector[pymysql]" 
* pip install python-dotenv


Might be you have to  gcloud auth application-default login    (no!)
Add the needed database name, user name and password in the env file
Load the env file into the test sql connection file
Add a row in this file and check if it got there

# Delete MySQL Database
The database will run up costs even though you turn it off.
To properly save costs you need to delete it and store it as a backup
This backup can be put back to live an all data within, users and so on will persist.
However, the region you have to set again (europe3, Frankfurt) and the IP will de different.
Update the env variable MYSQL_PUBLIC_IP_ADDRESS with the new IP and run the script again. If you need to update your own Ip Address to the whitelist,
see here how to do it in the right format https://mxtoolbox.com/subnetcalculator.aspx. 
I Asked Daniel and for 95.90.232.195, the correct format is
 The IP address you need to add under the SQL instances Connection Part

