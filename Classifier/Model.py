import tensorflow as tf


class LeNet(tf.keras.Model):
    def __init__(self, input_shape):
        super().__init__()
        self.conv1 = tf.keras.layers.Conv2D(filters=6, kernel_size=5,activation='sigmoid', padding='same')
        self.avgpool1 = tf.keras.layers.AvgPool2D(pool_size=2, strides=2)
        self.conv2 = tf.keras.layers.Conv2D(filters=16, kernel_size=5,activation='sigmoid')
        self.svgpool2 = tf.keras.layers.AvgPool2D(pool_size=2, strides=2)
        self.flatten = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(120, activation='sigmoid')
        self.dense2 = tf.keras.layers.Dense(84, activation='sigmoid')
        self.calssify = tf.keras.layers.Dense(10, activation='softmax')

        self.build(input_shape)


    def call(self, inputs):
        ' processes the input to output '
        x = self.conv1(inputs)
        x = self.avgpool1(x)
        x = self.conv2(x)
        x = self.svgpool2(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        y = self.calssify(x)
        return y

    def get_callbacks(self, batch_size):
        model_ckpt = tf.keras.callbacks.ModelCheckpoint(filepath='Saved/Models/cp-{epoch:04d}.ckpt',
                                                 save_weights_only=True,
                                                 verbose=1,
                                                 save_freq=1*batch_size)
        return [model_ckpt]