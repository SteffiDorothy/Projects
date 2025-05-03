# Oceanographic Parameter Prediction using CalCOFI Dataset

**Worcester Polytechnic Institute (WPI)** 

**Course:** CS 548: Knowledge Discovery and Data Mining

**Author:** Steffi Dorothy

**Instructor:** Prof. Roee Shraga

**Date:** 10/27/2024

---

## Overview

This project focuses on developing predictive models for oceanographic parameters, specifically temperature, based on salinity and depth measurements from the California Cooperative Oceanic Fisheries Investigations (CalCOFI) dataset. The CalCOFI program is a long-standing initiative that monitors the California Current system, providing crucial data for understanding marine ecosystems and climate.

The goal of this project is to leverage machine learning techniques to create accurate models that can predict temperature variations. These predictions can contribute to a better understanding of ocean dynamics, climate change impacts, and marine ecosystem health, potentially aiding in fisheries management and the protection of endangered species.

---

## Dataset

The project utilizes the CalCOFI bottle database, a rich repository of oceanographic data collected over many years. The dataset includes:

* **Total Records:** 864,863
* **Number of Attributes:** 74 (with key parameters being temperature, salinity, and depth)

---

## Motivation

Understanding the relationships between fundamental oceanographic parameters like temperature, salinity, and depth is vital for various scientific and environmental applications. Accurate predictive models for these parameters can:

* Enhance our understanding of ocean circulation.
* Contribute to research on climate change impacts on marine environments.
* Support marine conservation efforts by anticipating environmental changes.
* Potentially aid in the management of fisheries by predicting temperature fluctuations.

---

## Key Features of the Model

* **Predictive Modeling:** Development of regression models to predict ocean temperature based on salinity and depth.
* **Comparative Analysis:** Evaluation and comparison of multiple regression techniques to identify the most effective model.
* **Model Optimization:** Implementation of hyperparameter tuning and regularization techniques to enhance model performance and prevent overfitting. 
* **Explainability:** Application of Explainable AI (XAI) methods to provide insights into the model's decision-making process.

---

## Technologies Used

* Python
* Scikit-learn
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SHAP
* LIME
* Optuna

---

## Methodology

This project involved the application of several regression techniques to predict temperature:

* Linear Regression
* Polynomial Regression
* Random Forest Regressor
* K-Nearest Neighbors (KNN) Regressor

The models were evaluated using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), and R-squared ($R^2$) score. Optimization techniques like GridSearchCV, RandomizedSearchCV, and Bayesian optimization (Optuna) were employed to fine-tune the models. Regularization techniques (Ridge, Lasso, ElasticNet) were also explored to prevent overfitting.

To gain insights into the models' decision-making processes, explainable AI techniques such as SHAP, Partial Dependence Plots, and LIME were utilized to identify important features and understand feature interactions.

---

## Results

The project findings indicate that the **Polynomial Regressor** and **Random Forest Regressor** demonstrated the best predictive accuracy based on lower MAE, MSE, and higher $R^2$ scores after optimization. While Linear and Polynomial Regressors showed strong performance, their susceptibility to overfitting in complex scenarios was noted. The Random Forest Regressor proved to be a robust choice due to its ensemble nature and ability to handle non-linear relationships.

---

## Future Directions

Potential future work includes:

* **Time Series Analysis:** If the data exhibits a significant temporal component, exploring time series forecasting techniques like ARIMA or Prophet could be beneficial.
* **Deep Learning:** Investigating deep learning models such as Recurrent Neural Networks (RNNs) or Long Short-Term Memory (LSTM) networks for potentially capturing more complex temporal or sequential patterns in the data.

---

## 💬 Contact

For questions or collaboration opportunities, please reach out via GitHub or [LinkedIn](https://www.linkedin.com/in/steffi-dorothy-9938a21a3/)!

