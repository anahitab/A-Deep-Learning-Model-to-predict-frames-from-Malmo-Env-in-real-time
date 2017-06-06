import tensorflow as tf
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
from scipy import misc
import glob
import os
import random
from data_preprocessing import final_labels , get_raw ,image_labels
from real_time_pre import predict_
from test import predict



tf.app.flags.DEFINE_integer("img_size",128,"dimension of image")
tf.app.flags.DEFINE_integer("num_channels",4,"dimension of image")
tf.app.flags.DEFINE_integer("num_classes",23,"dimension of image")
tf.app.flags.DEFINE_integer("filter_size1",3,"dimension of image")
tf.app.flags.DEFINE_integer("filter_size2",3,"dimension of image")
tf.app.flags.DEFINE_integer("filter_size3",3,"dimension of image")
tf.app.flags.DEFINE_integer("num_filters1",32,"dimension of image")
tf.app.flags.DEFINE_integer("num_filters2",32,"dimension of image")
tf.app.flags.DEFINE_integer("num_filters3",64,"dimension of image")
tf.app.flags.DEFINE_integer("fc_size",128,"dimension of image")
tf.app.flags.DEFINE_integer("train_batch_size",16,"training batch size")
tf.app.flags.DEFINE_integer("img_size_flat",65536,"dimension of image")
tf.app.flags.DEFINE_integer("num_epochs",20,"number of epochs")

tf.app.flags.DEFINE_bool("test",True,"use True for testing")
tf.app.flags.DEFINE_bool("real_time_pre",False,"use True for testing")
tf.app.flags.DEFINE_bool("load_train",False,"use True to continue from previous training checkpoint")
tf.app.flags.DEFINE_string("path_to_csv","/home/prayalankar/Downloads/anahita/new_csv.csv","change according to your path")
#tf.app.flags.DEFINE_string("save_dir","/home/prayalankar/Downloads/anahita/ter","change according to your path")
tf.app.flags.DEFINE_string("save_dir","/Users/cory/aip/project_save","change according to your path")

from model import img_Model

FLAGS = tf.app.flags.FLAGS 


def main():

    im_id ,im_label = get_raw(FLAGS.path_to_csv)
    final_images , temp_label = image_labels(im_id,im_label)
    final_label = final_labels(temp_label)
    
    tf.reset_default_graph()
    model = img_Model(final_images , final_label , FLAGS)
    
    if FLAGS.test:
        print ("testing")
        asw = predict(final_label,final_images,FLAGS)
        print("-"*50)
        return
    if FLAGS.real_time_pre:
        ase = predict_predict(final_label=None,final_images=None,FLAGS=None)
        reutrn 
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        if FLAGS.load_train:
            a=5
        else:
            model.optimize(sess)

if __name__ == '__main__':
    main()

