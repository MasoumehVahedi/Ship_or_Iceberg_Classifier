# Ship or Iceberg Classifier

In this project, I predicted whether an image contains a ship or an iceberg. All the images are 75x75 images with two bands.

# Description

According to drifting icebergs, there is a threat for navigation and some activities in offshore. There have been plenty of companies to monitor risks of icebergs using aerial recognition and exploration. Despite the fact that, in some cases, such as harsh weather in remote areas, such techniques would not be practical, therefore, monitoring through satellite images can be considered the only method which make it feasible.

# Content

In this project, I have challenged to build some practical algorithms which automatically determine whether the classes or that remotely sensed target is a ship or iceberg. Therefore, I have been trained models including:\
1 - A Variational Autoencoders model (CNN-VAE)\
2- Transfer Learning using VGG Pre-trained model\
3- Transfer Learning using Inception-v3 Pre-trained model\
4- Transfer Learning using Resnet50\
5- Transfer Learning using VGG as Feature Extracion and PCA\
6- Gray-level co-occurrence matrix (GLCM) features and LightGBM Binary Classification\
7- Transfer Learning using VGG16 as feature extractor and eXtreme Gradient Boosting (XGBoost) classifier\
8- Fully Connected Neural Network (FCNN) model

# Data fields

train.json, test.json
The data (train.json, test.json) is presented in json format. The files consist of a list of images, and for each image, you can find the following fields:

id - the id of the image\
band_1, band_2 - the flattened image data. Each band has 75x75 pixel values in the list, so the list has 5625 elements. Note that these values are not the normal non-negative integers in image files since they have physical meanings - these are float numbers with unit being dB. Band 1 and Band 2 are signals characterized by radar backscatter produced from different polarizations at a particular incidence angle. The polarizations correspond to HH (transmit/receive horizontally) and HV (transmit horizontally and receive vertically). More background on the satellite imagery can be found here.\
inc_angle - the incidence angle of which the image was taken. Note that this field has missing data marked as "na", and those images with "na" incidence angles are all in the training data to prevent leakage.\
is_iceberg - the target variable, set to 1 if it is an iceberg, and 0 if it is a ship. This field only exists in train.json.

# Dataset
The dataset is available in Kaggle website: https://www.kaggle.com/c/statoil-iceberg-classifier-challenge/data
