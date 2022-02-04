'''
This script simulates a Model app, which:
(1) reads from 'prediction_request' topic -> (2) predicts output -> (3) write to 'prediction_output' topic
'''
import sys, os
import time
import json
import numpy as np
import config
cwd = os.getcwd()
sys.path.append(cwd.split('ML_system')[0])

from PubSub_API.BrokerProvider import BrokerProvider
from PubSub_API.Consumer import Consumer
from PubSub_API.Producer import Producer

from Classifier.Model import LeNet
import tensorflow as tf


def make_prediction(model, msg):
    msg = eval(msg.value().decode('utf-8'))
    # print(msg)
    key = list(msg.keys())[0]
    value = np.array(msg[key])[None,:,:,:]
    prediction_proba = model.predict(value)  # model outputs a string of probabilities
    prediction = np.argmax(prediction_proba)  # convert from probabilities to a category
    print(f'{key}: {prediction}')
    return {key: prediction.tolist()}

def write_prediction(message, producer):
    encoded_message = json.dumps(message, indent=2).encode('utf-8')
    producer.write(topic=config.PREDICTION_OUTPUT, msg=encoded_message)

def process_message_wraper(model, producer):
    ' Function wraper to pass model, and producer objects to process_message function '
    def process_message(msg):
        msg = make_prediction(model, msg)
        write_prediction(msg, producer)
    return process_message


def main():
    # load model
    model = LeNet(input_shape=(None,28,28,1))
    latest = tf.train.latest_checkpoint(cwd.split('ML_system')[0] + '/Classifier/Saved/Models')
    model.load_weights(latest)

    # instantiate producer to 'prediction_output' topic
    broker = BrokerProvider(service='kafka')
    producer = broker.get_producer()
    producer.create_topic(config.PREDICTION_OUTPUT)

    # instantiate consumer
    consumer = broker.get_consumer(process_message_wraper(model, producer))
    consumer.subscribe([config.PREDICTION_REQUEST])

    # do the processing loop:
    consumer.read()


if __name__ == "__main__":
    main()