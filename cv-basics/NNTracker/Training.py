import os
from sklearn.model_selection import train_test_split
from utlis import *

### load data
path = 'DataCollected'
data = importDataInfo(path) #function from utlis
print(data.head())

### visualize and balance data
data = balanceData(data, display=True)

### prepare for processing
imagesPath, steering = loadData(path,data)

### split for train and test
x_train, x_val, y_train, y_val = train_test_split(imagesPath, steering, test_size = 0.2, random_state = 10)
print('Total training images: ', len(x_train))
print('Total test images: ', len(x_val))
