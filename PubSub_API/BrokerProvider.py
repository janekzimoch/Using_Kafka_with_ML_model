import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')
import PubSub_API.config as config

from Producer import Producer_Kafka #, Producer_google_PubSub
from Consumer import Consumer_Kafka #, Consumer_google_PubSub
import socket

print(cwd)
print(config)
conf = {}
conf['producer'] = {'bootstrap.servers': config.SERVER_IP,
                    'client.id': socket.gethostname()} #,
                    # 'project.id': config.PROJECT_ID}

conf['consumer'] = {'bootstrap.servers': config.SERVER_IP,
                    'group.id': "foo",
                    'auto.offset.reset': 'smallest'} #,
                    # 'project.id': config.PROJECT_ID}



class BrokerProvider:
    def __init__(self, service='confluent', config=conf):
        self.service = service
        self.conf = conf
    
    def get_producer(self, ):
        if self.service == 'confluent':
            return Producer_Kafka(self.conf['producer'])
        elif self.service == 'google_pubsub':
            return # Producer_google_PubSub(self.conf['producer'])
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')

    def get_consumer(self, process_message=None):
        if self.service == 'confluent':
            return Consumer_Kafka(self.conf['consumer'], msg_processing_func=process_message)
        elif self.service == 'google_pubsub':
            return # Consumer_google_PubSub()
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')
