# Effectiveness of Data Synthesized by Generative AI in Supervised Image Classification

**Worcester Polytechnic Institute**  
**CS539: Machine Learning**  
**Date:** 12/12/2024


## 📌 Overview

This project investigates the role of synthetic image data, generated using Generative AI models, in improving the performance of supervised image classification models. The primary goal is to assess how models perform when trained with various combinations of real and synthetic data.


## 🧠 Motivation

Collecting and labeling large-scale image datasets can be expensive and time-consuming. Generative AI offers a promising alternative by synthesizing realistic data to supplement or replace real datasets. This study explores:

- How synthetic data affects classification accuracy.
- The ideal synthetic-to-real data ratio for optimal performance.
- The practicality of using synthetic images in real-world applications.


## 🧪 Methodology

### 🔹 Dataset

- **Real Images**: Sourced from the [Fruit Images for Object Detection](https://www.kaggle.com/datasets/mbkinaci/fruit-images-for-object-detection) dataset on Kaggle.
- **Synthetic Images**: Generated using **Stable Diffusion**, conditioned on class-specific prompts to ensure visual relevance and class consistency.

### 🔹 Experiments

We trained a Convolutional Neural Network (CNN) with different real-to-synthetic data ratios:

- 100% Real
- 75% Real + 25% Synthetic
- 50% Real + 50% Synthetic
- 25% Real + 75% Synthetic
- 100% Synthetic

### 🔹 Tools & Libraries

- Python, Jupyter Notebooks
- PyTorch / TensorFlow
- OpenCV, NumPy, Matplotlib
- Stable Diffusion (via Hugging Face or local implementation)

### 🔹 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score


## 📁 Folder Structure
- Final Presentation Group9.pdf # Final presentation slides summarizing the project 

- DataPreprocessing.ipynb # Notebook for data cleaning, formatting, and organization 

- Report.pdf # Full project report with background, methods, and results 

- machine_learning_model_CNN_synthetic.py # Python script for CNN architecture and synthetic training 

- model_training.ipynb # Main training and evaluation notebook 

- model_training copy.ipynb # Backup of model training notebook


## 📊 Key Findings

- Models trained on hybrid datasets (50–75% real + synthetic) showed comparable or slightly better results than those trained on only real data.
- Synthetic data helped balance class distributions and introduced useful variations.
- The quality and class relevance of synthetic images were crucial for maintaining model performance.


## 🚀 Future Work

- Evaluate model generalization using cross-domain datasets.
- Experiment with other generative models like GANs and VAEs.
- Use synthetic data in other domains such as medical imaging or remote sensing.


## 🤝 Contributors

- **Steffi Dorothy**
- **Diego Pena-Stein**
- **Ehu Shubham Shaw**
- **Bashir Gulistani**


## 📄 License

This project is licensed under the [MIT License](LICENSE).
