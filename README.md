# Data Stream Kafka
Ingest data from an API using Kafka into local computer's file system in a streaming way.

## Tech Stack
1. Docker
2. Confluent Kafka

## Dataset
Users and carts dataset [from here](https://dummyjson.com).

## Step
### A. Topic with no partition and only one consumer (dir: users)
1. Install confluent kafka python library:
   ```
   pip3 install confluent-kafka
   ```
2. Run a local Kafka Cluster with Docker <br /> 
   In order to run a Kafka cluster in local, we need two things: a Kafka broker and Zookeeper. The most convenient way to set them up, is to use a Docker compose file to run multiple containers and launch everything with a single configuration script. I use the `docker-compose.yml` file stored in this GitHub repo (stored in the same directory as the Kafka producer and consumer Python files). To build both containers via CLI, use this command:
   ```
   docker-compose up -d
   ```
3. Confluent Control Center
   Control Center provides a user interface that enables you to get a quick overview of cluster health, observe and control messages, topics, and Schema Registry, and to develop and run ksqlDB queries. access to the control center can be done from the port on the docker container or can go directly to http://localhost:9021/
   <img width="988" alt="Screenshot 2023-03-26 at 21 29 33" src="https://user-images.githubusercontent.com/113230789/227782580-cd1dcdc7-7de3-4222-8055-aa58de0864f4.png">
   <img width="1440" alt="Screenshot 2023-03-22 at 15 08 25" src="https://user-images.githubusercontent.com/113230789/227782721-aca7aa39-2987-4e6f-b3f8-0b55793d166f.png">
4. Build a Kafka producer and consumer.
5. Run kafka producer (make sure to run in the directory that stored kafka producer)
   ```
   python kafka_producer.py
   ```
   when the producer is run a log file will be created: `users.log`.
6. Run kafka consumer (make sure to run in the dir. that stored kafka consumer).
   ```
   python kafka_consumer.py
   ```
   The ingested data will appear in the directory: `users.txt`.
   
   
### B. Topic with partition and 2 consumer (dir: carts)
To create a topic with partition, I try to use confluent UI:
1. Click on `topics` > `Add a topic` > fill in `topic name` and `number of partitions` > `create with defaults`.
<img width="1439" alt="Screenshot 2023-03-22 at 15 30 48" src="https://user-images.githubusercontent.com/113230789/227783521-464a4664-b1bb-4856-8f01-0fceebd8b4b7.png">
<img width="1074" alt="Screenshot 2023-03-26 at 21 54 31" src="https://user-images.githubusercontent.com/113230789/227784171-2e291939-1fd2-48a5-b7e9-9bd71bcef220.png">
<img width="1437" alt="Screenshot 2023-03-23 at 13 23 47" src="https://user-images.githubusercontent.com/113230789/227784320-7e457b5e-146d-48b9-99db-b3ca77643a26.png">
2. Build Kafka producer and consumer. <br />
3. Run Kafka producer and consumer. <br />
4. The ingested data will appear in the directory: carts1.txt and carts2.txt.
