#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 16:40:48 2018

@author: jiahzhao
"""
import os
import time
import tensorflow as tf
import tensorlayer as tl


import numpy as np

X_train = np.load('/home/jiahzhao/Desktop/cancer classification/x_train_triple.npy')
X_val = np.load('/home/jiahzhao/Desktop/cancer classification/x_test_triple.npy')
y_train = np.load('/home/jiahzhao/Desktop/cancer classification/y_train_triple.npy')
y_val = np.load('/home/jiahzhao/Desktop/cancer classification/y_test_triple.npy')

rootdir='/home/jiahzhao/Desktop/result for houses-ALL/lung-nodule-result'

result_list=os.listdir(rootdir)

for ii in range(0,len(result_list)):
    
    tf.reset_default_graph()

    path=os.path.join(rootdir,result_list[ii])
    result_name=os.path.basename(path)
    
    print(result_name)
    if result_name[-3:]=='txt':
    
       hp_setting=np.loadtxt(path,delimiter=',')
    elif result_name[-3:]=='npy':
       hp_setting=np.load(path)
    
    hp_setting=np.round(hp_setting)
    
        
        
    conv1_1=hp_setting[0]
    conv1_2=hp_setting[1]
    conv2_1=hp_setting[2]
    conv2_2=hp_setting[3]    
    conv3_1=hp_setting[4]
    conv3_2=hp_setting[5]        
    drop_out_rate1=hp_setting[6]*0.01
    dense1=hp_setting[7]
    drop_out_rate2=hp_setting[8]*0.01
    
    
    
    
    
    sess = tf.InteractiveSession()
    
    batch_size = 50
    
    x = tf.placeholder(tf.float32, shape=[batch_size, 52, 52])
    y_ = tf.placeholder(tf.float32, shape=[batch_size,3])
    
    
    def model(x, is_train=True, reuse=False):
        # In BNN, all the layers inputs are binary, with the exception of the first layer.
        # ref: https://github.com/itayhubara/BinaryNet.tf/blob/master/models/BNN_cifar10.py
        with tf.variable_scope("binarynet", reuse=reuse):
    
            net= tl.layers.InputLayer(x, name='input')
            net = tl.layers.ExpandDimsLayer(net,axis=3,name='add')
            net = tl.layers.BatchNormLayer(net, act=tf.nn.relu, is_train=is_train, name='bn0')
            
            
            net1 = tl.layers.Conv2dLayer(net,
                               act = tf.identity,
                               shape = [3, 3, 1, conv1_1],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer1_1')
            net1 = tl.layers.BatchNormLayer(net1, act=tl.act.htanh, is_train=is_train, name='bn1_1')
            net1 = tl.layers.MaxPool2d(net1, (2, 2), (2, 2), padding='SAME', name='pool1_1')
            # net = tl.layers.SignLayer(net)
            net1 = tl.layers.Conv2dLayer(net1,
                               act = tf.identity,
                               shape = [3, 3, conv1_1, conv1_2],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer1_2')
            net1 = tl.layers.BatchNormLayer(net1, act=tl.act.htanh, is_train=is_train, name='bn1_2')
            net1 = tl.layers.MaxPool2d(net1, (7, 7), (7, 7), padding='SAME', name='pool1_2')
    
            net1 = tl.layers.FlattenLayer(net1)
            net1 = tl.layers.DropoutLayer(net1, keep=drop_out_rate1, is_fix=True, is_train=is_train, name='drop1')
          
            net2 = tl.layers.Conv2dLayer(net,
                               act = tf.identity,
                               shape = [5, 5, 1, conv2_1],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer2_1')
            net2 = tl.layers.BatchNormLayer(net2, act=tl.act.htanh, is_train=is_train, name='bn2_1')
            net2 = tl.layers.MaxPool2d(net2, (2, 2), (2, 2), padding='SAME', name='pool2_1')
            # net = tl.layers.SignLayer(net)
            net2 = tl.layers.Conv2dLayer(net2,
                               act = tf.identity,
                               shape = [5, 5, conv2_1, conv2_2],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer2_2')
            net2 = tl.layers.BatchNormLayer(net2, act=tl.act.htanh, is_train=is_train, name='bn2_2')
            net2 = tl.layers.MaxPool2d(net2, (7, 7), (7, 7), padding='SAME', name='pool2_2')
    
            net2 = tl.layers.FlattenLayer(net2)
            net2 = tl.layers.DropoutLayer(net2, keep=drop_out_rate1, is_fix=True, is_train=is_train, name='drop2')        
            
         
              
            net3 = tl.layers.Conv2dLayer(net,
                               act = tf.identity,
                               shape = [7, 7, 1, conv3_1],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer3_1')
            net3 = tl.layers.BatchNormLayer(net3, act=tl.act.htanh, is_train=is_train, name='bn3_1')
            net3 = tl.layers.MaxPool2d(net3, (2, 2), (2, 2), padding='SAME', name='pool3_1')
            # net = tl.layers.SignLayer(net)
            net3 = tl.layers.Conv2dLayer(net3,
                               act = tf.identity,
                               shape = [7, 7, conv3_1, conv3_2],
                               padding='SAME',
                               W_init=tf.truncated_normal_initializer(stddev=5e-2),
                               W_init_args={},
                               b_init = tf.constant_initializer(value=0.0),
                               b_init_args = {},
                               name ='conv_layer3_2')
            net3 = tl.layers.BatchNormLayer(net3, act=tl.act.htanh, is_train=is_train, name='bn3_2')
            net3 = tl.layers.MaxPool2d(net3, (7, 7), (7, 7), padding='SAME', name='pool3_2')
    
            net3 = tl.layers.FlattenLayer(net3)
            net3 = tl.layers.DropoutLayer(net3, keep=drop_out_rate1, is_fix=True, is_train=is_train, name='drop3')      
            
            
            net = tl.layers.ConcatLayer([net1,net2,net3],1,name='concat_layer_all')
         
            net = tl.layers.DenseLayer(net, dense1, b_init=None, name='dense')
            net = tl.layers.DropoutLayer(net, keep=drop_out_rate2, is_fix=True, is_train=is_train, name='drop')
            net = tl.layers.DenseLayer(net, n_units=3,
                                     act = tf.identity,
                                     name='output_layer')
    
        return net
    
    
    # define inferences
    net_train = model(x, is_train=True, reuse=False)
    net_test = model(x, is_train=False, reuse=True)
    
    # cost for training
    y = net_train.outputs
    cost =  tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y, labels=y_), name='xentropy')
    
    
    # cost and accuracy for evalution
    y2 = net_test.outputs
    cost_test = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y2, labels=y_), name='xentropy2')
    
    correct_prediction = tf.equal(tf.argmax(y2,1), tf.argmax(y_,1))
    
    
    
    acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    # define the optimizer
    train_params = tl.layers.get_variables_with_name('binarynet', True, True)
    train_op = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost, var_list=train_params)
    
    # initialize all variables in the session
    tl.layers.initialize_global_variables(sess)
    
    net_train.print_params()
    net_train.print_layers()
    
    n_epoch = 300
    
    
    # print(sess.run(net_test.all_params)) # print real values of parameters
    record=np.zeros((1,5))#####save a  set with n(epoches+1)row 5 clomn(epoch,trainloss trainacc,testloss,testacc)
    
    
    for epoch in range(1,n_epoch+1):
        start_time = time.time()
        for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
            sess.run(train_op, feed_dict={x: X_train_a, y_: y_train_a})
    
        print("Epoch %d of %d took %fs" % (epoch, n_epoch, time.time() - start_time))
        train_loss, train_acc, n_batch = 0, 0, 0
        for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
            err, ac = sess.run([cost_test, acc], feed_dict={x: X_train_a, y_: y_train_a})
            train_loss += err
            train_acc += ac
            n_batch += 1
    
        print("   train loss: %f" % (train_loss / n_batch))
        print("   train acc: %f" % (train_acc / n_batch))
        
        train_loss=  train_loss/n_batch                  
        train_acc=train_acc/n_batch    
        
        val_loss, val_acc, n_batch = 0, 0, 0
        for X_val_a, y_val_a in tl.iterate.minibatches(X_val, y_val, batch_size, shuffle=True):
            err, ac = sess.run([cost_test, acc], feed_dict={x: X_val_a, y_: y_val_a})
            val_loss += err
            val_acc += ac
            n_batch += 1
        print("   val loss: %f" % (val_loss / n_batch))
        print("   val acc: %f" % (val_acc / n_batch))
        val_loss= val_loss / n_batch
        val_acc=val_acc / n_batch           
        
        record_e=[[epoch,train_loss,train_acc,val_loss,val_acc]]
        
        print(record_e)
        print(record)
        record=np.concatenate((record,record_e),axis=0)
        print(record)
    record=record[1:,] 
    print('epoch,train_loss,train_acc,val_loss,val_acc') 
    print(record)
    
    sname='saved_result_'+result_name+'.txt'

    np.savetxt(sname,record)