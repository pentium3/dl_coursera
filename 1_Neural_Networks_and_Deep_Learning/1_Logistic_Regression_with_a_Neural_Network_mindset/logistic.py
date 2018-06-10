'''
classify cat image by logistic regression
'''

import numpy as np
import matplotlib.pyplot as plt 
import h5py
import scipy
from PIL import Image
from scipy import ndimage
from lr_utils import load_dataset

def sigmod(x):
    return (1 / (1 + np.exp(-x)))

def initialize_with_zeros(dim):
    w = np.zeros((dim,1))
    b = 0
    return (w,b)

def propagate(w, b, X, Y):
    m = X.shape[1]
    #forward propgation
    A = sigmod(np.dot(w.T, X) + b)
    J = (-1/m) * np.sum( Y * np.log(A) + (1-Y) * np.log(1-A) )
    #backward propgation
    dw = (1/m) * np.dot(X, (A - Y).T)
    db = (1/m) * np.sum(A - Y)
    assert(dw.shape == w.shape)
    assert(db.dtype == float)
    J = np.squeeze(J)
    assert(J.shape == ())
    grads = {"dw": dw , "db": db}
    return grads, J

def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost=False):
    costs = []
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)
        dw = grads["dw"]
        db = grads["db"]
        w = w - learning_rate * dw
        b = b - learning_rate * db
        #record the cost of every 100 iterations
        if(i%100 == 0):
            costs.append(cost)
            if(print_cost):
                print("cost of iteration %i == %f"%(i, cost))
    params = {"w": w , "b": b}
    grads = {"dw": dw, "db": db}
    return params, grads, costs

def predict(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((1,m))
    w = w.reshape(X.shape[0], 1)
    A = sigmod(np.dot(w.T, X)+b)
    for i in range(A.shape[1]):
        Y_prediction[0, i] = 1 if(A[0, i]>0.5) else 0
    assert(Y_prediction.shape == (1,m))
    return Y_prediction

def model(X_train, Y_train, X_test, Y_test, num_iterations=2000, learning_rate=0.5, print_cost=False):
    w, b = initialize_with_zeros(X_train.shape[0])
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost)
    w = parameters["w"]
    b = parameters["b"]
    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)
    train_acc = 100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100
    test_acc = 100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100
    print("training accuracy == ",train_acc)
    print("testing accuracy == ",test_acc)
    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
    return d

train_set_x_org, train_set_y, test_set_x_org, test_set_y, classes = load_dataset()

m_train = np.shape(train_set_x_org)[0]
m_test = np.shape(test_set_x_org)[0]
num_px = np.shape(train_set_x_org)[1]
print(m_train, m_test, num_px)

train_set_x_flatten = train_set_x_org.reshape(m_train, -1).T
test_set_x_flatten = test_set_x_org.reshape(m_test, -1).T
train_set_x = train_set_x_flatten/255
test_set_x = test_set_x_flatten/25
print(np.shape(train_set_x_org))
print(np.shape(train_set_y))
print(np.shape(test_set_x_org))
print(np.shape(test_set_y))
print(np.shape(train_set_x))
print(np.shape(test_set_x))

d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 2000, learning_rate = 0.005, print_cost = True)
