## **Credit Card Fraud Detection**
**Author: Steffi Dorothy**

### **Project Description:** 
This project focuses on detecting fraudulent credit card transactions using machine learning models. By analyzing a dataset of credit card transactions, I aim to classify transactions as either fraudulent or legitimate based on various features.

### **Objective**
The objective of this project is to build a machine learning model that can identify fraudulent credit card transactions in real-time, helping banks and financial institutions prevent financial losses and protect their customers from fraud.

### **Dataset**

* **Description:** The dataset consists of anonymized transaction data with features such as transaction amount, user location, and transaction time, among others. Each transaction is labeled as either fraud or not fraud.

### **Key Features of the Model**
* **Classification:** The model classifies transactions into two categories: fraudulent and legitimate.
* **Feature Selection:** Selected features include transaction amount, time of day, location, and other relevant data points. I focus on reducing data imbalance and handling missing data to ensure the model's robustness.
* **Algorithms Used:**
  * Decision Trees
  * Random Forest
  * XGBoost
  * Logistic Regression
  * Support Vector Machines (SVM)

### **Model Evaluation Metrics**
To evaluate the model's performance, I used the following metrics:
* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
* ROC Curve

### **Steps Involved**
* **Data Preprocessing:**

  * Data cleaning (removal of duplicates, handling missing values)
  * Feature engineering (e.g., creating new variables from the dataset)
  * Scaling and normalization of numerical features
* **Model Training:**

  * Split the data into training and testing sets.
  * Train various models using the training data.
  * Tune hyperparameters for optimal model performance.
* **Evaluation:**

  * Evaluate the models using cross-validation.
  * Analyze model performance using confusion matrix, precision, recall, and F1 score.
### **Technologies Used**
* **Python:** For implementing machine learning models and data preprocessing.
* **Pandas:** For data manipulation.
* **Scikit-learn:** For implementing machine learning algorithms and evaluation.
* **XGBoost:** For advanced gradient boosting algorithms.
* **Matplotlib / Seaborn:** For data visualization and evaluation plots.
### **Future Improvements**
* **Real-time Fraud Detection:** Implement a real-time fraud detection system.
* **Deep Learning Models:** Experiment with deep learning models like neural networks for fraud detection.
* **Ensemble Methods:** Explore additional ensemble methods like stacking to improve performance
