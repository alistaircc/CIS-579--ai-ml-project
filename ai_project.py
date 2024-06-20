# -*- coding: utf-8 -*-
"""AI Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jmDA9acYFIyuhbTU6yDZvYyEuXENbceq

#### Import Libraries & Dataset
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score

# Mount drive
from google.colab import drive
drive.mount('/content/drive')

# Path to your CSV file
csv_file_path = '/content/drive/My Drive/datasets/phishing_dataset_train.csv'

# Import Dataset
dataset = pd.read_csv(csv_file_path)

# Get Dataset shape (i.e. rows, cols)
print(dataset.shape)

"""#### Visualize Raw Dataset"""

# Visualize first 10 rows within dataset
dataset.head(10)

"""#### View Dataset Features w/ Data Types"""

# View dataset feature names and their data types
dataset.info()

"""#### Add New Column for Categorical Classification"""

# Consolidate all instances of the class labelled '1'
dataset['Classification'] = np.where(dataset['class']==1, 'Phishing', 'Non-Phishing')
dataset.head()

# Drop the Label feature since Class was added
dataset = dataset.drop(dataset.columns[-2],axis=1)
dataset.head()

"""#### Specify Feature Columns for Panda Dataframe Analysis"""

# Define features to be used by the classifier
features = pd.Index(['Domain Similarity', 'URL Length', 'HTTP Protocol',
                    'No. of Dot', 'No. of Slash', 'No. of Double Slash', 'No. of Hyphen',
                    'No. of Underscore', 'No. of Equal', 'No. of Parenthesis', 'No of Curly Bracket', 'No. of Square Bracket',
                    'No. of Less Than and Greater Than', 'No. of Tilde', 'No. of Asterisk', 'No. of Plus', 'URL Include @', 'URL Include IP',
                    'Server Response History', 'Redirect', 'No. of <a> Tag', 'No. of <input> Tag', 'No. of <button> Tag', 'No. of <link> Tag',
                    'No. of <iframe> Tag'])

"""#### Conduct Dataset Cleaning"""

# Delete rows with null values
dataset.dropna(inplace=True)

# Remove duplicated rows (avoid overfitting)
dataset.drop_duplicates(inplace=True)

print(dataset.shape)

"""#### Split Dataset into Training and Test Set"""

# With 'Classification' being the target variable, drop for X and add for y
X = dataset.drop('Classification', axis=1)
y = dataset['Classification']

# Split dataset into 85% training and 15% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

"""#### Perform Feature Scaling"""

# Using the StandardScaler from scikit-learn lib
# Create scaler obj
sc = StandardScaler()

# Compute the mean and std of the training data
X_train = sc.fit_transform(X_train)

# Compute the mean and std of the test data
X_test = sc.transform(X_test)

"""#### 1. K-Nearest Neighbors Model Analysis

##### Training the K-NN model
"""

# No. of neighbor cluster set to 5
# Distance metric set to minkowski (which is a combination of Manhattan and Euclidean)
# P=2 sets the minkowski to be more equivalent to Euclidean Distance
#knn = KNeighborsClassifier(n_neighbors= 5, metric = 'minkowski', p=2)
knn = KNeighborsClassifier()

# Train the K-NN classifier
knn.fit(X_train, y_train)

"""##### Test K-NN Model Predictions"""

# Test the trained model using the test set
knn_start = time.time()
knn_pred = knn.predict(X_test)
knn_end = time.time()

# Calculate prediction time
knn_pred_time = knn_end - knn_start

print("KNN Prediction Time: ", knn_pred_time)
print("KNN Accuracy:",  accuracy_score(y_test, knn_pred))
print("KNN F1-score:", f1_score(y_test, knn_pred, pos_label = 'Phishing'))

"""#### 2. Decision Tree Model Analysis

##### Training the DT model
"""

# Criterion = Gini impurity
#dtree = DecisionTreeClassifier(criterion= 'gini', random_state=0)
dtree = DecisionTreeClassifier()

# Train the Decision Tree classifier
dtree.fit(X_train, y_train)

"""##### Test Decision Tree Model Predictions"""

# Test the trained model using the test set
dt_start = time.time()
dtree_pred = dtree.predict(X_test)
dt_end = time.time()

# Calculate prediction time
dt_pred_time = dt_end - dt_start

