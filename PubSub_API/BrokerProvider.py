import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')
import config as conf

from Producer import Producer_Kafka
from Consumer import Consumer_Kafka
from confluent_kafka import Producer
import socket

config = {}
config['producer'] = {'bootstrap.servers': conf.SERVER_IP,
                    'client.id': socket.gethostname()}

config['consumer'] = {'bootstrap.servers': conf.SERVER_IP,
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}


class BrokerProvider:
    def __init__(self, service='confluent', config=config):
        self.service = service
        self.config = config
    
    def get_producer(self, ):
        if self.service == 'confluent':
            return Producer_Kafka(self.config['producer'])
        elif self.service == 'google_pubsub':
            return
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')

    def get_consumer(self, process_message=None):
        if self.service == 'confluent':
            return Consumer_Kafka(self.config['consumer'], msg_processing_func=process_message) #, self.config['consumer']
        elif self.service == 'google_pubsub':
            pass
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')
