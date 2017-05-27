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
from nn_helper import new_weights,new_biases,new_conv_layer,flatten_layer,new_fc_layer
from data_helper import data_iterator
#from main import FLAGS


def predict_(final_label,final_images,FLAGS):
   
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
        #sess.run(tf.initialize_all_variables())
	sess.run(tf.global_variables_initializer())
        checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
        #print('Loaded the trained model: {}'.format(checkpoint_file))

        saver = tf.train.Saver()
        saver.restore(sess, checkpoint_file)

        
        test_len = 1
        #d_itr   = data_iterator(final_images,final_label)
        #a1, a2  = d_itr.next_batch(test_len)
        #x_batch = np.reshape(a1,[test_len, imz_size_flat])

        #rt = misc.imread(final_images)
	      #final_images =[]
        #final_images.append(rt)        


        x_batch = [final_images]
        a2 =[final_label]

        test_data = x_batch
        test_label = a2
        
        #print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
        ase = sess.run(y_pred,feed_dict={x:x_batch,y_true:a2})
        tpi=list(ase[0])
        #print("\n")
      	apol= tpi.index(max(tpi))
        print("value of index is",apol)
        #print("new_doc"*10)
        #print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y_true: test_label}))
        #return ase , test_label
	return apol
