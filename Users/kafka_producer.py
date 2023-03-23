# Import libraries
from confluent_kafka import Producer
import json
import time
import logging
import requests

url = 'https://dummyjson.com/users'
# request data
response = requests.get(url)
# read and parse the data using json()
users = response.json()

# Configure the format of logs. Every time a new event becomes available,
# logs will be appended in a producer.log file in main directory
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')
# filemode='w': Opens a file for writing only. Overwrites the file if the file exists.
# If the file does not exist, creates a new file for writing.

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the producer by specifying the port of Kafka cluster
p = Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer has been initiated...')

# Define a callback function that takes care of acknowledging new messages or errors. 
# When a valid message becomes available, it is decoded to utf-8 and printed in the
# preferred format. The same message is also appended to the logs file
def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

# Write a producer loop. Each message is converted from dictionary to json format to be sent to Kafka
topic_name = 'user'
def main():
    for user in users['users']: # in the json file users there is key namely 'users'
        p.produce(topic_name, json.dumps(user).encode('utf-8'), callback=receipt) # json.dumps(): convert dict to json file
        p.poll(1)
        p.flush()
        time.sleep(3) # suspends execution for 3 sec.

if __name__ == '__main__':
    main()

# the main() function is calling poll() to request any previous events to the producer.
# If found, events are sent to the callback function (receipt). In this case, 
# p.poll(1) means that a timeout of 1 second is allowed.

# Eventually, the producer is also flushed ( p.flush()),
# that means blocking it until previous messaged have been delivered effectively,
# to make it synchronous.