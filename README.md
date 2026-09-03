# 🏨 TravelMate — Hotel Recommendation & Value Prediction System
An end-to-end Machine Learning project combining **Hotel Valuation** via Regression models and a personalized **Hotel Recommendation System** using K-Nearest Neighbors (KNN), integrated with an intuitive Graphical User Interface (GUI).
---
## 📌 About The Project
**TravelMate** helps users discover the best accommodations and evaluate hotel pricing based on amenities, rating, and location. 
The system provides:
* **Value Prediction:** Estimates the expected market value/price of a hotel using predictive regression models.
* **Smart Recommendation:** Uses the **K-Nearest Neighbors (KNN)** algorithm to compute similarity metrics and suggest the **top 5 matching hotels** with an associated compatibility/match percentage (%).
### 🌍 Geographic Coverage
* 🇪🇬 **Egypt**
* 🇨🇭 **Switzerland**
* 🇫🇷 **France**
* 🇪🇸 **Spain**
---
## 👥 Team & Responsibilities

| Role / Task | Responsible Member | Details |
| :--- | :--- | :--- |
| **Data Preprocessing** | **Simon** | Data cleaning, deduplication, missing value imputation, regex text normalization, and coordinate parsing. |
| **Model 1 (Linear Regression)** | **Marian** | Implementation of baseline (`DummyRegressor`) and Linear Regression pipelines. |
| **Model 2 (Random Forest)** | **Martina** | Training, fine-tuning, and evaluation of the Random Forest Regressor. |
| **Model 3 (KNN Recommendation)** | **Mariam & Ganna** | Building the K-Nearest Neighbors (KNN) model for similarity search and hotel matching. |
| **Prediction & Accuracy** | **Marian & Martina** | Metric computations (MAE, RMSE, $R^2$), error analysis, and comparative benchmarking. |
| **GUI Development** | **Ganna & Mariam** | Designing and integrating the interactive GUI for both prediction and recommendation. |

---
## 🛠️ Project Workflow
1. **Data Cleaning & Exploration:**
   - Cleansed raw HTML tags from textual features (`Description`, `HotelFacilities`, `Address`).
   - Handled missing attributes and dropped broken location records.
   - Removed 32,000+ duplicate records based on the unique `HotelCode`.
   - Extracted numerical coordinates (`Latitude` and `Longitude`) from map strings.
2. **Feature Engineering & Transformation:**
   - Engineered quantitative metrics including `FacilitiesCount` and `DescriptionLength`.
   - Built Scikit-Learn pipelines leveraging `StandardScaler` for continuous features and `OneHotEncoder` for categorical country labels.
3. **Machine Learning Pipeline:**
   - **Model 1 (Linear Regression):** Linear model to estimate hotel worth with high interpretability.
   - **Model 2 (Random Forest):** Ensemble regressor for capturing non-linear relationships.
   - **Model 3 (KNN Recommendation):** Distance-based similarity model to retrieve the top 5 closest hotel alternatives.
4. **Graphical User Interface (GUI):**
   - User-friendly dashboard for real-time value estimation and interactive hotel exploration.
---
## 📊 Regression Evaluation Results

| Model | MAE | RMSE | $R^2$ | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline (Dummy Regressor)** | 46.58 | 53.20 | -0.00 | Reference Benchmark |
| **Linear Regression** | **15.98** | **20.01** | **0.86** | **Top Performer** |
| **Random Forest Regressor** | 17.12 | 21.45 | 0.84 | Strong Baseline |

---
## 🚀 How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SimonAbdelmalak/MLProject_NTI.git](https://github.com/SimonAbdelmalak/MLProject_NTI.git)
   cd MLProject_NTI
