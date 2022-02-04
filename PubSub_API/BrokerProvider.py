import sys, os
cwd = os.getcwd()
sys.path.append(cwd.split('Vector.ai')[0] + 'Vector.ai/PubSub_API')
import PubSub_API.config as config

from Producer import ProducerKafka #, ProducerGooglePubSub
from Consumer import ConsumerKafka #, ConsumerGooglePubSub
import socket


conf = {'kafka': {}, 'google': {}}
conf['kafka']['producer'] = {'bootstrap.servers': config.SERVER_IP,
                            'client.id': socket.gethostname()}
conf['kafka']['consumer'] = {'bootstrap.servers': config.SERVER_IP,
                            'group.id': "foo",
                            'auto.offset.reset': 'smallest'}

conf['google']['producer'] = {'project_id': config.PROJECT_ID}
conf['google']['consumer'] = {'project_id': config.PROJECT_ID}


class BrokerProvider:
    def __init__(self, service='kafka', config=conf):
        self.service = service
        self.conf = conf
    
    def get_producer(self, ):
        if self.service == 'kafka':
            return ProducerKafka(self.conf['kafka']['producer'])
        elif self.service == 'google':
            return # ProducerGooglePubSub(self.conf['google']['producer'])
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')

    def get_consumer(self, process_message=None):
        if self.service == 'confluent':
            return ConsumerKafka(self.conf['kafka']['consumer'], msg_processing_func=process_message)
        elif self.service == 'google':
            return # ConsumerGooglePubSub(self.conf['google']['consumer'])
        else:
            raise KeyError(f'{self.service} is not one of the supported service providers.')
