from BrokerProvider import BrokerProvider
from Consumer import Consumer
from Producer import Producer
import time 

broker = BrokerProvider(service='confluent')
consumer = broker.get_consumer()
print('Subscribe...')
consumer.subscribe(['test_A'])
print('Start reading...')
consumer.read()