import pickle
import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
 
 
with open('X.pkl', 'rb') as f:
    xTrain = pickle.load(f)
with open('X_test.pkl', 'rb') as f:
    xTest = pickle.load(f)

with open('y.pkl', 'rb') as f:
    y = pickle.load(f)
    
print(y)

model= Sequential([
	Input(shape=(80,80,3)),
  	Conv2D(64, (3, 3),activation='relu',padding='same'),
  	Conv2D(32, (3, 3),activation='relu',padding='same'),
  	MaxPooling2D((2, 2), strides=(2, 2)),
      	Dense(8, activation='relu',),
      	Dropout(0.5),
      	Flatten(),
      	Dense(1, activation='sigmoid'),
      	
])



model.compile(loss = "binary_crossentropy" ,optimizer='adam', metrics=['accuracy'])


print(xTrain.shape)


model.fit(xTrain, y, epochs=50, batch_size=10)

k = model.evaluate(xTrain,y)
print(k)
model.save('giveme.h5')