print("DT Prediction Time: ", dt_pred_time)
print("DT Accuracy:",  accuracy_score(y_test, dtree_pred))
print("DT F1-score:", f1_score(y_test, dtree_pred, pos_label = 'Phishing'))

"""#### 3. Random Forest Model Analysis

##### Training the RF model
"""

# random forest model creation
rfc = RandomForestClassifier()

# Train the Random Forest classifier
rfc.fit(X_train,y_train)

"""##### Test RF Model Predictions"""

# Test the trained model using the test set
rf_start = time.time()
rf_pred = rfc.predict(X_test)
rf_end = time.time()

# Calculate prediction time
rf_pred_time = rf_end - rf_start

print("RF Prediction Time: ", rf_pred_time)
print("RF Accuracy:",  accuracy_score(y_test, rf_pred))
print("RF F1-score:", f1_score(y_test, rf_pred, pos_label = 'Phishing'))

"""#### 4. Multilayer Perceptron Model Analysis

##### Training the MLP model
"""

# Two hidden layers with 100 and 50 neurons
# ReLU Activation function
# Regularization term (L2)
# Broyden–Fletcher–Goldfarb–Shanno (L-BFGS) optimization algorithm
#mlp = MLPClassifier(hidden_layer_sizes=(100,50), activation='relu', alpha=0.00001, max_iter=200, solver='lbfgs', random_state=0)
mlp = MLPClassifier()

# Train the Decision Tree classifier
mlp.fit(X_train, y_train)

"""##### Test MLP Model Predictions"""

# Test the trained model using the test set
mlp_start = time.time()
mlp_pred = mlp.predict(X_test)
mlp_end = time.time()

# Calculate prediction time
mlp_pred_time = mlp_end - mlp_start

print("MLP Prediction Time: ", mlp_pred_time)
print("MLP Accuracy:",  accuracy_score(y_test, mlp_pred))
print("MLP F1-score:", f1_score(y_test, mlp_pred, pos_label = 'Phishing'))

"""##### Baseline Results Combined"""

from prettytable import PrettyTable

# Create a PrettyTable object
table = PrettyTable()

# Define column names
table.field_names = ["Model / Algorithm", "Prediction Time", "Accuracy", "F1-Score"]

# Add rows to the table
table.add_row(["KNN", knn_pred_time, accuracy_score(y_test, knn_pred), f1_score(y_test, knn_pred, pos_label = 'Phishing')])
table.add_row(["DT", dt_pred_time, accuracy_score(y_test, dtree_pred), f1_score(y_test, dtree_pred, pos_label = 'Phishing')])
table.add_row(["RF", rf_pred_time, accuracy_score(y_test, rf_pred), f1_score(y_test, rf_pred, pos_label = 'Phishing')])
table.add_row(["MLP", mlp_pred_time, accuracy_score(y_test, mlp_pred), f1_score(y_test, mlp_pred, pos_label = 'Phishing')])

print(table)

"""##### Training the K-NN model w/ Param Fine-Tunning"""

# No. of neighbor cluster set to 5
# Distance metric set to minkowski (which is a combination of Manhattan and Euclidean)
# P=1 sets the minkowski to be more equivalent to Manhattan Distance
knn_model = KNeighborsClassifier(n_neighbors= 5, metric = 'minkowski', p=1)

# Train the K-NN classifier
knn_model.fit(X_train, y_train)

# Test the trained model using the test set
knn_model_start = time.time()
knn_model_pred = knn_model.predict(X_test)
knn_model_end = time.time()

# Calculate prediction time
knn_model_pred_time = knn_model_end - knn_model_start

print("KNN w/ Fine-Tunning Prediction Time: ", knn_model_pred_time)
print("KNN w/ Fine-Tunning Accuracy:",  accuracy_score(y_test, knn_model_pred))
print("KNN w/ Fine-Tunning F1-score:", f1_score(y_test, knn_model_pred, pos_label = 'Phishing'))

"""##### Training the DT model w/ Param Fine-Tunning"""

# Criterion = entropy
dt_model = DecisionTreeClassifier(criterion= 'entropy', random_state=42)

# Train the Decision Tree classifier
dt_model.fit(X_train, y_train)

# Test the trained model using the test set
dt_model_start = time.time()
dt_model_pred = dt_model.predict(X_test)
dt_model_end = time.time()

