# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 21:28:46 2023

@author: dell
"""
#pip install mlxtend
import numpy as np
import pandas as pd
df1 = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\SalaryData_Train(1).csv")
df1
df2 = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\SalaryData_Test(1).csv")
df2
df1.info()
df2.info()
df1.shape #(30161,14)
df2.shape #(15060,14)

# Preprocess the data

# EDA #

#EDA----->EXPLORATORY DATA ANALYSIS
#BOXPLOT AND OUTLIERS CALCULATION #

import seaborn as sns
import matplotlib.pyplot as plt
data = ['age','educationno','capitalgain','capitalloss','hoursperweek']
for column in data:
    plt.figure(figsize=(8, 6))  
    sns.boxplot(x=df1[column])
    plt.title(" Horizontal Box Plot of column")
    plt.show()
#so basically we have seen the ouliers at once without doing everytime for each variable using seaborn#

"""removing the ouliers"""

import seaborn as sns
import matplotlib.pyplot as plt
# List of column names with continuous variables
continuous_columns = ['age','educationno','capitalgain','capitalloss','hoursperweek']

# Create a new DataFrame without outliers for each continuous column
data_without_outliers = df1.copy()
for column in continuous_columns:
    Q1 = data_without_outliers[column].quantile(0.25)
    Q3 = data_without_outliers[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    data_without_outliers = data_without_outliers[(data_without_outliers[column] >= lower_whisker) & (data_without_outliers[column] <= upper_whisker)]

# Print the cleaned data without outliers
print(data_without_outliers)
df_train = data_without_outliers
print(df_train.shape) #(19064,14)
print(df_train.info())
df_train
# Check the shape and info of the cleaned DataFrame


# removing outliers from the testing data sample

continuous_columns = ['age','educationno','capitalgain','capitalloss','hoursperweek']

# Create a new DataFrame without outliers for each continuous column
data_without_outliers = df2.copy()
for column in continuous_columns:
    Q1 = data_without_outliers[column].quantile(0.25)
    Q3 = data_without_outliers[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    data_without_outliers = data_without_outliers[(data_without_outliers[column] >= lower_whisker) & (data_without_outliers[column] <= upper_whisker)]

# Print the cleaned data without outliers
print(data_without_outliers)
df_test = data_without_outliers
df_test
# Check the shape and info of the cleaned DataFrame
print(df_test.shape) #(9549,14)
print(df_test.info())




#HISTOGRAM BUILDING, SKEWNESS AND KURTOSIS CALCULATION #
df_train.hist()
df_train.skew()
df_train.kurt()
df_train.describe() 

df_test.hist()
df_test.skew()
df_test.kurt()
df_test.describe() 

#data partition#
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load our training data from Excel sheet 1
df_train = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\SalaryData_Train(1).csv")
df_train.info()
# Load our testing data from Excel sheet 2
df_test = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\SalaryData_Test(1).csv")
df_test.info()
# Assuming your target variable column is named 'target' in both DataFrames
X_train = df_train.drop(columns=['Salary'])  # Features for training data
Y_train = df_train['Salary']               # Target variable for training data


import numpy as np
unique_classes = np.unique(Y_train)
print(unique_classes)


X_test = df_test.drop(columns=['Salary'])    # Features for testing data
Y_test = df_test['Salary']                   # Target variable for testing data




                     # Apply label encoding to categorical columns
                     
categorical_columns = ['workclass', 'education', 'maritalstatus', 'occupation', 'relationship', 'race', 'sex', 'native']
LE = LabelEncoder()
for column in categorical_columns:
    X_train[column] = LE.fit_transform(X_train[column])
    X_test[column] = LE.transform(X_test[column])  # Use transform, not fit_transform

# Standardize the data
SS = StandardScaler()
X_train = SS.fit_transform(X_train)
X_test = SS.transform(X_test)

#This code ensures that both training and testing data are label-encoded and standardized correctly before fitting the SVM model.



# Create and train your SVM model

from sklearn.svm import SVC
svc = SVC(C=1.0, kernel='linear') # linear function
svc.fit(X_train, Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))

#Train accuracy score: 0.789
#Test accuracy score: 0.791

"""when we have two distinct datasets,one for training and one for testing,the validation approach involving cross validation
 may not be directly applicable.The purpose of cross validation is to utilize the training data for model validationa and as 
 a tuning parameter.so we will split the train data into train set and validation set, fit our model on the train data and evaluate the model performance using the validation 
 data ,once we have selected the best performing model we will evaluate on the independent test data set to estimate the models performance on unseen data. """

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Assuming we have X_train, Y_train, X_test, Y_test

# Step 1: Split the training data into train and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, train_size=0.75, random_state=42)

# Step 2: Fit our model on the training set and evaluating  on the validation set
svc = SVC(C=1.0, kernel='linear') # linear function
svc.fit(X_train, Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_val = svc.predict(X_val)

# Step 3: Evaluating  the performance on the validation set
ac_val = accuracy_score(Y_val, Y_pred_val)
print("Validation accuracy score:", ac_val.round(3))

# Step 4: Once we have selected the best model,  we evaluate it on the independent test dataset
Y_pred_test = svc.predict(X_test)
ac_test = accuracy_score(Y_test, Y_pred_test)
print("Test accuracy score:", ac_test.round(3))


#Validation accuracy score: 0.787
#Test accuracy score: 0.791


#plotting

from sklearn.svm import SVC 
svc = SVC(C=1.0,kernel='linear')   #linear Classifier
svc.fit(X,Y)
X =df_final.iloc[:,:2]
from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X.values,
                      y=Y.values,
                      clf=svc,
                      legend=4)

##Polynomial function
#SVM
from sklearn.svm import SVC
svc =SVC(degree=3,kernel='poly')  #Polynomial function
svc.fit(X_train,Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

#Metrics
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))

#Train accuracy score: 0.836
#Test accuracy score: 0.831

# Assuming we have X_train, Y_train, X_test, Y_test

# Step 1: Split the training data into train and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, train_size=0.75, random_state=42)

# Step 2: Fit our model on the training set and evaluating  on the validation set
svc = SVC(degree=3,kernel='poly') # polynomial function
svc.fit(X_train, Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_val = svc.predict(X_val)

# Step 3: Evaluating  the performance on the validation set
ac_val = accuracy_score(Y_val, Y_pred_val)
print("Validation accuracy score:", ac_val.round(3))

# Step 4: Once we have selected the best model,  we evaluate it on the independent test dataset
Y_pred_test = svc.predict(X_test)
ac_test = accuracy_score(Y_test, Y_pred_test)
print("Test accuracy score:", ac_test.round(3))

#Validation accuracy score: 0.829
#Test accuracy score: 0.831


#Radial Basis Function
#SVM
from sklearn.svm import SVC
svc =SVC(degree=3,kernel='rbf')  #Radial Basis Function
svc.fit(X_train,Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

#Metrics
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))   

#Train accuracy score: 0.84
#Test accuracy score: 0.835    


# Assuming we have X_train, Y_train, X_test, Y_test

# Step 1: Split the training data into train and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, train_size=0.75, random_state=42)

# Step 2: Fit our model on the training set and evaluating  on the validation set
svc = SVC(degree=3,kernel='rbf') # polynomial function
svc.fit(X_train, Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_val = svc.predict(X_val)

# Step 3: Evaluating  the performance on the validation set
ac_val = accuracy_score(Y_val, Y_pred_val)
print("Validation accuracy score:", ac_val.round(3))

#Validation accuracy score: 0.842

# Step 4: Once we have selected the best model,  we evaluate it on the independent test dataset
Y_pred_test = svc.predict(X_test)
ac_test = accuracy_score(Y_test, Y_pred_test)
print("Test accuracy score:", ac_test.round(3))

#Test accuracy score: 0.835








