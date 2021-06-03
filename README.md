# skin-cancer-classification
Mobile application prototype skin cancer classification project for Bangkit's final project assignment.

# Model
This model use .h5 extension and you can download the model [here](https://github.com/Cipaduduck/skin-cancer-classification/blob/main/backend/model.h5).
You can see the notebook [here](https://github.com/Cipaduduck/skin-cancer-classification/blob/main/main_notebook.ipynb).

# Dataset
Processing dataset for your machine learning model. What we use is the HAM10000 dataset which has been balancing the amount of data for each class by artakusuma on Kaggle. You can use [this dataset](https://www.kaggle.com/artakusuma/basedir) for training the model. 

# Train and test
You can run the notebook for training [here](https://github.com/Cipaduduck/skin-cancer-classification/blob/main/main_notebook.ipynb) also on the bottom of code you can easily test your model by upload the image. 

# Save model
Save the model that has been trained and tested into .h5 format.

# Deployment
Deploy the model into google cloud storage and put [this code](https://github.com/Cipaduduck/skin-cancer-classification/blob/main/backend/main.py) into google cloud function. For this project we use firebase for the database that you can connect with your Google Cloud Platform account. After that, deploy the firebase into the Website that is used as the skin cancer classifier user interface.