# Calculate prediction time
dt_model_pred_time = dt_model_end - dt_model_start

print("DT w/ Fine-Tunning Prediction Time: ", dt_model_pred_time)
print("DT w/ Fine-Tunning Accuracy:",  accuracy_score(y_test, dt_model_pred))
print("DT w/ Fine-Tunning F1-score:", f1_score(y_test, dt_model_pred, pos_label = 'Phishing'))

"""##### Training the RF model w/ Param Fine-Tunning"""

from sklearn.model_selection import RandomizedSearchCV

# Create random grid
random_grid = {'bootstrap': [True, False], # Method of selecting samples for training each tree
               'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, None], # Maximum number of levels in tree
               'max_features': ['auto', 'sqrt'], # Number of features to consider at every split
               'min_samples_leaf': [1, 2, 4], # Minimum number of samples required at each leaf node
               'min_samples_split': [2, 5, 10], # Minimum number of samples required to split a node
               'n_estimators': [130, 180, 230]} # Number of trees in random forest

# random forest model creation
rf = RandomForestClassifier()

# n_iter = 100 different sets of hyperparameters will be randomly selected and evaluated
# cv=3, each set of hyperparameters will be evaluated using 3-fold cross-validation
# verbosity: the higher the value, the more messages are printed
# n_jobs = number of jobs to run in parallel
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)

# Train the Random Forest classifier
rf_random.fit(X_train,y_train)

# Test the trained model using the test set
rf_random_start = time.time()
rf_random_pred = rf_random.predict(X_test)
rf_random_end = time.time()

# Calculate prediction time
rf_random_pred_time = rf_random_end - rf_random_start

print("RF w/ Fine-Tunning Prediction Time: ", rf_random_pred_time)
print("RF w/ Fine-Tunning Accuracy:",  accuracy_score(y_test, rf_random_pred))
print("RF w/ Fine-Tunning F1-score:", f1_score(y_test, rf_random_pred, pos_label = 'Phishing'))

"""##### Training the MLP model w/ Param Fine-Tunning"""

# Two hidden layers with 100 and 50 neurons
# ReLU Activation function
# Regularization term (L2)
# Broyden–Fletcher–Goldfarb–Shanno (L-BFGS) optimization algorithm
mlp_model = MLPClassifier(hidden_layer_sizes=(100,50), activation='logistic', alpha=0.00001, max_iter=200, solver='adam', random_state=42)

# Train the Decision Tree classifier
mlp_model.fit(X_train, y_train)

# Test the trained model using the test set
mlp_model_start = time.time()
mlp_model_pred = mlp_model.predict(X_test)
mlp_model_end = time.time()

# Calculate prediction time
mlp_model_pred_time = mlp_model_end - mlp_model_start

print("MLP Prediction Time: ", mlp_model_pred_time)
print("MLP Accuracy:",  accuracy_score(y_test, mlp_model_pred))
print("MLP F1-score:", f1_score(y_test, mlp_model_pred, pos_label = 'Phishing'))

"""##### Hyperparam Fine-tunning Models Results Combined"""

# Create a PrettyTable object
table = PrettyTable()

# Define column names
table.field_names = ["Model / Algorithm", "Prediction Time", "Accuracy", "F1-Score"]

# Add rows to the table
table.add_row(["KNN", knn_model_pred_time, accuracy_score(y_test, knn_model_pred), f1_score(y_test, knn_model_pred, pos_label = 'Phishing')])
table.add_row(["DT", dt_model_pred_time, accuracy_score(y_test, dt_model_pred), f1_score(y_test, dt_model_pred, pos_label = 'Phishing')])
table.add_row(["RF", rf_random_pred_time, accuracy_score(y_test, rf_random_pred), f1_score(y_test, rf_random_pred, pos_label = 'Phishing')])
table.add_row(["MLP", mlp_model_pred_time, accuracy_score(y_test, mlp_model_pred), f1_score(y_test, mlp_model_pred, pos_label = 'Phishing')])

print(table)

# Create bar chart using extracted values from table
plt.bar("KNN", knn_model_pred_time)
plt.bar("DT", dt_model_pred_time)
plt.bar("RF", rf_random_pred_time)
plt.bar("MLP", mlp_model_pred_time)

