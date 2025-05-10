# 🦠 COVID-19 Research Topic Modeling: A Comparative Study

**Worcester Polytechnic Institute**  
**DS 504: Big Data Analytics**  
**Date:** 05/06/2025  

---

## 📚 Project Overview

The COVID-19 pandemic triggered an **explosion of research publications**, overwhelming scientists and policymakers with information. Our project leverages **AI and NLP topic modeling techniques** to automatically categorize and extract insights from COVID-19 research papers.

We conducted a **comparative study** using multiple topic modeling approaches to help summarize key themes and trends in COVID-19 research.

---

## 👥 Team Members

- Steffi Dorothy
- Dinesh Kodwani
- Guruganesh Holla
- Jose Fabrizio Filizzola
- Kathryn Butziger

---

## 🎯 Objectives

- Use **AI-driven techniques** like LDA, BERT, NMF, and K-Means clustering to extract meaningful topics.  
- Efficiently summarize COVID-19 research to assist researchers and policymakers.  
- Build an interactive demo app to visualize and compare topic modeling results.

---

## 🛠️ Methodology

### 1️⃣ Data Collection & Preprocessing
- Collected COVID-19 research articles.
- Cleaned and preprocessed titles & abstracts.
- Removed stop words and irrelevant characters.

### 2️⃣ Feature Extraction
- **TF-IDF vectors** (for LDA, NMF, K-Means).
- **BERT embeddings** (for BERT-based models & BERTopic).

### 3️⃣ Topic Modeling Techniques
| Technique | Description |
|-----------|-------------|
| **TF-IDF + K-Means** | Clusters documents using TF-IDF features. |
| **BERT + K-Means** | Clusters using BERT semantic embeddings. |
| **LDA** | Latent Dirichlet Allocation via Gensim. |
| **NMF** | Non-negative Matrix Factorization using Scikit-learn. |
| **BERTopic** | Combines BERT embeddings, UMAP, and HDBSCAN for dynamic topic discovery. |

### 4️⃣ Visualization
- Word clouds
- UMAP & PCA plots
- Topic distribution histograms

---

## 📝 Results

| Model                 | Silhouette Score | Coherence Score |
|----------------------|-----------------|----------------|
| **KMeans (TF-IDF)**   | 0.0038          | N/A            |
| **KMeans (BERT)**     | 0.0361          | N/A            |
| **LDA**               | N/A             | 0.5706         |
| **NMF**               | N/A             | 0.6725         |
| **BERTopic**          | 0.554           | 0.7381         |

✅ **BERTopic achieved the highest coherence and interpretability**, producing well-defined, context-aware topics.

---

## 💡 Key Takeaways

- Successfully modeled topics from **~10,000 COVID-19 research articles**.
- Extracted meaningful keywords and clusters from each method.
- **BERTopic** outperformed others in generating coherent, interpretable topics thanks to BERT embeddings.

---

## 🎬 Deliverables

- Topic modeling pipeline using **TF-IDF, BERT, LDA, NMF, BERTopic**.
- Interactive demo app to explore topic modeling results.
- Visualizations: word clouds, topic distribution plots, cluster visualizations.

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Run main script:
   ```bash
   python app.py

## 🙏 Acknowledgments

Thanks to **Worcester Polytechnic Institute** and **Professor Yanhua Li** for guidance and support throughout this project.

## 📞 Contact

For questions or collaboration, contact any team member or email **santhraj@wpi.edu**.
