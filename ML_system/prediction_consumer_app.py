'''
This script simulates an application which uses predictions made by Model in real time.
It consumes from 'prediction_output' topic
''' 
import sys, os
import config
cwd = os.getcwd()
sys.path.append(cwd.split('ML_system')[0])

from PubSub_API.BrokerProvider import BrokerProvider
# from PubSub_API.Consumer import Consumer


def msg_print(msg):
    msg = msg.value().decode('utf-8')
    print(msg)

def main():
    # instantiate consumer
    broker = BrokerProvider(service='kafka')
    consumer = broker.get_consumer(msg_print)
    consumer.subscribe([config.PREDICTION_OUTPUT])

    # do the processing loop
    consumer.read()



if __name__ == "__main__":
    main()