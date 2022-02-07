import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from confluent_kafka import Producer as Kafka_Producer
from confluent_kafka.admin import AdminClient, NewTopic
from google.cloud import pubsub_v1


class Producer:
    def __init__(self, config):
        self.config = config

    def error_callback(self, err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))


class ProducerKafka(Producer):
    def __init__(self, config):
        super().__init__(config)
        self.producer = Kafka_Producer(self.config)

    def write(self, topic, msg):
        self.producer.produce(topic, key=None, value=msg, callback=self.error_callback)

    def create_topic(self, topic):
        broker = AdminClient({"bootstrap.servers": self.config['bootstrap.servers']})
        broker.create_topics([NewTopic(topic, 1, 1)])


class ProducerGooglePubSub(Producer):
    def __init__(self, config):
        super().__init__(config)
        self.producer = pubsub_v1.PublisherClient()
        self.project_id = self.config['project_id']
        self.topics = {}

    def write(self, topic, msg):
        msg = msg.encode("utf-8")
        self.producer.publish(self.topics[topic], msg)

    def create_topic(self, topic):
        topic_path = self.producer.topic_path(self.project_id, topic)
        topic = self.producer.create_topic(request={"name": topic_path})
        self.topics[topic] = topic_path
        print(topic, topic_path)

        # in google pub-sub in order to subscribe to a topic we need to know the topic path.
        # a list of all topic paths should be somehow accesible for the consumer (aka subscriber)
        # thus maybe i can keep some .json file which keeps a dict of topic: topic_path
    

