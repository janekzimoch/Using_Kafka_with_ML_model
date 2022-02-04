import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from concurrent.futures import TimeoutError
from confluent_kafka import Consumer as Kafka_Consumer
from google.cloud import pubsub


class Consumer:
    def __init__(self, config):
        self.config = config


class ConsumerKafka(Consumer):
    def __init__(self, config, msg_processing_func=False):
        super().__init__(config)
        self.consumer = Kafka_Consumer(config)
        self.running = False
        if msg_processing_func == False:
            self.msg_processing_func = self.msg_print
        else:
            self.msg_processing_func = msg_processing_func

    def msg_print(self, msg):
        msg = msg.value().decode('utf-8')
        print(msg)

    def subscribe(self, topics):
        try:
            self.consumer.subscribe(topics)
        except NameError:
            print(f'Couldnt subscribe to {topics}')

    def read(self, ):
        self.running = True
        while self.running:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                    (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                self.msg_processing_func(msg)

    def shutdown(self, ):
        self.running = False
        self.consumer.close()


class ConsumerGooglePubSub(Consumer):
    def __init__(self, config):
        super().__init__(config)
        self.consumer = pubsub.SubscriberClient()
        self.project_id = self.config['project_id']

    def subscribe(self, topics):
        subscription_id = [topics[i] + id(self) for i in range(len(topics))]  #unique identifier of an object subscription to a topic
        subscription_path = self.consumer.subscription_path(self.project_id, subscription_id)
        self.streaming_pull_future = self.consumer.subscribe(subscription_path)

    def read(self, ):
        with self.consumer:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                timeout = 5.0
                self.streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                self.streaming_pull_future.cancel()  # Trigger the shutdown.
                self.streaming_pull_future.result() 

