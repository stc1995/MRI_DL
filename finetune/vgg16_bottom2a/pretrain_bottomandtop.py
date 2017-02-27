from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.applications.vgg16 import VGG16
from keras.layers.convolutional import MaxPooling2D, ZeroPadding2D, Convolution2D
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras import optimizers
import numpy as np
import random

# npy_path = './Material/old_0.npy'
# temp = np.load(npy_path)
# temp = np.expand_dims(temp, axis=0)
# temp = preprocess_input(temp)
# temp = temp[0]
# oldData = [temp]
# print(temp.shape)
# print(type(temp))
# for i in range(1, 98):
#     npy_path = './Material/old_%d.npy' % i
#     print(npy_path)
#     temp = np.load(npy_path)
#     temp = np.expand_dims(temp, axis=0)
#     temp = preprocess_input(temp)
#     temp = temp[0]
#     oldData.append(temp)
#
# oldData = np.array(oldData)
# print(oldData.shape)  # (98, 1, 7, 7, 512)
# # np.save('old_features.npy', features)
#
#
# npy_path = './Material/ad_0.npy'
# temp = np.load(npy_path)
# temp = np.expand_dims(temp, axis=0)
# temp = preprocess_input(temp)
# temp = temp[0]
# adData = [temp]
# print(temp.shape)
# print(type(temp))
# for i in range(1, 100):
#     npy_path = './Material/ad_%d.npy' % i
#     print(npy_path)
#     temp = np.load(npy_path)
#     temp = np.expand_dims(temp, axis=0)
#     temp = preprocess_input(temp)
#     temp = temp[0]
#     adData.append(temp)
#
# adData = np.array(adData)
# print(adData.shape)  # (98, 1, 7, 7, 512)
# # np.save('old_features.npy', features)
# np.save('adData.npy', adData)
# np.save('oldData.npy', oldData)
#
ad_num = 100
old_num = 98
seed = 10
#####################################################################################################
#####################################################################################################
random.seed(seed)
#####################################################################################################
######################## #############################################################################
adData = np.load('adData.npy')
oldData = np.load('oldData.npy')

temp = list(range(ad_num))
random.shuffle(temp)
ad_train_num = temp[0: int(ad_num * 0.7)]
ad_test_num = temp[int(ad_num * 0.7):]
ad_train = []
ad_test = []
for i in ad_train_num:
    ad_train.append(adData[i])
for j in ad_test_num:
    ad_test.append(adData[j])
ad_train = np.array(ad_train)
ad_test = np.array(ad_test)

del adData

temp = list(range(old_num))
random.shuffle(temp)
old_train_num = temp[0: int(old_num * 0.7)]
old_test_num = temp[int(old_num * 0.7):]
old_train = []
old_test = []
for i in old_train_num:
    old_train.append(oldData[i])
for j in old_test_num:
    old_test.append(oldData[j])
old_train = np.array(old_train)
old_test = np.array(old_test)

del oldData

train_data = np.concatenate((ad_train, old_train))
del ad_train
del old_train
validation_data = np.concatenate((ad_test, old_test))
del ad_test
del old_test
print(train_data.shape)
print(validation_data.shape)

# the features were saved in order, so recreating the labels is easy
train_labels = np.concatenate(([[0, 1]] * 70, [[1, 0]] * 68))
validation_labels = np.concatenate(([[0, 1]] * 30, [[1, 0]] * 30))
print(train_labels.shape)
print(validation_labels.shape)


bottom_model = Sequential()
bottom_model.add(ZeroPadding2D((1, 1), input_shape=(224, 224, 81)))
bottom_model.add(Convolution2D(32, 3, 3, activation='relu', name='conv0_1'))
bottom_model.add(ZeroPadding2D((1, 1)))
bottom_model.add(Convolution2D(3, 3, 3, activation='relu', name='conv0_2'))

base_model = Sequential()
base_model.add(ZeroPadding2D((1, 1), input_shape=(224, 224, 3)))

base_model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
base_model.add(MaxPooling2D((2, 2), strides=(2, 2)))

base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
base_model.add(MaxPooling2D((2, 2), strides=(2, 2)))

base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_1'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_2'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_3'))
base_model.add(MaxPooling2D((2, 2), strides=(2, 2)))

base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_1'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_2'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_3'))
base_model.add(MaxPooling2D((2, 2), strides=(2, 2)))

base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_1'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_2'))
base_model.add(ZeroPadding2D((1, 1)))
base_model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_3'))
base_model.add(MaxPooling2D((2, 2), strides=(2, 2)))
base_model.load_weights('/home/stc/.keras/models/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')

top_model = Sequential()
top_model.add(BatchNormalization(input_shape=(1, 7, 7, 512)))
top_model.add(Flatten())
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(2, activation='softmax'))

bottom_model.add(base_model)
bottom_model.add(top_model)

for layer in bottom_model.layers[4].layers:
    layer.trainable = False

# model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
bottom_model.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

bottom_model.fit(train_data, train_labels, nb_epoch=19, batch_size=5, shuffle=True,
                 validation_data=(validation_data, validation_labels))
bottom_model.save_weights('bottom2_model.h5')