# Define chart labels
plt.title("Param Fine-Tune Classification Times")
plt.xlabel("Model")
plt.ylabel("Time (Secs)")

# Show plot
plt.show()

# Create bar chart using extracted values from table
plt.bar("KNN", f1_score(y_test, knn_model_pred, pos_label = 'Phishing'))
plt.bar("DT", f1_score(y_test, dt_model_pred, pos_label = 'Phishing'))
plt.bar("RF", f1_score(y_test, rf_random_pred, pos_label = 'Phishing'))
plt.bar("MLP", f1_score(y_test, mlp_model_pred, pos_label = 'Phishing'))

# Define chart labels
plt.title("Param Fine-Tune F1-Scores")
plt.xlabel("Model")
plt.ylabel("Percentage %")

# Show plot
plt.show()

# Create bar chart using extracted values from table
plt.bar("KNN", accuracy_score(y_test, knn_model_pred))
plt.bar("DT", accuracy_score(y_test, dt_model_pred))
plt.bar("RF", accuracy_score(y_test, rf_random_pred))
plt.bar("MLP", accuracy_score(y_test, mlp_model_pred))

# Define chart labels
plt.title("Param Fine-Tune Accuracy")
plt.xlabel("Model")
plt.ylabel("Percentage %")

# Show plot
plt.show()

"""#### Optimal Model Selection

##### Feature Selection using SelectKBest
"""

# Feature Selection (K=10)
skb = SelectKBest(score_func=f_classif, k=10)

X_train_selected = skb.fit_transform(X_train, y_train)
X_test_selected = skb.transform(X_test)

# Retrieve selected features
selected_features = skb.get_support(indices=True)

# Get feature names
selected_feature_names = X.columns[selected_features]

print("Selected feature names:", selected_feature_names)

"""##### Train & test the DT model (Optimal Selected Model)"""

# Optimal DT model creation
optimal_model = DecisionTreeClassifier(criterion= 'entropy', random_state=42)

# Train the Decision Tree classifier
optimal_model.fit(X_train_selected, y_train)

# Test the trained model using the test set
model_start = time.time()
model_pred = optimal_model.predict(X_test_selected)
model_end = time.time()

# Calculate prediction time
model_pred_time = model_end - model_start

print("DT Prediction Time: ", model_pred_time)
print("DT Accuracy:",  accuracy_score(y_test, model_pred))
print("DT F1-score:", f1_score(y_test, model_pred, pos_label = 'Phishing'))

# Create a PrettyTable object
table = PrettyTable()

# Define column names
table.field_names = ["Iteration", "Model / Algorithm", "Prediction Time", "Accuracy", "F1-Score"]

# Add rows to the table
table.add_row(["Baseline", "DT", dt_pred_time, accuracy_score(y_test, dtree_pred), f1_score(y_test, dtree_pred, pos_label = 'Phishing')])
table.add_row(["Param Fine-Tune", "DT", dt_model_pred_time, accuracy_score(y_test, dt_model_pred), f1_score(y_test, dt_model_pred, pos_label = 'Phishing')])
table.add_row(["Optimal", "DT", model_pred_time, accuracy_score(y_test, model_pred), f1_score(y_test, model_pred, pos_label = 'Phishing')])

print(table)

# Create bar chart using extracted values from table
plt.bar("Baseline", dt_pred_time)
plt.bar("Param Fine-Tune", dt_model_pred_time)
plt.bar("Optimal", model_pred_time)

# Define chart labels
plt.title("Decision Tree Classification Times")
plt.xlabel("Iterations")
plt.ylabel("Time (Secs)")

# Show plot
plt.show()

"""#### Save Trained Model w/ top 10 Best Features:
1. domain_similarity
2. url_length
3. http_protocol
4. num_slash
5. num_hyphen
6. response_history
7. redirect
8. num_a_href
9. num_link_href
10. num_iframe
"""

import joblib

base_path = '/content/drive/My Drive/datasets/models/'

model_path = base_path + 'dt_model.joblib'
scaler_path = base_path + 'scaler.joblib'
selector_path = base_path + 'selector.joblib'

# Save classifier, scaler and selector
joblib.dump(optimal_model, model_path)
joblib.dump(sc, scaler_path)
joblib.dump(skb, selector_path)