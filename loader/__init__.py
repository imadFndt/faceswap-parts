import tensorflow as tf

from .data_augmentation import read_image


class DataLoader:
    def __init__(
            self,
            filenames,
            all_filenames,
            batch_size,
            dir_bm_eyes,
            resolution,
            num_cpus,
            session,
            **config
    ):
        self.filenames = filenames
        self.all_filenames = all_filenames
        self.batch_size = batch_size
        self.dir_bm_eyes = dir_bm_eyes
        self.resolution = resolution
        self.num_cpus = num_cpus
        self.session = session

        self.prob_random_color_match = 0.5
        self.use_da_motion_blur = None
        self.use_bm_eyes = None

        self.set_data_augm_config(
            config["prob_random_color_match"],
            config["use_da_motion_blur"],
            config["use_bm_eyes"]
        )

        self.data_iter_next = self.create_tfdata_iter()

    def set_data_augm_config(
            self,
            prob_random_color_match=0.5,
            use_da_motion_blur=True,
            use_bm_eyes=True
    ):
        self.prob_random_color_match = prob_random_color_match
        self.use_da_motion_blur = use_da_motion_blur
        self.use_bm_eyes = use_bm_eyes
        pass

    def create_tfdata_iter(self):
        tf_fns = tf.constant(self.filenames, dtype=tf.string)  # use tf_fns=filenames is also fine
        dataset = tf.data.Dataset.from_tensor_slices(tf_fns)
        dataset = dataset.shuffle(len(self.filenames))
        dataset = dataset.apply(
            tf.contrib.data.map_and_batch(
                lambda filenames: tf.py_func(
                    func=read_image,
                    inp=[filenames,
                         self.all_filenames,
                         self.dir_bm_eyes,
                         self.resolution,
                         self.prob_random_color_match,
                         self.use_da_motion_blur,
                         self.use_bm_eyes],
                    Tout=[tf.float32, tf.float32, tf.float32]
                ),
                batch_size=self.batch_size,
                num_parallel_batches=self.num_cpus,  # cpu cores
                drop_remainder=True
            )
        )
        dataset = dataset.repeat()
        dataset = dataset.prefetch(32)

        iterator = dataset.make_one_shot_iterator()
        next_element = iterator.get_next()  # this tensor can also be useed as Input(tensor=next_element)
        return next_element

    def get_next_batch(self):
        return self.session.run(self.data_iter_next)

    pass
