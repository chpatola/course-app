gcloud pubsub subscriptions create course-app-sub-deadletter \
    --topic=course-app-topic-deadletter \
    --bigquery-table=etl-test-404717.course_app.course_enrollments_raw_dead_letter \
    --use-table-schema \
    --write-metadata \
    --drop-unknown-fields \
    --ack-deadline=10 \
    --message-retention-duration=2d \
    --expiration-period=100d \
    --project=etl-test-404717
