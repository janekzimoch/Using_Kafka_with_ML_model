import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

import tensorflow_datasets as tfds



class DataLoader:
    def __init__(self, ):
        self.available_datasets = tfds.list_builders()
        self.train_ds = {}
        self.test_ds = {}


    def load_TF_data(self, ds_name):
        ' loads data from www.tensorflow.org/datasets/ '
        if ds_name in self.available_datasets:
            for data_obj, data_type in zip([self.train_ds, self.test_ds], ['train', 'test']):
                ds = tfds.as_numpy(tfds.load(ds_name, 
                                    split=[data_type], 
                                    shuffle_files=True,
                                    batch_size=-1,
                                    as_supervised=True))
                data_obj['image'], data_obj['label'] = ds[0][0], ds[0][1].astype(np.int32)
                if np.issubdtype(ds[0][0].dtype, np.integer): # convert from int [0,255] to float [0,1.0]
                    data_obj['image'] = data_obj['image'] / 255.0
        else:
            print('Use one of the available datasets (see: www.tensorflow.org/datasets/) or use \n\
                    load_data_from_file() function to load your own data. ')
            return


    def load_data_from_file(self, file_name):
        ' Loads data from .npz file, you will need to modify to match your file format '
        data = np.load(file_name)
        x = data['image']  # replace key with your input name
        y = data['label']  # replace key with your output name
        return {'image': x, 'label': y}