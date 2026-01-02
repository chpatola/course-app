# What this app does
This is a flask app that hosts a course enrollment site for a traffic school.
The - very simple - web page save the enrollments to course in a MySQL instance hosted on Google Cloud.
The app is deployed with Docker and run in a Google CLoud Run instance.

The data from the app is written to a GCP mySQL instance and sent to a pubsub topic. From there, there is a 
pubsub subscriber that reads the data from the topic and writes it to a GCP BigQuery table.

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
Create a virtual environment 
`python -m venv course_app`
* cd into it and activate it with 
`Scripts/activate`
Install the packages in requirements.txt
`pip install -r requirements.txt`
Uncomment the CREDENTIAL_PATH lines in app.py

### With Docker
* Uncomment the CREDENTIAL_PATH lines in app.py
* Open docker desktop to start the docker engine
* In case you have made changes in the repo and need to update the image, do it with
`docker build . -t course_app`
* Create credentials with `gcloud auth application-default login` Go to the file and paste the content in the file named in application_default_credentials.json in the Repos/secrets folder
* Start the container with 
`docker run -it -v “C:\Users\Ch_EP\OneDrive\Skrivbord\Repos\secrets:/app/auth" -p 5000:5000 course_app`
docker run  -it -p 5000:5000 course_app`

## From Cloud Run
### With GitHub

1. Upload your repo to GitHub
2. Go to Cloud Run in the GCP UI. Click on build from GitHub
3. Follow the steps. For example with the help of https://medium.com/codex/continuously-deploying-a-flask-app-from-a-github-repository-to-google-cloud-run-6f26226539b0#
4. When done, go to Triggers. Make sure the correct settings are here. Especially that the correct service account is chosen
5. Go to Permissions and make sure the correct service account is also used there

### With GCP Artefact
1. Go to Artefact UI
2. Click on create a new repository
3. Fill in the info
4. Run `gcloud auth configure-docker europe-west3-docker.pkg.dev` Exchange the region with your region
5. Tag your local picture `docker build -t europe-west3-docker.pkg.dev/etl-test-404717/course-app/course-app:1.0.0 .`. Exchange the region, the project, the repo-name (from artefact repo name) and the image name
6. Push it to GCP `docker push europe-west3-docker.pkg.dev/etl-test-404717/course-app/course-app:1.0.0`

## What to do next 
1. Plan what kind of transformations should be done to the raw data and what technology?
2. Set up one transformation Job
3. Create a few different outputports (unique Students, unique courses?, exams?)
4. Set up dataplex / Data Catalouge
5. Create some Notebook
6. Do some AI project
 



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


