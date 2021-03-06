# Using_Kafka_with_ML_model
A toyexample for Pub/Sub communication, using Kafka Broker, between: an input query app, a simple classification model, and a prediction reading app.

#### Requirements:
* Classifier (Part A)
  * Python (3.+), Tensorflow, Numpy, json, argparse, matplotlib
* PubSub_API (Part B)
  * Java JDK 11+, confluent_kafka, google.cloud.pubsub_v1, Numpy
* ML_system (Part C)
  * all of the above   

Download this repository to a directory called <code>Vector.ai</code>.

# Classifier (Part A)
### How to use
cd to <code>Classifier/</code>  and from the command line run: \
<code>python main.py</code> - to train and evaluate model \
or <code>python main.py --dont-train</code> - to just evaluate on most recently saved model. 
### Structure
This directory contains scripts and classes needed to train, evaluate, and use a simple Classifier model. This is a minimal example of how i build, test, and validate my machine learning models. The structure is as follows: \
Classifier: \
├── Model.py \
├── DataLoader.py \
├── Evaluate.py \
├── Test.py \
├── main.py \
├── Saved \
│   ├── Figures \
│   ├── History \
│   ├── Predictions \
└── ├── Models \
 * **main.py** is a script which can be run from the command line to train or evaluate models (by specyfing appropriate flags).
 * **Model.py** contains Model classes, which can by used interchangably. Each Model class, such as LeNet, extends tf.keras.Model
 * **DataLoader.py** is a class responsible for downloading and loading data from 'tensorflow_datasets'. Because Fashion MNIST and most of other datasets in 'tensorflow_datasets' are small, I didn't create a generator, but just load data in memory (for simplicity).
 * **Evaluate.py** has a class Evaluate(model, data) responsible for evaluation. Curently i implemented the following functions: (1) predict, (2) get/plot_per_class_accuracy() - for logging and visualising train and test performance per each class of a given model, (3) plot_train_and_test_accuracy_evolution() - to inspect how our accuracy changes over epochs.
 * **Test.py** where I would write (reusable) unit tests to proof that functionality of each modle submodule works as intended.
 * **Saved** is a directory where i save visualisations, logs, and models. 

### For bigger projects:
Whenever I work on more complex projects than classifying Fashion MNIST images, I would add additional modules to the structure above, such as: metrics and visualisation callbacks.  The point of this modularity is to have reusable blocks, which i can leverage, to automate running of new experiments and validating ideas. For problems which require model to train longer, I would implement visualisation callbacks which evaluate internal states of the model or do some visualisations every N epochs, this gives me more insight into whats going on inside of the model. For longer projects I would also setup experiment pipeline, where I log every experiment ran into a separete directory, such that I can keep track of the progress and decisions I made during my research.

### Data Loader
To load data you need to first instantiate <code>DataLoader</code> object. Then you can call <code>data.load_TF_data('fashion_mnist')</code> or <code>data.load_data_from_file(file_name)</code> to update internal states of the object <code>self.train_ds</code> and <code>self.test_ds</code>. This are dictionaries and to acces input and outputs ndarrays you need to call <code>self.train_ds['image']</code> or <code>self.train_ds['label']</code>.

### Modyfing dataset:
You can easily load a different dataset from <code>tensorflow_dataset</code> by modifying argument in a method call <code>data.load_TF_data('fashion_mnist')</code> to a different dataset name than 'fashion_mnist' (for list of avilable names see (https://www.tensorflow.org/datasets/catalog/overview) ). \
If you want to load your own dataset from a local file and it is a dict {'image': ..., 'label': ...} saved in <code>.npz</code> file format then within a main.py use <code>data.train_ds = data.load_data_from_file(file_name_train)</code> and <code>data.train_ds = data.load_data_from_file(file_name_test)</code> instead.


# PubSub_API (Part 2)

### How to use
**First, you need to setup a Brooker server** \
You can do it on your local machine by following the instructions in this quickstart tutorial: (https://kafka.apache.org/quickstart) \
Once you have the Kafka Zookeeper and a Broker server running, you can move to the next section.

**Test API functionality** \
Assuming you set your <code>--bootstrap-server</code> to <code>localhost:9092</code> inthe previous step then you don't need to modify anything in the <code>PubSub_API/</code> script. Otherwise change <code>SERVER_IP</code> in configs to your <code>host:port</code>.
  
T demonstrate functionality of the API run in seperate terminals (from within <code>PubSub_API/</code> dir): <code>python main_producer.py/</code> which writes integers from 1 to 100 every 3 seconds to topic 'test_A' and <code>python main_consumer.py/</code> which reads from that topic.

# ML_system (Part 3)
Here we have a toy example of a real life system. There are 3 applications:
* **prediction_query_app.py** which simulates an application that senses/feeds input from the wild to the Brooker topic <code>prediction_request</code>
* **classifier_model_app.py** reads from <code>prediction_request</code> topic, does some processing (that is it uses the classifier model to make a prediction) and then it writes this prediction to a <code>prediction_output</code> topic. 
* **prediction_consumer_app** reads from <code>prediction_output</code> topic and prints to a command line.

To run this example, you need to first setup Zookeerper and Broker server as instructed in *PubSub_API* section above, and then call each app script mentioned above in seperate terminals i.e. <code>python prediction_query_app.py</code>.

 
