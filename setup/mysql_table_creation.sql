CREATE TABLE IF NOT EXISTS
  `course_app`.`course_enrollments`( id INT NOT NULL AUTO_INCREMENT,
    enrollment_time TIMESTAMP,
    course_date DATE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    comment VARCHAR(500),
  PRIMARY KEY
    (id) );