# Dominic Klusek

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.utils import to_categorical
import keras.backend as back
from keras.utils import plot_model
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import pickle

def printListByLine(data):
    for dat in data:
        print(dat)

def filePrintList(filename, data, label):
    '''
    1. filename is a reference to a file buffer
    2. data is a list of number data
    3. label is the label of the data
    '''
    filename.write(label + '\n')
    for dat in data:
        filename.write(str(dat) + '\n')

def filenameappend(activationList, batchSize, fileName = "MNIST Results", extension=".txt"):
    '''
        create a string for a filename that is the
        DatasetName + Results + ListofElements + .txt
        '''
    for i in activationList:
        if i == None:
            fileName = fileName + "None".capitalize()
        else:
            fileName = fileName + i.capitalize()
    return fileName + str(batchSize) + extension

def testname(activationList):
    returnString = ""
    for item in activationList:
        returnString = returnString + item + ' '
    return returnString

def plotlabel(activationList, optimizer, prefix):
    label = prefix
    for act in activationList:
        label = label + " " + act
    label = label + " " + optimizer
    return label

def readData(fname, numFeatures, classIndex = 0, delimeter = ' '):
    featureData = [] # create array object to hold data
    classData = []
    f = open(fname) # open file
    for line in f: # read file line for line
        lineData = line.split(delimeter) # split line by delimeter
        classData.append(int(lineData[classIndex])) # store class of features
        lineData.pop(classIndex) # remove class number from list
        if not(numFeatures == len(lineData)): #check if all features are available
            classData.pop() #remove class data from line missing feature
        else:
            tempList = [] # hold feature data
            for index in range(0, len(lineData)): #for each feature in lineData, append feature data to tempList
                tempList.append(float(lineData[index]))
            featureData.append(tempList) # append line feature data to featureData list
    f.close() # close file
    return featureData, classData #return list of features and classes X and Y respectively

# list of activation functions for each test set, of the form layer1, layer2, ..., layerN
'''
activationList = [["selu", "selu"],
                  ["selu", "sigmoid"],
                  ["selu", "softmax"],
                  ["selu", "tanh"],
                  ["selu", "selu"],
                  ["selu", "sigmoid"],
                  ["selu","softmax"],
                  ["selu", "tanh"]
]'''
'''
activationList = [["selu", "selu", "selu"],
                  ["selu", "selu", "sigmoid"],
                  ["selu", "selu", "softmax"],
                  ["selu", "selu", "tanh"],
                  ["selu", "selu", "selu"],
                  ["selu", "selu", "sigmoid"],
                  ["selu", "selu","softmax"],
                  ["selu", "selu", "tanh"]
]'''

activationList = [["selu", "selu", "selu", "selu"],
                  ["selu", "selu", "selu", "sigmoid"],
                  ["selu", "selu", "selu", "softmax"],
                  ["selu", "selu", "selu", "tanh"],
                  ["selu", "selu", "selu", "selu"],
                  ["selu", "selu", "selu", "sigmoid"],
                  ["selu", "selu", "selu","softmax"],
                  ["selu", "selu", "selu", "tanh"]
]

optimizerList = ['sgd','sgd','sgd','sgd','adam','adam','adam','adam']

# list of number of hidden layers + 1 to account for output layer
numLayers = [len(activationList[0]),len(activationList[0]),len(activationList[0]),len(activationList[0]),len(activationList[0]),len(activationList[0]),len(activationList[0]),len(activationList[0])]

# list of input and output dimensions for each layer, must be of the form [inputDimension, outputDimension]
'''
inputOutputDimensions = [[[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]],
                         [[784,784],[784,10]]]'''
'''
inputOutputDimensions = [[[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]],
                         [[784,784],[784,128],[128,10]]]'''

inputOutputDimensions = [[[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]],
                         [[784,784],[784,344],[344,128],[128,10]]]

#batchSizes = [128,128,128,128,128,128,128,128,128,128,128,128]
#batchSizes = [1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024]
batchSizes = [54000,54000,54000,54000,54000,54000,54000,54000,54000,54000,54000,54000]

# the data, split between train and test sets
(X, Y), (x_test, y_test) = mnist.load_data()

X = X.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
X = X.astype('float32')
x_test = x_test.astype('float32')
X /= 255
x_test /= 255

# convert class vectors to binary class matrices
Y = to_categorical(Y, 10)
y_test = to_categorical(y_test, 10)

