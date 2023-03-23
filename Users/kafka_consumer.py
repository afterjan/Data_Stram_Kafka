# Import libraries
from confluent_kafka import Consumer
import json

# Create the consumer instance. Pass the port where the Kafka cluster is running, 
# a consumer group name, as well as the offset reset (where the consumer should start reading):
c = Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer has been initiated...')

# Determine the name of the topic that should be consumed and subscribe to it. 
# If there is more then one topic available, you can list their names with the list_topics().topics command:

print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['user'])

# In order to start receiving events you create an infinite loop that polls the topic, 
# looking for any available messages. The consumer can always be adjusted to start and stop from a specific offset:

def main():
    while True:
        msg = c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue

        with open('users.txt','a') as file:
            data = msg.value().decode('utf-8')
            file.write(''.join(data))
            file.write(', \n')
    c.close()

if __name__ == '__main__':
    main()

# 'a': Opens a file for appending. The file pointer is at the end of the file if the file exists. 
# That is, the file is in the append mode. If the file does not exist, it creates a new file for writing.
