from confluent_kafka import Consumer, KafkaError, Producer
import json
import time
import random

# Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'job-status-group',
    'auto.offset.reset': 'earliest'
})

# producer = Producer({'bootstrap.servers': 'localhost:9092'})

def process_event(event):
    job = json.loads(event)
    job["status"] = "DONE"
    print(f"Processed job: {job}")

    # Log the processed job to a file
    with open("processed_jobs1.log", "a") as log_file:
        log_file.write(json.dumps(job) + "\n")
        log_file.flush()
        print(f"Logged job: {job}")

    return job

consumer.subscribe(['job-status'])

# Set a timeout duration (e.g., 60 seconds)
timeout_duration = 60
last_message_time = time.time()

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
             # Check if the timeout has been reached
            if time.time() - last_message_time > timeout_duration:
                print("No new messages for 1 minute. Exiting consumer.")
                break
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        event = msg.value().decode('utf-8')
        processed_job = process_event(event)
        # producer.produce("job-status", value=json.dumps(processed_job))
        # producer.flush()

finally:
    consumer.close()
