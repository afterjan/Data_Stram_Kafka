# Import libraries
from confluent_kafka import Producer
import json
import time
import logging
import requests

url = 'https://dummyjson.com/carts'
# request data
response = requests.get(url)
# read and parse the data using json()
carts = response.json()

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
        message = 'Produced message on topic {} in partition {} with value of {}\n'.format(msg.topic(), msg.partition(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

# Write a producer loop. Each message is converted from dictionary to json format to be sent to Kafka
topic_name = 'carts'
def main():
    for cart in carts['carts']:
        p.produce(topic_name, json.dumps(cart).encode('utf-8'), callback=receipt) # json.dumps(): convert dict to json file
        p.poll(1)
        p.flush()
        time.sleep(3) # suspends execution for 3 sec.

if __name__ == '__main__':
    main()