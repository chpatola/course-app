gcloud pubsub topics create [TOPIC_ID] \
    --schema=projects/etl-test-404717/schemas/course-appv1 \
    --message-encoding=json \
    --first-revision-id=projects/etl-test-404717/schemas/course-appv1@- \
    --last-revision-id=projects/etl-test-404717/schemas/course-appv1@+
