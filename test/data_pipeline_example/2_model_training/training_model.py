import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from io import StringIO
#from torchvision import model_selection
import torch 
from base_model import Model
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
import numpy as np 
import json 

def load_data(data):

    d = StringIO(data)
    iris = pd.read_csv(d, sep=',')
    print(iris.shape)
    return iris

def get_train_test_data(iris):

    encode = LabelEncoder()
    iris.Species = encode.fit_transform(iris.Species)

    train , test = train_test_split(iris, test_size=0.2, random_state=0)
    print('shape of training data : ', train.shape)
    print('shape of testing data', test.shape)


    X_train = train.drop(columns=['Species'], axis=1)
    y_train = train['Species']
    X_test = test.drop(columns=['Species'], axis=1)
    y_test = test['Species']

    return np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)


if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '--data',
        type=str, 
        help="Input data csv"
    )

    argument_parser.add_argument(
        '--name',
        type=str, 
        help="Input data csv"
    )

    args = argument_parser.parse_args()
    iris = args.data
    iris = load_data(iris)

    X_train, X_test, y_train, y_test = get_train_test_data(iris)

    # model = LogisticRegression()
    # model.fit(X_train, y_train)
    # predict = model.predict(X_test)
    # print('\nAccuracy Score on test data : ')
    # print(accuracy_score(y_test, predict))
    model = Model(X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn =  torch.nn.CrossEntropyLoss()
    model

    import tqdm

    EPOCHS  = 100000000
    X_train = Variable(torch.from_numpy(X_train)).float()
    y_train = Variable(torch.from_numpy(y_train)).long()
    X_test  = Variable(torch.from_numpy(X_test)).float()
    y_test  = Variable(torch.from_numpy(y_test)).long()

    loss_list     = np.zeros((EPOCHS,))
    accuracy_list = np.zeros((EPOCHS,))

    for epoch in range(EPOCHS):
        y_pred = model(X_train)
        loss = loss_fn(y_pred, y_train)
        loss_list[epoch] = loss.item()
        
        # Zero gradients
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 20==0:
            with torch.no_grad():
                y_pred = model(X_test)
                correct = (torch.argmax(y_pred, dim=1) == y_test).type(torch.FloatTensor)
                accuracy_list[epoch] = correct.mean()
                print(f'args_name: {args.name} Epoch[{epoch}] : loss:{loss},  Accuracy:{correct.mean()}')
                print(f'args_name : {args.name} Epoch[{int(epoch)}] : loss:{float(loss)},  Accuracy:{correct.mean()}')
                d = {'Deep_learning_Epoch': int(epoch), 'loss': float(loss)}
                print(json.dumps(d))

