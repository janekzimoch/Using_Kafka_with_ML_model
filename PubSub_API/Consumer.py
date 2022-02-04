import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from confluent_kafka import Consumer as Kafka_Consumer
from google.cloud import pubsub_v1


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


# class ConsumerGooglePubSub(Consumer):
#     def __init__(self, config):
#         super().__init__(config)
#         self.consumer = pubsub_v1.SubscriberClient()
#         self.project_id = self.config['project.id']

#     def subscribe(self, topics):
# 		subscription_path = self.consumer.subscription_path(self._project_id, self.subscription_id)
# 		self._subscription_path = subscription_path
#         pass

#     def read(self, ):
#         pass

#     def shutdown(self, ):
#         pass
