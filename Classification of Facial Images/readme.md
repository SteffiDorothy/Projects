# Classification of Facial Images

**Worcester Polytechnic Institute (WPI)** 

**Course:** CS 548: Knowledge Discovery and Data Mining

**Instructor:** Prof. Roee Shraga

**Team:** Steffi Dorothy & Neha Bathuri 

**Date:** October 22, 2024

---

## ✅ Summary
This project explores facial image classification, attribute analysis, and image generation using a combination of traditional ML, deep learning, and GAN architectures. It demonstrates strong results across multiple tasks, including:
- Landmark detection
- Attribute prediction
- Image synthesis

---
  
## 📌 Purpose
- Understand the dataset
- Analyze the data
- Train and evaluate machine learning & deep learning models for:
  - Facial classification
  - Attribute analysis
  - Image generation

---

## 📂 The Dataset
- **Size**: Over 200,000 high-quality celebrity images
- **Attributes**: 40 binary attributes per image (e.g., gender, age, hair color, facial expressions)
- **Variations**: Wide range of poses, backgrounds, and lighting conditions

---

## 🔎 Exploratory Data Analysis (EDA)
- **Gender Distribution**: Slight skew toward female individuals
- **Attribute Distribution**:
  - High counts for Young and Attractive
  - Highest male attribute: No Beard
- **Correlation Matrix Insights**:
  - **Gender**: 
    - Strong negative correlation between Male vs. Young/Female
    - Male positively correlated with No_Beard
  - **Facial Hair**: 
    - Strong positive correlation between Beard and Mustache
    - Moderate positive correlation between Beard and Sideburns
  - **Age**: 
    - Strong negative correlation between Young vs. Bald/Gray_Hair/Receding_Hairline
  - **Appearance**: 
    - Moderate positive correlation between Attractive vs. High_Cheekbones

---

## 💡 Applications
- Face detection
- Facial attribute recognition (e.g., gender, hair color, expressions)
- Image segmentation (e.g., isolating eyes, lips)
- Image generation (e.g., creating realistic or modified facial images)

---

## 🛠 Problem Definition
- **Facial attribute recognition** using Face Recognition Library and RNN
- **Gender detection** with CelebA Dataset using InceptionV3
- **Image generation** using DCGAN trained on CelebA Dataset

---

## ⚙️ Data Preprocessing
- **Normalization**: Applied on 5,000 random images; rescales pixel intensity ranges for consistent convergence
- **Data Augmentation**: Techniques applied include rotation, shifting, zooming, flipping
- **Missing Values**: None

---

## 🤖 Machine Learning & Deep Learning Models

### 1. **Face Recognition**
- Detects facial landmarks (eyes, nose, mouth, chin)
- ~99% detection accuracy, even with non-aligned faces

### 2. **Haar Cascades**
- Uses Haar features and integral images for object detection
- **Limitation**: Fails on non-aligned images

### 3. **Rectifier Neural Networks (RNN)**
- Keras/TensorFlow implementation to classify attributes (e.g., bald or not)
- **Architecture**: Conv2D, MaxPooling, Dropout, Dense layers, ReLU activations
- **Results**: 97.7% accuracy, 1.32% loss

### 4. **InceptionV3**
- Deep CNN for efficient image classification and feature extraction
- Uses batch normalization and pre-trained weights
- Shows decreasing training and validation loss

### 5. **DCGAN (Deep Convolutional GAN)**
- **Generator Architecture**:
  - Input: 100-dimensional noise vector
  - Layers: Dense → Transposed Conv (256 → 128 → 64 filters) → BatchNorm → ReLU → Tanh
  - Output: RGB image
- **Discriminator Architecture**:
  - Input: Real or generated image
  - Layers: Conv (64 → 128 filters) → BatchNorm → LeakyReLU → Sigmoid
  - Output: Real vs. Fake classification

---

## 🔧 Key Features of the Model
- High accuracy in facial attribute prediction using RNN and InceptionV3
- Efficient image generation using DCGAN
- Robust face recognition capabilities with near-perfect accuracy

---

## 🚀 Future Improvements
- Implement more complex architectures like Transformer-based models for better attribute recognition.
- Improve the robustness of facial recognition under challenging lighting and pose variations.
- Expand the dataset with more diverse images to improve generalization.
- Optimize DCGAN generation speed and image quality for real-time applications.

---

## 📞 Contact
- **Steffi Dorothy**: [steffi.dorothy@email.com](mailto:steffdorothy@gmail.com)
- For questions or collaboration opportunities, please reach out via GitHub or [LinkedIn](https://www.linkedin.com/in/steffi-dorothy-9938a21a3/)!
