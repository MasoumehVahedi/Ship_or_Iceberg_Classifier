# -*- coding: utf-8 -*-
"""vgg16_and_vgg19_as_feature_extractor_and_PCA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yK57-GV-8R9i5W546A7BgK7RMSUxvZmm

**Import libraries**
"""

import numpy as np
import pandas as pd
import seaborn as sns
import datetime
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from keras.utils import to_categorical
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19

"""**Load the dataset and data exploratory**"""

#Load dataset
df_train = pd.read_json("/content/drive/MyDrive/train.json")
df_train.head()

print(df_train.shape)

print(df_train.info())

# MISSING VALUES:
#NOTE: we want to find "Nan" filds and replace it
df_train.inc_angle.replace({"na":np.nan}, inplace=True)
# Drop the rows that has NaN value for inc_angle
df_train.drop(df_train[df_train["inc_angle"].isnull()].index, inplace=True)

iceberg_size = df_train["is_iceberg"].value_counts(sort=1)
plt.pie(iceberg_size, autopct = "%1.1f%%")
plt.show()

def prepare_data(df):
    X_band_1 = []
    X_band_2 = []
    
    for band in df["band_1"]:
        #Convert to float32
        band_1 = np.array(band).astype(np.float32)
        #Reshaping band_1 and band_2
        band_1 = band_1.reshape(75,75)
        X_band_1.append(band_1)
        
    for band in df["band_2"]:
         #Convert to float32
        band_2 = np.array(band).astype(np.float32)
        #Reshaping band_1 and band_2
        band_2 = band_2.reshape(75,75)
        X_band_2.append(band_2)
        
    #Convert list to numpy array
    X_band_1 = np.array(X_band_1)
    X_band_2 = np.array(X_band_2)
    
    # Rescale
    X_band_1 = (X_band_1 - X_band_1.mean()) / (X_band_1.max() - X_band_1.min())
    X_band_2 = (X_band_2 - X_band_2.mean()) / (X_band_2.max() - X_band_2.min())
    
    #Concatenate band_1 and band_2 to create X for training (or test)
    X = np.concatenate([X_band_1[:, :, :, np.newaxis], 
                        X_band_2[:, :, :, np.newaxis],((X_band_1+X_band_2)/2)[:, :, :, np.newaxis]], 
                        axis=-1)
    
    Y = np.array(df["is_iceberg"])
    
    return X, Y

# Load X and Y
X, Y = prepare_data(df_train)

print("X shape is:{}".format(X.shape))
print("Y shape is:{}".format(Y.shape))

""" **Transfer learning using VGG16 as feature extraction and PCA**"""

SIZE = 75

# Split data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

print("X_train shape is:{}".format(X_train.shape))
print("Y_train shape is:{}".format(Y_train.shape))
print("X_test shape is:{}".format(X_test.shape))
print("Y_test shape is:{}".format(Y_test.shape))

# Normalize and reshape
X_train = X_train.astype("float32")
X_test = X_test.astype("float32")
X_train = X_train / 255
X_test = X_test / 255

# One hot encoding
y_train_one_hot = to_categorical(Y_train)
y_test_one_hot = to_categorical(Y_test)

# Load VGG model
vgg_model = VGG16(weights="imagenet", include_top=False, input_shape=(SIZE, SIZE, 3))
vgg_model.summary()

# Make Loaded layers as non-trainable
for layer in vgg_model.layers:
    layer.trainable = False
    
vgg_model.summary()

# Now we want to use features from convolutional network (vgg16) for random forest model
feature_vgg16 = vgg_model.predict(X_train)
feature_vgg16 = feature_vgg16.reshape(feature_vgg16.shape[0], -1)

"""**PCA**

**1- PCA model with vgg16 feature**
"""

scaler = StandardScaler()
scaler = scaler.fit_transform(feature_vgg16)

# PCA model
pca_model = PCA(whiten=True)
# Fit the model
pca_model.fit(scaler)

print('variation ratio: {}'.format(pca_model.explained_variance_ratio_))
print('variations: {}'.format(pca_model.explained_variance_))
print('Components: {}'.format(pca_model.components_))

# Plotting
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("n_components")
ax.set_ylabel("explained variance")
ax.set_xlim(0,100)
ax.set_ylim(0,10)
ax.plot(pca_model.explained_variance_)

"""**2- PCA model with vgg16 feature**"""

scaler = StandardScaler()
scaler = scaler.fit_transform(feature_vgg16)

# PCA model
pca_model = PCA(n_components=2)
# Fit_transform the model
components = pca_model.fit_transform(scaler)

print('variation ratio: {}'.format(pca_model.explained_variance_ratio_))
print('variations: {}'.format(pca_model.explained_variance_))
print('Components: {}'.format(pca_model.components_))

# Show two pca components as a data frame
df = pd.DataFrame(data = components, columns = ['principal component 1', 'principal component 2'])
print(df.head())

# Visualizing two pca components

plt.figure(figsize=(10,10))
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
colors = {0: 'r', 1:'g'}.items()
for cat, color in colors:
  plt.scatter(df.loc[df_train.is_iceberg==cat ,'principal component 1'], 
              df.loc[df_train.is_iceberg==cat ,'principal component 2'], c = color, s = 50)

plt.legend([_[0] for _ in colors],prop={'size': 15})
plt.show()

"""**Transfer learning using VGG19 as feature extraction and PCA**"""

# Load VGG model
vgg19_model = VGG19(weights="imagenet", include_top=False, input_shape=(SIZE, SIZE, 3))
vgg19_model.summary()

# Make Loaded layers as non-trainable
for layer in vgg19_model.layers:
    layer.trainable = False
    
vgg19_model.summary()

# Now we want to use features from convolutional network (vgg16) for random forest model
feature_vgg19 = vgg_model.predict(X_train)
feature_vgg19 = feature_vgg19.reshape(feature_vgg19.shape[0], -1)

"""**PCA**

**1- PCA model with vgg16 feature**
"""

scaler = StandardScaler()
scaler = scaler.fit_transform(feature_vgg19)

# PCA model
pca_model = PCA(whiten=True)
# Fit the model
pca_model.fit(scaler)

print('variation ratio: {}'.format(pca_model.explained_variance_ratio_))
print('variations: {}'.format(pca_model.explained_variance_))
print('Components: {}'.format(pca_model.components_))

# Plotting
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("n_components")
ax.set_ylabel("explained variance")
ax.set_xlim(0,100)
ax.set_ylim(0,10)
ax.plot(pca_model.explained_variance_)

"""**2- PCA model with vgg16 feature**"""

scaler = StandardScaler()
scaler = scaler.fit_transform(feature_vgg19)

# PCA model
pca_model = PCA(n_components=2)
# Fit_transform the model
components = pca_model.fit_transform(scaler)

print('variation ratio: {}'.format(pca_model.explained_variance_ratio_))
print('variations: {}'.format(pca_model.explained_variance_))
print('Components: {}'.format(pca_model.components_))

df = pd.DataFrame(data=components, columns=["principal component 1", "principal component 2"])
df.head()

# Visualizing two pca components

plt.figure(figsize=(10,10))
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
colors = {0: 'r', 1:'g'}.items()
for cat, color in colors:
    plt.scatter(df.loc[df_train.is_iceberg==cat ,'principal component 1'], 
                df.loc[df_train.is_iceberg==cat ,'principal component 2'], c = color, s = 50)

plt.legend([_[0] for _ in colors],prop={'size': 15})
plt.show()