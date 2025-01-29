from confluent_kafka import Producer
import time 
import json
import random


producer = Producer({'bootstrap.servers': 'localhost:9092'})

def generate_job_event():
    return {
        "job_id": random.randint(1000, 9999),
        "status": "NEW"
    }   

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed for {msg.key()}: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    while True:
        event = generate_job_event()
        producer.produce(
            "job-status",
            key = str(event["job_id"]),
            value = json.dumps(event),
            callback = delivery_report
        )

        producer.flush()
        time.sleep(0.5)
s