# list of line colors if there are a lot of tests, that need to be graphed
lineColor = ["black", "lightcoral","maroon","coral","orange","olive","green","mediumaquamarine","dodgerblue","darkblue","crimson"]
# list of line style to go with line colors
lineStyle = ['-.', '--',':',"-"]
# a marker for each data point
marker = ["o","D","P","s"]
# index to hold place of lineColor
colorIndex = 0
# index to hold place of lineStyle
lineIndex = 0
# index to hold place of marker
markerIndex = 0
# experiment number to keep track of progress
experimentNumber = 0

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# define a number of splits and epochs for each run
numberOfSplits = 3
numberOfEpochs = 20

experimentConfusionMatrices = []

#create an instance of an excel workbook and set the row number of the data to begin at
workbook = xlsxwriter.Workbook(str(numLayers[0] - 1) + ' ' + 'MNIST Test'+str(batchSizes[0])+'Selu.xlsx', {'nan_inf_to_errors': True})
row = 2

# for every set of activation functions, create a Kfold function object, split data, get averages and errors, store in file, and then graph data
for actList, index, batch, optimizer in zip(activationList, range(0, len(activationList)), batchSizes, optimizerList):
    print("Experiment Number: {}".format(experimentNumber))
    # define 10-fold cross validation test harness
    kfold = KFold(n_splits=numberOfSplits, shuffle=True, random_state=seed)
    accuracyScores = []
    lossScores = []
    historyOfScores = []
    confusionMatrix = []

    for train, test in kfold.split(X, Y):
        # create model object
        model = Sequential()
        # for each set of dimensions in inputOutputDimensions
        for dimensions, layerIndex in zip(inputOutputDimensions[index], range(0, numLayers[index])):
            model.add(Dense(dimensions[1], input_dim=dimensions[0], activation=actList[layerIndex])) # to prevent ide from complaining, put layer output dimension first
            #if(layerIndex != numLayers[index] - 1):
               #model.add(BatchNormalization())
	    # Compile model
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['acc'])

        # Fit the model
        history = model.fit(X[train], Y[train], epochs=numberOfEpochs, batch_size=batch, validation_data=(X[test], Y[test]), verbose=0)

	    # evaluate the model
        scores = model.evaluate(x_test, y_test, verbose=1)
        
        # store results of predicition
        confused = model.predict_classes(np.array(x_test))

        #store confusion matrix for split
        confusionMatrix.append(confusion_matrix(list(np.argmax(y_test,axis=1)), list(np.array(confused)),labels=list(np.unique(np.argmax(y_test,axis=1)))))

        # store data of final accuracy and loss scores, as well as data of each epoch
        accuracyScores.append(scores[1] * 100)
        lossScores.append(scores[0])
        historyOfScores.append(history.history)
        
    confused = confusionMatrix[0]
    for i in range(1, len(confusionMatrix)):
        confused = confused + confusionMatrix[i]
    
    print(confused)

    # release model from memory
    #back.clear_session()
    print("Size of batch: {}".format(batch))
    print("Final Accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(accuracyScores), np.std(accuracyScores)))
    print("Final Loss: %.2f (+/- %.2f)" % (np.mean(lossScores), np.std(lossScores)))

    #get accuracy and loss everage of all splits
    accuracyOfAllSplitsVal = []
    lossOfAllSplitsVal = []
    errorOfAccuracyAllSplitsVal = []
    errorOfLossAllSplitsVal = []

    accuracyOfAllSplits = []
    lossOfAllSplits = []
    errorOfAccuracyAllSplits = []
    errorOfLossAllSplits = []

    for epoch in range(0, numberOfEpochs):
        '''
        1. Go through data of each split
        2. Get average and loss of each epoch for all splits
        3. Calculate errors for each epoch
        '''
        accuracyOfSplit = 0 #accuracy of a single split
        errorOfAccuracy = [] #error for accuracy
        lossOfSplit = 0 #loss of a single split
        errorOfLoss = [] #error for loss

        accuracyOfSplitVal = 0 #accuracy of a single split
        errorOfAccuracyVal = [] #error for accuracy
        lossOfSplitVal = 0 #loss of a single split
        errorOfLossVal = [] #error for loss
        for split in range(0, numberOfSplits):
            accuracyOfSplit += historyOfScores[split]['acc'][epoch] # add up all accuracy scores
            lossOfSplit += historyOfScores[split]['loss'][epoch] # add up all loss scores
            errorOfAccuracy.append(historyOfScores[split]['acc'][epoch]) # get a list of all accuracy scores for later error calculation
            errorOfLoss.append(historyOfScores[split]['loss'][epoch]) #get a list of all loss scores for later error calculation
            
            accuracyOfSplitVal += historyOfScores[split]['val_acc'][epoch] # add up all accuracy scores
            lossOfSplitVal += historyOfScores[split]['val_loss'][epoch] # add up all loss scores
            errorOfAccuracyVal.append(historyOfScores[split]['val_acc'][epoch]) # get a list of all accuracy scores for later error calculation
            errorOfLossVal.append(historyOfScores[split]['val_loss'][epoch]) #get a list of all loss scores for later error calculation
        
        accuracyOfAllSplits.append((accuracyOfSplit / numberOfSplits) * 100)
        lossOfAllSplits.append(lossOfSplit / numberOfSplits)
        errorOfAccuracyAllSplits.append(np.std(errorOfAccuracy) * 100)
        errorOfLossAllSplits.append(np.std(errorOfLoss))

        accuracyOfAllSplitsVal.append((accuracyOfSplitVal / numberOfSplits) * 100)
        lossOfAllSplitsVal.append(lossOfSplitVal / numberOfSplits)
        errorOfAccuracyAllSplitsVal.append(np.std(errorOfAccuracyVal) * 100)
        errorOfLossAllSplitsVal.append(np.std(errorOfLossVal))

    # add a worksheet for current test case
    worksheet = workbook.add_worksheet()
    # add labels to the top of each column
    worksheet.write_string(0,0, "Activation List: %s" % (testname(actList)))
    worksheet.write_string(1,0, "Accuracy Training")
    worksheet.write_string(1,1, "Accuracy Error Training")
    worksheet.write_string(1,2, "Loss Training")
    worksheet.write_string(1,3, "Loss Error Training")
    worksheet.write_string(1,4, "Accuracy Validation")
    worksheet.write_string(1,5, "Accuracy Error Validation")
    worksheet.write_string(1,6, "Loss Validation")
    worksheet.write_string(1,7, "Loss Error Validation")
    worksheet.write_string(2,10, "Batch size: %i" %(batch))
    worksheet.write_string(3,10, "Final Accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(accuracyScores), np.std(accuracyScores)))
    worksheet.write_string(4,10, "Final Loss: %.2f (+/- %.2f)" % (np.mean(lossScores), np.std(lossScores)))
    worksheet.write_string(6,10,"Confusion Matrix")
    for i in range(0, len(confused)):
        worksheet.write_row(7+i,10,confused[i])

    # create a list of all results and then write to file
    listOfResults = [accuracyOfAllSplits, errorOfAccuracyAllSplits, lossOfAllSplits, errorOfLossAllSplits, accuracyOfAllSplitsVal, errorOfAccuracyAllSplitsVal, lossOfAllSplitsVal, errorOfAccuracyAllSplitsVal]
    for col, data in enumerate(listOfResults):
        try:
            worksheet.write_column(row, col, data)
        except:
            worksheet.write_column(row, col, 'nan')

    # begin plotting gathered data into two seperate plots
    accPlotVal = plt.figure(3)
    plt.plot(range(1, numberOfEpochs+1), accuracyOfAllSplitsVal, color=lineColor[colorIndex], marker=marker[markerIndex], label=plotlabel(actList, optimizer, "Accuracy of ") , lw=3, linestyle=lineStyle[lineIndex])
    plt.xticks(np.arange(1, numberOfEpochs+1, 1))
    plt.ylabel("Accuracy %")
    plt.xlabel("Epoch")
    plt.title("MNIST Accuracy over Epoch Validation")

    lossPlotVal = plt.figure(4)
    plt.plot(range(1, numberOfEpochs+1), lossOfAllSplitsVal, color=lineColor[colorIndex], marker=marker[markerIndex], label=plotlabel(actList, optimizer, "Loss of "), lw=3, linestyle=lineStyle[lineIndex])
    plt.xticks(np.arange(1, numberOfEpochs+1, 1))
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.title("MNIST Loss over Epoch Validation")

    # increment indices for line style and color at appropriate times
    colorIndex+=1
    markerIndex+=1
    lineIndex+=1
	
    if(colorIndex == len(lineColor)):
        colorIndex = 0

    if(markerIndex == len(marker)):
        markerIndex = 0
        lineIndex = 0
    experimentNumber+=1

    # clear list
    confusionMatrix.clear()

# grid and legend activation outside of loops to prevent them from activating and deactivating
plt.figure(3)
plt.grid()
plt.legend()
plt.figure(4)
plt.grid()
plt.legend()

file = open(str(batchSizes[0]) + ' ' + str(numLayers[0] - 1) + ' Hidden Layers MNISTAccValFigSelu.pickle','wb')
pickle.dump(accPlotVal, file)
file.close()

file = open(str(batchSizes[0]) + ' ' + str(numLayers[0] - 1) + ' Hidden Layers MNISTLossValFigSelu.pickle','wb')
pickle.dump(lossPlotVal, file)
file.close()

plt.show()

workbook.close()