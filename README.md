# 🏨 TravelMate — Hotel Recommendation & Value Prediction System
An end-to-end Machine Learning project combining **Hotel Valuation** via Regression models and a personalized **Hotel Recommendation System** using K-Nearest Neighbors (KNN), integrated with an intuitive Graphical User Interface (GUI).
---
## 📌 About The Project
**TravelMate** is designed to help users discover the most suitable accommodations based on personal preferences and evaluate fair market pricing based on amenities, rating, and geographic coordinates.
The system provides two core capabilities:
* **Smart Recommendation:** Uses the **K-Nearest Neighbors (KNN)** algorithm to compute similarity metrics across features, returning the **top 5 matching hotels** along with a calculated compatibility/match percentage (%).
* **Value Prediction:** Estimates the expected market value/price of a hotel using trained regression pipelines.
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
| **Prediction & Accuracy** | **Marian & Martina** | Metric computations (MAE, RMSE, $R^2$), error analysis, and comparative benchmarking. |
| **GUI Development** | **Ganna & Mariam** | Designing and integrating the interactive GUI for both prediction and recommendation. |

---
## 🛡️ Repository Rules & Contribution Workflow
To maintain code stability and prevent accidental overwrites, the `main` branch is protected:
* **Direct Push Restricted:** Pushing directly to `main` is strictly disabled (`git push origin main` will be rejected).
* **Pull Request Required:** All changes, bug fixes, or new features must be developed on a separate branch and submitted via a **Pull Request (PR)**.
* **Review & Approval:** Each PR requires at least **2 approvals** from collaborators before merging into `main`.
* **No Force Push:** Force pushes (`--force`) and branch deletions are blocked on the target branch.
### How to Contribute:
1. Create and switch to your feature branch:
   ```bash
   git checkout -b feature/your-feature-name