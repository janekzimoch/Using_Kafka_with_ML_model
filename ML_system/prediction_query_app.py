'''
This script simulates an application which requests prediction for some input samples of Fashion MNIST dataset
''' 
import sys, os
import time
import json
import config
cwd = os.getcwd()
sys.path.append(cwd.split('ML_system')[0])

from Classifier.DataLoader import DataLoader

from PubSub_API.BrokerProvider import BrokerProvider
from PubSub_API.Producer import Producer


def main():
    # load dataset
    data = DataLoader()
    data.load_TF_data('fashion_mnist')
    val_input_data = data.test_ds['image']

    # instantiate producer
    broker = BrokerProvider(service='kafka')
    producer = broker.get_producer()
    producer.create_topic(config.PREDICTION_REQUEST)

    # simulate prediction requests
    for ind, image in enumerate(val_input_data):
        message = {ind: image.tolist()}  # send message with a key identyfing which input sample we are passing
        encoded_message = json.dumps(message, indent=2).encode('utf-8')
        producer.write(topic=config.PREDICTION_REQUEST, msg=encoded_message)
        print(f'sent {ind}th image to broker')
        time.sleep(5)



if __name__ == "__main__":
    main()