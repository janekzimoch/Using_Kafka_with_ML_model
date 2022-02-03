import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic


class Producer_Kafka:
    def __init__(self, config):
        self.config = config
        self.producer = Producer(config)

    def write(self, topic, msg):
        self.producer.produce(topic, key=None, value=msg, callback=self.error_callback)

    def create_topic(self, topic):
        broker = AdminClient({"bootstrap.servers": self.config['bootstrap.servers']})
        broker.create_topics([NewTopic(topic, 1, 1)])

    def error_callback(self, err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))
