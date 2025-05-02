# **Synthetic Data Toolkit – MassGov MDO-WPI-GQP-MA2**

This repository contains a toolkit to generate **realistic, privacy-preserving synthetic data** from structured CSV files using models like **TVAE**, **CTGAN**, and **GaussianCopula**.

---
## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Repository Structure](#repository-structure)
- [License](#license)
---

## Overview

This toolkit allows users to:

-  Generate synthetic datasets that mirror real data patterns  
-  Choose a generative model: `TVAE`, `CTGAN`, or `GaussianCopula`  
-  Apply privacy hashing to selected columns (PII)  
-  Evaluate synthetic data quality vs. real data  

---
## Installation

1. **Clone or Download the Repository:**
   ```bash
    git clone --branch SynData-Toolkit --single-branch https://github.com/massgov/mdo-wpi-gqp-ma2.git

---
Install Dependencies:
Ensure you have Python 3 installed. Then run:

2. **Using Pip:**
```sh
pip install -r requirements.txt
```
---
# Choosing a Synthetic Model

This toolkit offers three different models for generating synthetic data, each with its own characteristics. The best choice depends on your specific dataset and goals:

## GaussianCopula

- **Type:** Statistical / Mathematical Model
- **How it works:** Models the marginal distribution of each column individually and learns the correlations between columns using a Gaussian Copula.

### Pros
- Generally the fastest to train.
- Requires less data compared to deep learning models.
- Good for datasets where relationships between variables are approximately linear or can be captured by correlations.

### Cons
- May struggle to capture complex, non-linear relationships present in the data.
- Might not generate highly novel or outlier-like data points as effectively as GANs or VAEs.

### When to Use
Good starting point, especially for quick experiments, smaller datasets, or data where complex deep interactions aren't the primary concern.

---

## CTGAN (Conditional Tabular GAN)

- **Type:** Deep Learning / Generative Adversarial Network (GAN)
- **How it works:** Uses a generator network to create synthetic data and a discriminator network to distinguish synthetic data from real data. It's specifically designed to handle challenges in tabular data, like mixed data types and imbalanced categorical columns.

### Pros
- Can capture complex patterns and non-linear relationships.
- Often produces high-fidelity synthetic data that closely mimics the real data distributions.
- Effective at modeling multimodal distributions (where a column might have multiple peaks).

### Cons
- Requires more data and significantly longer training time compared to GaussianCopula.
- Training can sometimes be unstable (common with GANs).
- Hyperparameter tuning might be needed for optimal results.

### When to Use
When high fidelity is crucial, the dataset is reasonably large, and complex relationships need to be preserved. Good for datasets with tricky categorical variables.

---

## TVAE (Tabular Variational Autoencoder)

- **Type:** Deep Learning / Variational Autoencoder (VAE)
- **How it works:** Learns a compressed representation (latent space) of the data using an encoder network and then generates synthetic data from that space using a decoder network.

### Pros
- Generally more stable to train than CTGAN.
- Also capable of capturing complex, non-linear relationships.
- Can sometimes generate more diverse (though potentially slightly less high-fidelity) data than GANs.

### Cons
- Typically requires more data and longer training time than GaussianCopula (often faster than CTGAN, but can vary).
- Might sometimes produce slightly blurrier or less sharp distributions compared to GANs for certain data types.
- Hyperparameter tuning can impact performance.

### When to Use
A good alternative to CTGAN, especially if GAN training proves unstable. Suitable for larger datasets where capturing complex patterns is important.

---

## General Recommendation

- Start with **GaussianCopula** for a quick baseline.


- If fidelity is low or complex patterns aren't captured, try **CTGAN** or **TVAE**, allowing for longer training times.


- **Experimentation is key!**  
The best model can vary between different datasets. Use the evaluation metrics and plots provided by the toolkit to compare the results from different models.

## **Running the Project**

1. **Place Your File**  
   Upload your CSV file into the `data/` folder.

---
2. **Run the Project**  
   Execute the script with:
   ```bash
   python src/Main.py
---
3. **Choose Your Model**

   When prompted, choose one of the following synthetic data models:

- `1`: GaussianCopula  
- `2`: CTGAN  
- `3`: TVAE (default)

---
4. **Choose Number of rows**

   You'll be asked how many rows you would like your synthetic dataset to have.
   
   (pressing Enter with no Value, selects the same number of rows as the original dataset.)
   
---

5. **Select Columns for Privacy Hashing**

   You'll be asked which columns to hash for privacy.  
   Enter column numbers separated by commas (e.g., `1, 3, 5`).
---

6. **Check the Output**

-  **Synthetic data** is saved in `output/synthetic_data.csv`
-  **Metadata** is saved in `output/metadata.json`
-  **Trained model** is saved in `models/synthesizer.pkl`
-  **Visual Plots** are saved in `output/plots`

---
## **Streamlit Web Application**

In addition to the command-line interface, the project includes a **Streamlit web application** (`app.py`) for an interactive user experience.

### Functionality:

- Upload CSV datasets directly from the browser  
- Auto-detect and convert semicolon-delimited files using `file_check.py`  
- Select a synthetic model (`TVAE`, `CTGAN`, or `GaussianCopula`)  
- Choose the number of synthetic rows  
- Apply differential privacy or hashing to specific columns  
- Generate and view evaluation metrics and comparison plots 
- Download synthetic datasets, plots, and reports  

### Run the app with:
```bash
python -m streamlit run app.py

```
---

# Interpreting Evaluation Results

The toolkit evaluates the quality of the synthetic data by comparing its statistical properties to the original data. Two key custom metrics are calculated for each column:

## Wasserstein Distance

- **What it measures:**  
  Represents the minimum "cost" or "effort" required to transform the distribution of the synthetic data into the distribution of the real data.  
  

- Imagine the distributions as piles of dirt; the metric is the minimum effort to move one pile to match the other.

### Interpretation
- A value closer to **0** indicates that the distributions are very similar.
- A larger value indicates a greater difference between the real and synthetic distributions for that column.
- This metric works well for both numerical and categorical data and avoids some issues that KL Divergence can have (e.g., infinite values when zero-probability events occur).

### Goal
Aim for **lower Wasserstein Distance** values.

---

## KL Divergence (Kullback-Leibler Divergence)

- **What it measures:**  
  Measures how much information is lost when approximating the real data distribution with the synthetic data distribution. It quantifies the difference between two probability distributions.  
 
_Note:_ It's calculated as **KL(Real || Synthetic)**, measuring the divergence from the synthetic to the real distribution.

### Interpretation
- A value closer to **0** indicates high similarity between the distributions.
- Larger positive values indicate greater divergence.


- **Important:**  
  - KL Divergence is **not symmetric** (KL(P||Q) ≠ KL(Q||P)).
  - It can become **infinite** if the synthetic distribution assigns zero probability to an event that has non-zero probability in the real data.
  - The implementation uses smoothing (adding a tiny epsilon) to mitigate this, but very large or infinite values can still occur if distributions are drastically different.

### Goal
Aim for **lower KL Divergence** values.

---

## Using the Metrics and Plots

- **Summary Report (`custom_metrics_summary.txt`)**  
  Provides average and other statistics (min, max, median, std) for Wasserstein and KL Divergence across all columns.  
  - This gives a quick overview of the overall synthetic data quality.
  - Lower average values are generally better.



- **Detailed Report (`custom_metrics_detailed.csv`)**  
  Shows the specific Wasserstein and KL Divergence scores for each column.
  - Use this to identify which columns are synthesized well (low scores) and which ones might need improvement (high scores).



- **Distribution Plots (`output/plots/`)**  
  Visual plots (histograms for numerical columns, bar charts for categorical columns) complement the metrics.
  - Examine them to see how the distributions differ.
  - Check if the synthetic data misses certain peaks or if the range differs.
  - This visual check is crucial alongside numerical scores.

---

By combining the numerical metrics with the visual plots, you can get a **comprehensive understanding** of your synthetic data's fidelity compared to the original dataset.


## **Privacy Feature**

The toolkit supports privacy-enhancing transformations:

- Use `privacy_utils.py` to **hash sensitive columns**


- Customizable during both command-line and Streamlit interactions
 

- Ensures better compliance for privacy-sensitive use cases

## **File Preprocessing**

Some CSVs use semicolons as delimiters. To ensure compatibility:

- Use `file_check.py` to auto-convert **semicolon-delimited** files to **comma-delimited** format  
- This runs automatically in the background via both `Main.py` and `app.py`

## **Repository Structure**

```
mdo-wpi-gqp-ma2/
│
├── data/                        # Input folder for original CSV files
├── output/                      # Generated synthetic data & metadata
│   ├── plots/                   # Visual distribution plots (HTML)
│   └── metrics/                 # Evaluation reports (summary + detailed)
├── models/                      # Trained model artifacts
├── temp_data/                   # Temporary files (uploaded via Streamlit)
│
├── src/                         # Source code
│   ├── Main.py                  # Main runner script
│   ├── file_check.py            # Auto-detects CSVs & handles delimiter conversion
│   ├── metadata_converter.py    # Generates metadata from real datasets
│   ├── synthetic_data_model.py  # Trains model and generates synthetic data
│   ├── privacy_utils.py         # Privacy hashing for selected columns
│   ├── evaluator.py             # Evaluates synthetic data vs. real data
│   ├── config.py                # Configuration constants
│   └── utils.py                 # Utility functions
├── app.py                       # Streamlit web app for interactive use
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation

```

## **Main Script vs. Web App**

- `src/Main.py`: Run for script-based generation via terminal/CLI  
- `app.py`: Launches an interactive UI using Streamlit for an easier user experience


## **License**

This project is licensed under the **MIT License**. See the [LICENSE](https://mit-license.org/) file for details.

---

### **Now you're all set! Clone, set up, and run the project!**

