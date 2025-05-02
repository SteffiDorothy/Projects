# Leveraging Chess Game Data for Player Performance Prediction

**Worcester Polytechnic Institute (WPI)**  
**Course:** DS 502 – Statistical Methods for Data Science  
**Team Members:** Sheroz Shaikh & Steffi Dorothy  
**Instructor:** Prof. Fatemeh Emdad  
**Date:** 05/01/2024

---

## 📖 Overview

This project analyzes chess data from the Lichess platform using machine learning techniques to predict player performance. By modeling player ratings and outcomes based on game attributes and player moves, we aim to uncover strategic patterns and factors influencing game outcomes.

---

## 📂 Files in Repository

- `DS502_Team_1_Leveraging_Chess_Game.ipynb` — Jupyter Notebook with full project code and analysis.
- `DS502_Team_1_Leveraging_Chess_Game.pdf` — Project report.
- `Project Team 1 DS502.pdf` — Project summary document.
- `readme.md` — Project README.

---

## ✨ Key Achievements

- Developed a predictive model using decision tree regression to forecast chess player performance.
- Performed extensive exploratory data analysis (EDA) to uncover trends, correlations, and patterns.
- Applied feature engineering and preprocessing to improve data quality.
- Visualized data insights using Python libraries (Matplotlib, Seaborn, Pandas).

---

## 🗂 Description of the Problem

The goal is to predict whether a player will win or lose a chess game based on various game features and player characteristics. By analyzing a large dataset of chess games, we aimed to extract strategic insights and recurring patterns to improve our understanding of gameplay dynamics.

---

## 📊 Dataset

- **Source:** [Chess Game Dataset (Lichess) on Kaggle](https://www.kaggle.com/datasets/datasnaek/chess/data)  
- **Size:** ~20,000 games, 16 features  
- **Features:**  
    - Player ratings (Elo), usernames  
    - Game outcomes (checkmate, resignation, timeout, draw)  
    - Move sequences  
    - Time controls  
    - Opening details (ECO code, name, opening moves)  
- **Quality:** No missing values, rich metadata, CC0 1.0 Universal Public Domain Dedication.

---

## 💡 Motivation

We were motivated to apply data analysis techniques to understand the complexities of chess, gain insights into strategies and patterns, and predict player outcomes using machine learning.

---

## 🛠 Preprocessing

- Removed duplicates and filtered out zero-duration games.
- Binned ‘turns’ using `pd.cut` to categorize games by length.
- Converted categorical features (`game_type`, `ECO_Names`, `rating_level`, `turns_binned`) into factors.
- One-hot encoded categorical variables.
- Engineered new features:
  - `game_time_duration` = `last_move_at` - `created_at`
  - `rating_diff` = abs(`white_rating` - `black_rating`), binned into Low/Mid/High.
- Scaled numeric features:
  - MinMaxScaler: `initial_time`, `rating_diff`
  - StandardScaler: `turns`, `white_rating`, `black_rating`
- Split data into train/test sets (85/15 split).

---

## 📈 Exploratory Data Analysis (EDA)

- Used `matplotlib`, `seaborn`, and `pandas` for visualization.
- Applied descriptive statistics, grouping, and aggregation.
- Analyzed trends in player ratings, outcomes, openings, and game duration.
- Identified hidden patterns and correlations.

---

## 🤖 Methods and Model

- **Model used:** Decision Tree Regressor (Scikit-learn)
- **Target:** Predict player performance (win/loss outcome)
- **Evaluation Metrics:** RMSE, R² score, and accuracy

---

## 📋 Results

- Built a robust predictive model with meaningful accuracy.
- Highlighted key factors influencing chess outcomes.
- Gained insights into how player rating, openings, and game dynamics impact results.

---

## 📈 Tools & Libraries

- Python

- pandas, numpy

- scikit-learn

- matplotlib, seaborn

---

## 🔚 Conclusion

Our project demonstrates the potential of combining machine learning and domain-specific data to understand and predict outcomes in strategic games like chess. With further optimization, such models could be integrated into chess coaching tools or game analysis platforms.

---

## 📚 References

- Kaggle Lichess Dataset
- Scikit-learn Documentation
- Matplotlib, Seaborn, Pandas Documentation
- AlphaZero, DeepMind Research

---

## 👥 About the Team

- **Sheroz Shaikh:** Data preprocessing, machine learning modeling.
- **Steffi Dorothy:** Statistical analysis, visualization, results interpretation, and communication.

---

## 💬 Contact

For questions or collaboration opportunities, please reach out via GitHub or [LinkedIn](https://www.linkedin.com/in/steffi-dorothy-9938a21a3/)!
