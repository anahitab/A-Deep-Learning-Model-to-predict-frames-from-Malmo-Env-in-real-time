import tensorflow as tf
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
from scipy import misc
import glob
import os
import random
from PIL import Image
from data_preprocessing import final_labels , get_raw ,image_labels
from nn_helper import new_weights,new_biases,new_conv_layer,flatten_layer,new_fc_layer
from data_helper import data_iterator

from sklearn.metrics import confusion_matrix
import time
from sklearn.metrics import confusion_matrix
import time

#from main import FLAGS
import matplotlib.pyplot as plt

def predict(final_label,final_images,FLAGS,images_aert,pllot=True):
   
    tf.reset_default_graph()
    checkpoint_dir = FLAGS.save_dir
    img_size=FLAGS.img_size; num_channels=FLAGS.num_channels;num_classes=FLAGS.num_classes
    filter_size1 = FLAGS.filter_size1 ; num_filters1 = FLAGS.num_filters1
    filter_size2 = filter_size1 ; num_filters2 = FLAGS.num_filters2
    filter_size3 = filter_size1 ; num_filters3 = FLAGS.num_filters3
    imz_size_flat  = FLAGS.img_size_flat
    fc_size = FLAGS.fc_size ; num_channels = FLAGS.num_channels
    
    global_step = tf.Variable(0, name='global_step', trainable=False)
    x = tf.placeholder(tf.float32, shape=[None, imz_size_flat], name='x')
    x_image = tf.reshape(x, [-1, img_size, img_size, num_channels])
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, dimension=1)

    layer_conv1, weights_conv1 = new_conv_layer(input=x_image,
                                                num_input_channels=num_channels,
                                                filter_size=filter_size1,
                                                num_filters=num_filters1,
                                                use_pooling=True)

    layer_conv2, weights_conv2 = new_conv_layer(input=layer_conv1,
                                                num_input_channels=num_filters1,
                                                filter_size=filter_size2,
                                                num_filters=num_filters2,
                                                use_pooling=True)

    layer_conv3, weights_conv3 = new_conv_layer(input=layer_conv2,
                                                num_input_channels=num_filters2,
                                                filter_size=filter_size3,
                                                num_filters=num_filters3,
                                                use_pooling=True)

    layer_flat, num_features = flatten_layer(layer_conv3)

    layer_fc1 = new_fc_layer(input=layer_flat,
                             num_inputs=num_features,
                             num_outputs=fc_size,
                             use_relu=True)

    layer_fc2 = new_fc_layer(input=layer_fc1,
                             num_inputs=fc_size,
                             num_outputs=num_classes,
                             use_relu=False)

    y_pred = tf.nn.softmax(layer_fc2)

    y_pred_cls = tf.argmax(y_pred, dimension=1)

    #print(self.y_pred_cls)

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits( logits = layer_fc2, labels = y_true)
    cost = tf.reduce_mean(cross_entropy)
    optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
    opt_op = optimizer.minimize(cost,global_step=global_step)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
        print('Loaded the trained model: {}'.format(checkpoint_file))

        saver = tf.train.Saver()
        saver.restore(sess, checkpoint_file)

        
        test_len = 10
        d_itr   = data_iterator(final_images,final_label,images_aert)
        a1, a2 ,a3  = d_itr.next_batch(test_len)
        x_batch = np.reshape(a1,[test_len, imz_size_flat])

        test_data = x_batch
        test_label = a2
        
        #print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
        ase = sess.run(y_pred,feed_dict={x:x_batch,y_true:a2})
        print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y_true: test_label}))
        if pllot:
            plot_images(a3,test_label,ase)
        return ase , test_label
	


def plot_images(imges, cls_true, cls_pred=None):
    print(cls_true[0])
    print (cls_pred[0],"sdfsdfs")
    axcv =[];pred=[]
    for val in cls_pred:
        #pred.append(val.index(np.max(val)))
        pred.append(np.argmax(val))

    for val in cls_true:
        axcv.append(val.index(1))


    images = []
    t = len(cls_true)
    for val in imges[:t-1]:
        ax = Image.open(val)
        images.append(ax)
    
    if len(images) == 0:
        print("no images to show")
        return 
    else:
        random_indices = random.sample(range(len(images)), min(len(images), 9))
        print random_indices
    images, cls_true  = zip(*[(images[i], axcv[i]) for i in random_indices])
    
    fig, axes = plt.subplots(3, 3)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    #print axes.flat

    for i, ax in enumerate(axes.flat):
        print i,ax
        ax.imshow(images[i])

        if cls_pred is None:
            xlabel = "True: {0}".format(axcv[i])
        else:
            xlabel = "True: {0}, Pred: {1}".format(axcv[i], pred[i])
        ax.set_xlabel(xlabel)
        
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.show()

