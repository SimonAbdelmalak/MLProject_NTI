# **TravelMate — Hotel Recommendation System**

---

## 📌 **About The Project**

**TravelMate** is an intelligent hotel recommendation system designed to help users find the most suitable hotel based on their personal preferences and selected features

Powered by the **K-Nearest Neighbors (KNN)** machine learning algorithm, the system analyzes user inputs to calculate similarities and recommend the **top 5 matching hotels**, along with a precise **match percentage (%)** for each result.

The dataset features curated hotel data across 4 countries:
* 🇪🇬 **Egypt**
* 🇨🇭 **Switzerland**
* 🇫🇷 **France**
* 🇪🇸 **Spain**

---

# 🏨 Hotel Value Prediction & Management System
An end-to-end Machine Learning project to clean, process, and predict hotel valuation and ratings using multiple regression techniques, integrated with an intuitive Graphical User Interface (GUI).

---

## 🛠️ Project Workflow

### 1. Data Cleaning & Exploration
* Handled missing attributes and removed broken records.
* Cleansed HTML tags and formatted descriptions & facilities.
* Deduplicated entries using unique HotelCode identifiers.
* Extracted coordinates (`Latitude` & `Longitude`) from map fields.

### 2. Feature Engineering & Transformation
* Extracted features like FacilitiesCount and DescriptionLength.
* Built robust scikit-learn pipelines with StandardScaler and OneHotEncoder.

### 3. Machine Learning Models
* Baseline: Dummy Regressor (Mean strategy).
* Model 1: Linear Regression (Achieved top performance with $R^2 \approx 0.86$).
* Model 2: Random Forest Regressor (Ensemble of 100 decision trees).

### 4. Graphical User Interface (GUI)
* User-friendly interface allowing users to input hotel specifications and get instant value estimates.
  
---

## 📊 Evaluation Results

| Model | MAE | RMSE | $R^2$ |
| :--- | :--- | :--- | :--- |
| **Baseline (Dummy)** | 46.58 | 53.20 | -0.00 |
| **Linear Regression** | **15.98** | **20.01** | **0.86** |
| **Random Forest Regressor** | 17.12 | 21.45 | 0.84 |

---

## 🛠️ **Key Features & Implementation**

* **Machine Learning Pipeline:** Trained a **KNN model** to compute feature distances, outputting the top 5 closest matches alongside their compatibility percentages.
* **User Interfaces (GUI):** Built functional **Web** and **Application** dashboards for seamless filtering and interactive hotel exploration.

---
## 🚀 How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SimonAbdelmalak/MLProject_NTI.git](https://github.com/SimonAbdelmalak/MLProject_NTI.git)
   cd MLProject_NTI

