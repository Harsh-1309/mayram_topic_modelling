from multiprocessing import pool
import os
from constants import *
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras import Input
import numpy as np
import json
import pickle
from tqdm import tqdm
# from multiprocessing import Pool


# load the data arrays that were previously saved
x_train=np.load("data/x_train.npy")
y_train=np.load("data/y_train.npy")

# load word2int previosuly saved
f = open("data/word2int.json","r")
word2int = dict(json.load(f))
f.close()

# set optimizers
opt_adam=tf.optimizers.Adam()
opt_sgd=tf.optimizers.SGD()

"""
DO NOT CHANGE DTYPE TO FLOAT32. CRASHES RANDOMLY.
ALSO, NEED TO DEFINE CUSTOM SOFTMAX WITH SHIFT AS 
SYSTEM CANT HANDLE EXPONENTS OF LARGE NUMBERS WHICH 
IS USED IN SOFTMAX FUNCTION
"""
def smi(x):
    # B = np.exp(x - max(x))
    return np.exp(x - max(x))/np.sum(np.exp(x - max(x)))
    # return B/C


def train(x_train,y_train,optimizer=opt_sgd):

    # initialise the weights and biases for both the layers.
    # w1,b1 for between input layer and hidden layer, hence shape [input,hidden]
    # w2,b2 for between hidden layer and output layer, hence shape is [hidden,output]
    # more weights and biases need to be added if hidden layers are increased 

    w1=tf.Variable(tf.random.normal([VOCAB_SIZE,DIMENSION],dtype="float64"),dtype="float64")
    b1=tf.Variable(tf.random.normal([DIMENSION],dtype="float64"),dtype="float64")
    w2=tf.Variable(tf.random.normal([DIMENSION,VOCAB_SIZE],dtype="float64"),dtype="float64")
    b2=tf.Variable(tf.random.normal([VOCAB_SIZE],dtype="float64"),dtype="float64")
    

    # iterate over epochs for updating weights and biases
    for _ in range(EPOCHS):
        # use GradientTape to watch tensors in context
        with tf.GradientTape() as t:
            # update w1,b1
            hidden_layer=tf.add(tf.matmul(x_train,w1),b1)
            output_layer = tf.nn.softmax(tf.add( tf.matmul(hidden_layer,w2),b2))
            cross_entropy_loss = tf.reduce_mean(-tf.math.reduce_sum(y_train * tf.math.log(output_layer), axis=[1]))
  
            grads = t.gradient(cross_entropy_loss, [w1,b1,w2,b2])
            optimizer.apply_gradients(zip(grads,[w1,b1,w2,b2]))

            # log the training loss 
            if(_ % 5 == 0):
                print("loss: ", cross_entropy_loss)

    return w1,b1

# get final word embeddings from w,b and word2int 
def get_vector(w,b,word_idx):
    return(w+b)[word_idx]

# start the training process

np.random.seed(5)
np.random.shuffle(x_train)

np.random.seed(5)
np.random.shuffle(y_train)

w,b=train(x_train,y_train)
print(f"\nTraining complete with {EPOCHS} epochs\n")

# pickle and save the weights and biases
with open("saved_weights/w","wb") as f:
    pickle.dump(w,f)

with open("saved_weights/b","wb") as f:
    pickle.dump(b,f)

print("weights abd biases saved at 'saved_weights/'")

"""
Sample output of embedding for word "used":

tf.Tensor(
[ 3.307526    1.2745522   0.6221365   1.0608096  -1.3911397  -2.7389529
 -0.03785023 -1.6968094   0.61216784  0.995255  ], shape=(10,), dtype=float32)

Shape will be dimension dependent
"""

#generate and save all word embeddings
all_words=list(word2int.keys())
word_embeddings={}

for word in all_words:
    word_embeddings[word]=list(np.asarray(get_vector(w,b,word2int[word])))

with open("saved_embeddings/generated_embeddings.json","w") as f:
    json.dump(word_embeddings,f)

print("all word embeddings saved at 'saved_embeddings/generated_embeddings.json")