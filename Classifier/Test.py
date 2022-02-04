import matplotlib.pyplot as plt


class TestDataLoader:

    @staticmethod
    def test_TF_dataloader(ds):
        # ds = ds.take(1)

        i = 0
        for example in ds.as_numpy_iterator()[:1]:  # example is `{'image': tf.Tensor, 'label': tf.Tensor}`
            print(list(example.keys()))
            image = example["image"]
            label = example["label"]
            print(image.shape, label)
            plt.figure()
            plt.imshow(image)
            plt.savefig('Saved/Figures/test_dataLoader.png')

            i +=1
            if i>0: break
