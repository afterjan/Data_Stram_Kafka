# Import libraries
from confluent_kafka import Consumer, KafkaError
import json

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'carts-group',
}

# Initiate consumers
consumer1 = Consumer({
    **conf,
    'auto.offset.reset': 'earliest'
})
consumer2 = Consumer({
    **conf,
    'auto.offset.reset': 'earliest'
})

# Subscribe to the topic
consumer1.subscribe(['carts'])
consumer2.subscribe(['carts'])

try:
    while True:
        msg1 = consumer1.poll(1.0)
        msg2 = consumer2.poll(1.0)

        # Displays messages received by each consumer
        if msg1 is not None:
            with open('carts1.txt','a') as file:
                data = msg1.value().decode('utf-8')
                file.write(''.join(data))
                file.write(', \n')
        if msg2 is not None:
            with open('carts2.txt','a') as file:
                data = msg2.value().decode('utf-8')
                file.write(''.join(data))
                file.write(', \n')
except KeyboardInterrupt:
    pass

consumer1.close()
consumer2.close()