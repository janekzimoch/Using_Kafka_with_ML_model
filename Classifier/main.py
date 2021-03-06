import os, sys
import argparse
import tensorflow as tf
import numpy as np
import json

from DataLoader import DataLoader
from Model import LeNet
from Evaluate import Evaluate
from Evaluate import EvaluateFashionMnist
from Test import TestDataLoader
import config


def main():
    args = pars_args()

    # Load data
    data = DataLoader()
    data.load_TF_data('fashion_mnist')  # Note: I am using a fully loaded dataset rather than a generator, because 
                                        # fashion_mnist/mnist are small datasets so memory usage is managable and
                                        # I wanted to present a clean, minimal solution.  

    # Create a Model
    input_shape = (None, *data.test_ds['image'].shape[1:])
    num_classes = np.max(data.test_ds['label'])+1  # +1 because it's 0 indexed #.shape[1]
    model = LeNet(input_shape=input_shape, num_classes=num_classes)
    loss = 'sparse_categorical_crossentropy'  # Note: we assume 'lable' vector to be NOT one-hot encoded
                                                # if you are using one-hot encoded vector use 'categorical_crossentropy' instead
    model.compile(optimizer="Adam", loss=loss, metrics=['accuracy'])

    # Train
    if args.train:
        print('Training...')
        epochs, batch_size = args.epochs, args.batch_size
        history = model.fit(x=data.train_ds['image'], 
                            y=data.train_ds['label'], 
                            validation_data=(data.test_ds['image'], data.test_ds['label']),
                            callbacks=model.get_callbacks(batch_size),
                            epochs=epochs, batch_size=batch_size)
        json.dump(history.history, open(config.HISTORY_DIR + 'history.json', 'w'))
    else:
        try:
            latest = tf.train.latest_checkpoint('Saved/Models')
            model.load_weights(latest)
        except NameError:
            print('upsss! No model found to load. Make sure you train model first. It should be saved in ./Saved/Models/ by default')

    # Evaluate
    print('Evaluation...')
    evaluate = EvaluateFashionMnist(model, data)
    evaluate.predict()
    evaluate.plot_per_class_accuracy()
    evaluate.plot_train_and_test_accuracy_evolution()


def pars_args():
    ' This function parses command line input from the user '
    parser = argparse.ArgumentParser(description='Specify details of how main.py should operate.')
    parser.add_argument('--dont-train', dest='train', action='store_false',
                        help='Use this flag if you just want to evaluate using last saved model.')
    parser.add_argument('--epochs', default='30', type=int)
    parser.add_argument('--batch_size', default='256', type=int)
    parser.set_defaults(train=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
