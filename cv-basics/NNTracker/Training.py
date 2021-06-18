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

### augment data
# this step is included in the dataGen() func
### preprocess
# this step is included in the dataGen() func

### create model and train
model = createModel()
train = model.fit(dataGen(x_train, y_train, 100, 1), steps_per_epoch=100, epochs=10, validation_data=dataGen(x_val, y_val, 50, 0), validation_steps=50 )

### save model
model.save('model.h5')
print('Model saved')

### plot result
plt.plot(train.history['loss'], label='Loss', marker='.')
plt.plot(train.history['val_loss'], label='Val loss', marker='o')
plt.legend()
plt.title('Loss over epochs')
plt.xlabel('Epochs')
plt.show()

