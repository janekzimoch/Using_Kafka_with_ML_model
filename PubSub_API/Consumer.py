import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')

from confluent_kafka import Consumer


class Consumer_Kafka:
    def __init__(self, config, msg_processing_func=False):
        self.config = config
        self.consumer = Consumer(config)
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

# i think it would make sense to have a childeren classes as objects Consumer_Kafka and Consumer_Google
