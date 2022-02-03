from BrokerProvider import BrokerProvider
from Consumer import Consumer
from Producer import Producer
import time 

broker = BrokerProvider(service='confluent')
producer = broker.get_producer()
producer.create_topic('test_A')
for i in range(100):
    producer.write(topic='test_A', msg=str(i))
    time.sleep(3)