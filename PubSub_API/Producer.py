import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from confluent_kafka import Producer as Kafka_Producer
from confluent_kafka.admin import AdminClient, NewTopic

class Producer:
    def __init__(self, config):
        self.config = config

    def error_callback(self, err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))


class Producer_Kafka(Producer):
    def __init__(self, config):
        super().__init__(config)
        self.producer = Kafka_Producer(self.config)

    def write(self, topic, msg):
        self.producer.produce(topic, key=None, value=msg, callback=self.error_callback)

    def create_topic(self, topic):
        broker = AdminClient({"bootstrap.servers": self.config['bootstrap.servers']})
        broker.create_topics([NewTopic(topic, 1, 1)])


# class Producer_google_PubSub(Producer):
#     def __init__(self,):
#         self.producer = pubsub_v1.PublisherClient()
#         self.project_id = self.config['project.id']
#         self.topics = {}

#     def write(self, topic, msg):
#         self.producer.publish(self.topics[topic], msg)

#     def create_topic(self, topic):
#         topic_path = self.producer.topic_path(self.project_id, topic)
#         self.topics[topic] = topic_path
    

