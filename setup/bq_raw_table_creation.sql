CREATE TABLE IF NOT EXISTS `course_app.course_enrollments_raw`(
  subscription_name STRING NOT NULL
  OPTIONS (
    description = "The name of the Pub/Sub subscription that delivered the message"),
  message_id STRING NOT NULL
  OPTIONS (
    description = "Unique ID assigned by Pub/Sub to identify this specific event"),
  publish_time TIMESTAMP NOT NULL
  OPTIONS (
    description = "The server-side timestamp when the message was received by Pub/Sub"),
  attributes JSON
  OPTIONS (
    description = "Custom key-value pairs (attributes) sent with the Pub/Sub message"),
  enrollment_time TIMESTAMP NOT NULL
  OPTIONS (description = "The application-level time the student enrolled"),
  course_date DATE NOT NULL
  OPTIONS (
    description = "The scheduled date of the course used for table partitioning"),
  first_name STRING
  OPTIONS (description = "Student's first name"),
  last_name STRING
  OPTIONS (description = "Student's last name used for table clustering"),
  email STRING
  OPTIONS (description = "Student's contact email address"),
  comment STRING
  OPTIONS (
    description = "Additional notes or comments provided during enrollment"))
  PARTITION BY course_date
  CLUSTER BY last_name
  OPTIONS (
    description = "Raw course enrollment landing table partitioned by course_date and clustered by last_name for optimized performance");
