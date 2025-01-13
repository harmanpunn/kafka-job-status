# Kafka Job Processing Project

This project demonstrates a simple Kafka-based system with a producer, consumer, and optional Flask API for processing jobs asynchronously. The producer generates jobs with a `status` of `NEW`, while the consumer processes these jobs and updates their status to `DONE`.

---

## Project Structure

```plaintext
kafka-job-status/
│
├── producer/
│   ├── producer.py          # Sends mock job events to Kafka
│
├── consumer/
│   ├── consumer.py          # Processes job events from Kafka
│
├── flask-api/
│   ├── app.py               # Flask API to expose job statuses (optional)
│
├── docker-compose.yml       # Kafka and Zookeeper setup
├── processed_jobs.log       # Logs processed jobs (created during runtime)
├── README.md                # Project description and setup guide
```

---

## Prerequisites

1. **Docker** and **Docker Compose** installed.
2. **Python** (3.7 or later) with `pip` installed.

---

## Setup and Installation

### Step 1: Start Kafka and Zookeeper

Start Kafka and Zookeeper using Docker Compose:
```bash
docker-compose up -d
```

### Step 2: Create the Kafka Topic

Create a topic named `job-status`:
```bash
docker exec -it kafka-job-status-kafka-1 kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 --partitions 1 --topic job-status
```

### Step 3: Install Dependencies

Create a Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install confluent-kafka flask
```

---

## Running the Project

### 1. Start the Producer
The producer generates jobs and sends them to the Kafka topic.

Run the producer script:
```bash
python producer/producer.py
```

### 2. Start the Consumer
The consumer retrieves jobs from the topic, processes them, and updates their status.

Run the consumer script:
```bash
python consumer/consumer.py
```

### 3. Optional: Run the Flask API
The Flask API allows you to interact with the system (e.g., fetch jobs or add new jobs).

Run the API:
```bash
python flask-api/app.py
```
Access it at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### API Endpoints:
- `GET /jobs`: Fetch all jobs.
- `POST /jobs`: Add a new job. Example payload:
  ```json
  {
    "job_id": 1234,
    "status": "NEW"
  }
  ```

---

## Advanced Scenarios

### Multiple Subscribers
- **Same Consumer Group**: Add more consumers with the same `group.id` to distribute workload.
- **Different Consumer Groups**: Use different `group.id` values to broadcast messages to independent subscribers.

### Scaling
- Increase the number of partitions in the Kafka topic to enable more parallelism:
  ```bash
  docker exec -it kafka-job-status-kafka-1 kafka-topics --alter \
    --bootstrap-server localhost:9092 \
    --topic job-status --partitions 4
  ```

---

## Notes
- Logs for processed jobs are written to `processed_jobs.log`.
- Adjust the `timeout_duration` in the consumer to control when it exits due to inactivity.

---

## Cleanup

Stop and remove the Kafka and Zookeeper containers:
```bash
docker-compose down
```

Deactivate the Python virtual environment:
```bash
deactivate
