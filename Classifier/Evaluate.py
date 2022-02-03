import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import json

import config


class Evaluate:
    def __init__(self, model, data):
        self.model = model
        self.train_ds = data.train_ds
        self.test_ds = data.test_ds

    def predict(self,):
        train_predictions = self.model.predict(self.train_ds['image'])
        test_predictions = self.model.predict(self.test_ds['image'])
        np.save(train_predictions, config.PREDICTIONS_DIR + 'train_predictions.npy')
        np.save(test_predictions, config.PREDICTIONS_DIR + 'test_predictions.npy')


    def get_per_class_accuracy(self, ):
        results = {}
        for data_obj, data_type in zip([self.train_ds, self.test_ds], ['train', 'test']):
            results[data_type] = {}
            num_classes = np.max(data_obj['label'])+1
            for i in range(num_classes):
                indexes = data_obj['label'] == i
                results[data_type][i] = self.model.evaluate(x=data_obj['image'][indexes], y=data_obj['label'][indexes], return_dict=True)
            with open(config.FIGURES_DIR + 'per_class_accuracy.txt', 'a') as f:
                f.write('ds,class,accuracy\n')
                for i in range(num_classes):
                    acc = np.round(results[data_type][i]["accuracy"], 3)
                    print(f'ds: {data_type}, Category: {i}, Acc: {acc}')
                    f.write(f'{data_type},{i},{acc}\n')
        return results

    def plot_per_class_accuracy(self, label_names=0):
        results = self.get_per_class_accuracy()
        
        plt.figure(figsize=(10,6))
        barwidth = 0.4
        num_classes = len(results['train'].keys())
        train_acc = [results['train'][i]["accuracy"]for i in range(num_classes)]
        test_acc = [results['test'][i]["accuracy"]for i in range(num_classes)]
        plt.bar(np.arange(num_classes)-(barwidth/2), train_acc, width = barwidth, label ='train')
        plt.bar(np.arange(num_classes)+(barwidth/2), test_acc, width = barwidth, label ='test')
        plt.ylabel('accuracy')
        plt.xlabel('categories')
        plt.title('Accuracy by classification category')
        if label_names == 0:
            plt.xticks(np.arange(num_classes))
        else:
            plt.xticks(np.arange(num_classes), [label_names[i] for i in range(num_classes)])
        plt.legend()
        plt.savefig(config.FIGURES_DIR + 'per_class_accuracy.png')


    def plot_train_and_test_accuracy_evolution(self, ):
        history = json.load(open(config.HISTORY_DIR + 'history.json', 'r'))
        
        plt.figure(figsize=(10,6))
        num_epochs = len(history['accuracy'])
        plt.plot(np.arange(num_epochs), history['accuracy'], label='train')
        plt.plot(np.arange(num_epochs), history['val_accuracy'], label='test')
        plt.title('Testa and train acc evolution')
        plt.xlabel('epochs')
        plt.ylabel('accuracy')
        plt.legend()
        plt.savefig(config.FIGURES_DIR + 'accuracy_evolution.png')



class Evaluate_Fashion_Mnist(Evaluate):
    def __init__(self, model, data):
        super().__init__(model, data)

    def plot_per_class_accuracy(self, ):
        label_names = {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 
                        5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}
        super().plot_per_class_accuracy(label_names)


    def plot_hard_samples(self, ):
        # TODO
        pass


