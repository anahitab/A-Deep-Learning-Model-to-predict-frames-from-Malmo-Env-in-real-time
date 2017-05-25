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




class base_Model:
    
    def __init__( self, final_images, fin_lab,FLAGS):
        self.img_size = FLAGS.img_size
	self.num_channels = FLAGS.num_channels
        self.num_classes = FLAGS.num_classes
        self.img_size_flat = FLAGS.img_size_flat
	self.train_batch_size= FLAGS.train_batch_size
	self.num_filters1 = FLAGS.num_filters1
	self.num_filters2 = FLAGS.num_filters2
	self.num_filters3 = FLAGS.num_filters3
	self.fc_size = FLAGS.fc_size
	self.filter_size1 = FLAGS.filter_size1

	
        self.save_dir = FLAGS.save_dir
        self.final_images , self.fin_lab  = final_images , fin_lab
        self.num_epochs = FLAGS.num_epochs
        self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.build()
        self.saver = tf.train.Saver(tf.all_variables())
            
    def build(self):
        raise NotImplementedError()
    
    def train_batch(self, sess, batch):
        feed_dict = self.get_feed_dict(batch, is_train=True)
        return sess.run([self.opt_op, self.global_step], feed_dict=feed_dict)

    def test_batch(self, sess, batch):
        feed_dict = self.get_feed_dict(batch, is_train=False)
        return sess.run([self.num_corrects, self.total_loss, self.global_step], feed_dict=feed_dict)

    
    def optimize(self,sess):
        
        #total_iterations = 0; global total_iterations
        
        for i in range(self.num_epochs):
            self.step = 0
            tep = 0
            d_iter = data_iterator(self.final_images , self.fin_lab)
            while tep<622:
                tep+=1
                self.step+=1
                x_batch , y_batch = d_iter.next_batch(self.train_batch_size)
                x_batch = np.reshape(x_batch,[self.train_batch_size, self.img_size_flat])
                feed_dict_train = {self.x: x_batch, self.y_true: y_batch}
                
                _, global_step = sess.run([self.opt_op, self.global_step], feed_dict=feed_dict_train)
                #session.run(self.optimizer, feed_dict=feed_dict_train)
                
                if self.step%4==0:
                    self.save(sess)
                #print("global step is",self.global_step)
        print("Training completed.")

    def save(self, sess):
        print("Saving model to %s" % self.save_dir)
        checkpoint_prefix = os.path.join(self.save_dir, "model")
        self.saver.save(sess, checkpoint_prefix, global_step=self.global_step )

    def load(self, sess):
        print("Loading model ...")
        checkpoint = tf.train.get_checkpoint_state(self.save_dir)
        if checkpoint is None:
            print("Error: No saved model found. Please train first.")
            sys.exit(0)
        self.saver.restore(sess, checkpoint.model_checkpoint_path)

class img_Model(base_Model):
    
    def build(self):
        
        #img_size=128; num_channels=4;num_classes=23
        #filter_size1 = 3 ; num_filters1 = 32;
        #filter_size2 = 3 ; num_filters2 = 32;
        #filter_size3 = 3 ; num_filters3 = 64;

        #fc_size = 128 ; num_channels = 4
        #img_size_flat = img_size * img_size * num_channels
        #img_shape = (img_size, img_size)

        
        
        self.x = tf.placeholder(tf.float32, shape=[None, self.img_size_flat], name='x')
        self.x_image = tf.reshape(self.x, [-1, self.img_size, self.img_size, self.num_channels])
        self.y_true = tf.placeholder(tf.float32, shape=[None, self.num_classes], name='y_true')
        self.y_true_cls = tf.argmax(self.y_true, dimension=1)
        
        layer_conv1, weights_conv1 = new_conv_layer(input=self.x_image,
                                                    num_input_channels=self.num_channels,
                                                    filter_size=self.filter_size1,
                                                    num_filters=self.num_filters1,
                                                    use_pooling=True)

        layer_conv2, weights_conv2 = new_conv_layer(input=layer_conv1,
                                                    num_input_channels=self.num_filters1,
                                                    filter_size=self.filter_size1,
                                                    num_filters=self.num_filters2,
                                                    use_pooling=True)

        layer_conv3, weights_conv3 = new_conv_layer(input=layer_conv2,
                                                    num_input_channels=self.num_filters2,
                                                    filter_size=self.filter_size1,
                                                    num_filters=self.num_filters3,
                                                    use_pooling=True)
        
        layer_flat, num_features = flatten_layer(layer_conv3)
        
        layer_fc1 = new_fc_layer(input=layer_flat,
                                 num_inputs=num_features,
                                 num_outputs=self.fc_size,
                                 use_relu=True)
        
        layer_fc2 = new_fc_layer(input=layer_fc1,
                                 num_inputs=self.fc_size,
                                 num_outputs=self.num_classes,
                                 use_relu=False)
        
        self.y_pred = tf.nn.softmax(layer_fc2)
        
        self.y_pred_cls = tf.argmax(self.y_pred, dimension=1)
        
        #print(self.y_pred_cls)
        
        self.cross_entropy = tf.nn.softmax_cross_entropy_with_logits( logits = layer_fc2, labels = self.y_true)
        self.cost = tf.reduce_mean(self.cross_entropy)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
        self.opt_op = self.optimizer.minimize(self.cost,global_step=self.global_step)
        self.correct_prediction = tf.equal(self.y_pred_cls, self.y_true_cls)
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
        #session.run(tf.global_variables_initializer())


