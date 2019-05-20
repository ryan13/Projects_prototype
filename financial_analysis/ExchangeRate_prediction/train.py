#!/usr/bin/env python3
"""
Author:  Tri Doan
Project: predict echange rate with regression with Exchange rate US/EUR data is downloaded from investing.com 

Using Multi-Layer Perceptron with Keras

"""

import conf

from keras.models import Sequential, load_model
from keras.layers import Dense

import math
import os
import sys
import pandas
import pickle

from plot import prep_tt_for_plot, plotme, plothist
from prep import get_data
from tools import get_params, train_test_split
from baseline import get_baseline

def get_mlp(inputs=1):
    """
    Create a simple Multilayer Perceptron model for regression/prediction problem.

    inputs - number of values we're using for prediction, here we're using=1
    """
    model = Sequential()
    # input_dim is s number of neurons which we we're using for prediction (just 1)
    #
    # We use a hidden layer of 1 
    #
    # Activation function is Rectified linear unit (ReLU) or Rectifier
    #
    model.add(Dense(1, input_dim=inputs, activation='relu'))
    
    model.add(Dense(1))
    return model

confs={'default': dict(model=get_mlp, inputs=1)}

def train_model(name, train_x, train_y, epochs, batches):
    """
    Get model if it exists, train if needed.
    """
    mparams=confs[name]
    model=mparams['model'](mparams['inputs'])
    # We use Loss function, or cost function as mean_squared_error
    # and Adam optimizer 
    # Metrics: mse is mean_squared_error, mape is mean_absolute_percentage_error
    #
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse','mape'])
    # Here we're starting our training
    history=model.fit(train_x, train_y, verbose=2, epochs=epochs, batch_size=batches)
    return model, name, mparams, history

if __name__ == '__main__':
   
    years, past_values, values=get_data()
    
    X, Y = past_values, values
    # Split data into training, testing
    # Test part won't be seen by a model during training so it will
    # give us some idea how our model performs on a unseen data.
    train_x, train_y, test_x, test_y = train_test_split(X, Y)
    # Getting command line parameters
    name, epochs, batches, plot=get_params()
    # Do the training
    model, name, mp, history=train_model(name, train_x, train_y, epochs, batches)
    # Save models and the training history for later use
    mname='models/model-%s-%d-%d' % (name, epochs, batches)

    # Save model in pickle file
    model.save(mname+'.h5')
    with open(mname+'-history.pickle', 'wb') as ms:
        pickle.dump(history.history, ms)
    print()
    print('Model and its history saved in %s*' % mname)
    title='%s (epochs=%d, batch_size=%d)' % (name, epochs, batches)
    # Test our model on both data that has been seen (training ) and unseen (testing)
    print('Scores for %s' % title)

    train_score = model.evaluate(train_x, train_y, verbose=0)

    print('List of model''s metric ',model.metrics_names)
    print('RMSE = %e '%math.sqrt(train_score[1]))

    #trscore='RMSE: %e MAPE: %e%%' % ("{:,.0f}".format(math.sqrt(train_score[1])), train_score[2])
    print('Train Score: RMSE: %e MAPE: %e  ' % (math.sqrt(train_score[1]), train_score[2]))
    
    test_score = model.evaluate(test_x, test_y, verbose=0)
    
    #tscore='RMSE: %e MAPE: %.e%%' % ("{:,.0f}".format(math.sqrt(test_score[1])), test_score[2])
       
    print('Test Score: RMSE: %e MAPE: %.e%%' % (math.sqrt(test_score[1]),test_score[2]))
    print('\n')
    # Get our baseline prediction
    # Our baseline is simply a mse of the difference between values from X and Y
    baseline=get_baseline()
    if plot == 'plot':
        train_plot, test_plot=prep_tt_for_plot(model, years, train_x, train_y, test_x, test_y)
        plotme(values, years, train_x=train_plot, test_x=test_plot, baseline=baseline[1], bttscore=baseline[3], trscore=trscore, tscore=tscore, title=title)
    elif plot == 'ploth':
        plothist(history)
