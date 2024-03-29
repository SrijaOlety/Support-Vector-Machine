# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:57:13 2023

@author: dell
"""

import pandas as pd
import numpy as np
df = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\forestfires.csv")
df.shape #(517,31) 
df.info()

# Preprocess the data

# EDA #

#EDA----->EXPLORATORY DATA ANALYSIS
#BOXPLOT AND OUTLIERS CALCULATION #

import seaborn as sns
import matplotlib.pyplot as plt
data = ['FFMC','DMC','DC','ISI','temp','RH','wind','rain','area']
for column in data:
    plt.figure(figsize=(8, 6))  
    sns.boxplot(x=df[column])
    plt.title(" Horizontal Box Plot of column")
    plt.show()
#so basically we have seen the ouliers at once without doing everytime for each variable using seaborn#

"""removing the ouliers"""

import seaborn as sns
import matplotlib.pyplot as plt
# List of column names with continuous variables
continuous_columns = ['FFMC','DMC','DC','ISI','temp','RH','wind','rain','area']

# Create a new DataFrame without outliers for each continuous column
data_without_outliers = df.copy()
for column in continuous_columns:
    Q1 = data_without_outliers[column].quantile(0.25)
    Q3 = data_without_outliers[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    data_without_outliers = data_without_outliers[(data_without_outliers[column] >= lower_whisker) & (data_without_outliers[column] <= upper_whisker)]

# Print the cleaned data without outliers
print(data_without_outliers)
df1 = data_without_outliers
df1
# Check the shape and info of the cleaned DataFrame
print(df1.shape)  #(302, 31)
print(df1.info())

#HISTOGRAM BUILDING, SKEWNESS AND KURTOSIS CALCULATION #
df1.hist()
df1.skew()
df1.kurt()
df1.describe() 

"""data division and standardizing"""
df_cont = df.iloc[:,2:11]
df_cont
df_cont.info()
from sklearn.preprocessing import StandardScaler
SS = StandardScaler()
X1 = SS.fit_transform(df_cont)
X1= pd.DataFrame(X1)
X1.columns=list(df_cont)
X1

df_cat = df.iloc[:,[0,1,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]]
df_cat
from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
for i in range(0,20):
    df_cat.iloc[:,i] = LE.fit_transform(df_cat.iloc[:,i])
df_cat.head()

X = pd.concat([X1,df_cat],axis = 1)
X
X.info()

#    Target variable #
Y = df.iloc[:,30:31]
Y
from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
Y.iloc[:,0] = LE.fit_transform(Y.iloc[:,0])
Y


 #  data partition and data validation#
 
from sklearn.model_selection import train_test_split

#by default it will take 75% of data as training data if we donot mention in the code#

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,train_size = 0.75,random_state = 15)
X_train.shape
X_test.shape

# Create and train your SVM model
from sklearn.svm import SVC
svc = SVC(C=1.0, kernel='linear')
svc.fit(X_train, Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))

#Train accuracy score: 0.902
#Test accuracy score: 0.892

#Validation set approach
training_accuracy = []
test_accuracy = []
for i in range (1,101):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=0.75,random_state=i)
    svc.fit(X_train,Y_train)
    Y_pred_train = svc.predict(X_train)
    Y_pred_test = svc.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train,Y_pred_train))
    test_accuracy.append(accuracy_score(Y_test,Y_pred_test))

print("Average training accuracy score:",(np.mean(training_accuracy)*100).round(3))   
print("Average test accuracy score:",(np.mean(test_accuracy)*100).round(3))          

#Average training accuracy score: 90.235
#Average test accuracy score: 89.4

#plotting

from sklearn.svm import SVC 
svc = SVC(C=1.0,kernel='linear')   #linear Classifier
svc.fit(X,Y)
"""X_final =X.iloc[:,:2]
from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X_final.values,
                      y=Y.values.reshape(-1),
                      clf=svc,
                      legend=4)"""
                      
X_subset = X.iloc[:, 9:11]
filler_feature_values = {i: 0.0 for i in range(11)}


clf = SVC(kernel='linear', C=1.0)
clf.fit(X_subset, Y)


from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X_subset.values,y=Y.values.ravel(),clf=clf, legend=4,filler_feature_values=filler_feature_values)


##Polynomial function(what if our data is in non linear shape, we have to functions in this case
#1. polynomial function and 2. radial function)

#SVM

from sklearn.svm import SVC
svc =SVC(degree=3,kernel='poly')  
svc.fit(X_train,Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

#Metrics
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))

#Train accuracy score: 0.767
#Test accuracy score: 0.762

#Validation set approach
training_accuracy = []
test_accuracy = []
for i in range (1,101):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=0.75,random_state=i)
    svc.fit(X_train,Y_train)
    Y_pred_train = svc.predict(X_train)
    Y_pred_test = svc.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train,Y_pred_train))
    test_accuracy.append(accuracy_score(Y_test,Y_pred_test))

print("Average training accuracy score:",(np.mean(training_accuracy)*100).round(3))    
print("Average test accuracy score:",(np.mean(test_accuracy)*100).round(3))            

#Average training accuracy score: 76.928
#Average test accuracy score: 76.031

#plotting

"""from sklearn.svm import SVC
svc =SVC(degree=3,kernel='poly')  #Polynomial function
svc.fit(X,Y)
X =df.iloc[:,:2]
from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X.values,
                      y=Y.values,
                      clf=svc,
                      legend=4)"""
                      
                      
X_subset = X.iloc[:, 9:11]
filler_feature_values = {i: 0.0 for i in range(11)}


clf = SVC(kernel='poly', degree = 3)
clf.fit(X_subset, Y)


from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X_subset.values,y=Y.values.ravel(),clf=clf, legend=4,filler_feature_values=filler_feature_values)


#Radial Basis Function
#SVM

from sklearn.svm import SVC
svc =SVC(degree=3,kernel='rbf')  
svc.fit(X_train,Y_train)
Y_pred_train = svc.predict(X_train)
Y_pred_test = svc.predict(X_test)

#Metrics
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Train accuracy score:", ac1.round(3))

ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test accuracy score:", ac2.round(3))  

# Train accuracy score: 0.762
#Test accuracy score: 0.754

#Validation set approach
training_accuracy = []
test_accuracy = []
for i in range (1,101):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=0.75,random_state=i)
    svc.fit(X_train,Y_train)
    Y_pred_train = svc.predict(X_train)
    Y_pred_test = svc.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train,Y_pred_train))
    test_accuracy.append(accuracy_score(Y_test,Y_pred_test))

print("Average training accuracy score:",(np.mean(training_accuracy)*100).round(3))    
print("Average test accuracy score:",(np.mean(test_accuracy)*100).round(3))            

#Average training accuracy score: 75.922
#Average test accuracy score: 74.638

#plotting

from sklearn.svm import SVC
svc =SVC(degree=3,kernel='rbf')  #Polynomial function
svc.fit(X,Y)

"""X =df_final.iloc[:,:2]
from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X.values,
                      y=Y.values,
                      clf=svc,
                      legend=4)"""


X_subset = X.iloc[:, 9:11]
filler_feature_values = {i: 0.0 for i in range(11)}


clf = SVC(kernel='rbf', degree = 3)
clf.fit(X_subset, Y)


from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X=X_subset.values,y=Y.values.ravel(),clf=clf, legend=4,filler_feature_values=filler_feature_values)










































