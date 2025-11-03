# 📊📈AI-Driven Analysis of India's Principal Commodity-Wise Exports (2021–24)

## 🔍 Overview

This project focuses on analyzing **India's Principal Commodity-wise Export Data for FY 2021–24**, sourced from the **Government of India Open Data Portal**. It uses **Data Science, Machine Learning, and Visualization techniques** to uncover trade patterns, segment export commodities, and provide actionable insights for policymakers, investors, and exporters.

The project integrates the complete **data analytics lifecycle** — from **data cleaning and preprocessing** to **exploratory data analysis (EDA)**, **advanced analytics (PCA, K-Means, Regression models)**, and **interactive dashboard deployment using Streamlit**.

---

## 📊 Project Objectives

* Analyze India's export composition at the commodity and country level.
* Identify top-performing export sectors and countries.
* Use **unsupervised learning (K-Means)** to segment commodities by trade characteristics.
* Apply **Principal Component Analysis (PCA)** for dimensionality reduction and visualization.
* Implement regression models (**Random Forest, Linear, Decision Tree**) to understand export value prediction patterns.
* Build a **Streamlit Dashboard** for real-time, interactive exploration of export trends and model outputs.

---

## 🔢 Dataset Information

**Source:** [data.gov.in](https://data.gov.in)
**Dataset Title:** Principal Commodity-wise Export Data (FY 2021–24)
**Files Used:**

* `Principal_Commodity_wise_export_for_the_year_2021-24.xlsx` (Raw Data)
* `Cleaned_Principal_Commodity_Exports.xlsx` (Processed Data)
* `Export Data.ipynb` (Jupyter Notebook – full analysis)
* `app.py` (Streamlit Dashboard App)

**Key Columns:**

* `COMMODITY_NAME`
* `COUNTRY`
* `UNIT`
* `QUANTITY`
* `VALUE (US$ Million)`
* Derived feature: `PRICE_PER_KG = VALUE / QUANTITY`

---

## 📚 Project Workflow

### **1. Data Preprocessing & Cleaning**

* Removed null values and duplicates.
* Renamed columns for clarity.
* Created a new feature: `PRICE_PER_KG`.
* Converted datatypes and standardized numeric fields.

### **2. Exploratory Data Analysis (EDA)**

* Top 10 Commodities by Export Value & Quantity.
* Top 10 Countries by Export Value.
* Most Expensive & Cheapest Commodities per KG.
* Heatmaps and Correlation analysis.
* Interactive visualizations using **Seaborn**, **Matplotlib**, and **Plotly**.

### **3. Advanced Analytics**

* **Scaling:** Used `StandardScaler` for normalization.
* **PCA:** Reduced high-dimensional data into 2D for better interpretability.
* **K-Means Clustering:** Segmented exports into 3 distinct groups:

  * High-Value, Low-Quantity Commodities (e.g., Gold, Diamonds)
  * Bulk Low-Cost Commodities (e.g., Rice, Iron Ore)
  * Balanced Exports (e.g., Pharma, Machinery, Textiles)
* **Model Evaluation:** Used Elbow Method and Silhouette Score to validate optimal cluster count (k=3).

### **4. Regression Models (Predictive Analytics)**

Implemented the following regression models to understand and predict export values:

* **Random Forest Regressor**
* **Decision Tree Regressor**
* **Linear Regression**
  Each model was evaluated based on R² score, Mean Absolute Error (MAE), and visualization of predictions.

### **5. Visualization & Dashboard (Streamlit)**

Developed a fully interactive **Streamlit dashboard** enabling users to:

* Filter data by **country**, **commodity**, or **cluster**.
* Visualize top exports via **bar charts**, **scatter plots**, and **heatmaps**.
* View PCA-based cluster visualizations and regression model insights.
* Explore key metrics such as export value, average price per kg, and country contribution.

---

## 🔧 Tech Stack & Tools

**Languages:** Python 3.13
**Libraries:** Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib, Plotly, Streamlit
**Environment:** Jupyter Notebook, VS Code
**Data Source:** [data.gov.in](https://data.gov.in)
**Dashboard Framework:** Streamlit
**Machine Learning Models:** PCA, K-Means, Random Forest, Decision Tree, Linear Regression

---

## 📊 Key Insights

* India’s export structure shows clear segmentation between **high-value niche exports** and **bulk low-cost commodities**.
* **Gold and precious stones** dominate export value despite low shipment volume.
* **Agricultural and raw materials** form the backbone of volume-driven trade.
* **Pharmaceuticals and industrial goods** create a balanced export portfolio.
* Clustering provides actionable grouping that aligns with India’s trade categories.

---

## 💡 Impact & Applications

* **Policy Making:** Helps identify high-revenue and high-volume export sectors.
* **Investor Insights:** Aids in recognizing profitable trade clusters.
* **Trade Strategy:** Supports data-driven decision-making for export diversification.
* **Educational Use:** Demonstrates integration of analytics, ML, and visualization in a real-world dataset.

---

## 📊 Results Summary

| **Model / Method** | **Purpose**              | **Key Output / Metric**                       |
| ------------------ | ------------------------ | --------------------------------------------- |
| PCA                | Dimensionality Reduction | 2D visualization with 90%+ variance retention |
| K-Means (k=3)      | Clustering               | Silhouette Score: ~0.62                       |
| Random Forest      | Export Value Prediction  | R²: ~0.88                                     |
| Decision Tree      | Predictive Model         | R²: ~0.81                                     |
| Linear Regression  | Baseline Prediction      | R²: ~0.76                                     |

---

## 🔊 Streamlit Dashboard Preview

**Features:**

* Real-time filtering by country and commodity.
* Cluster-wise visualization of exports.
* PCA scatter plot for export segmentation.
* Comparative graphs for top commodities and countries.

**Run the App:**

```bash
streamlit run app.py
```

---

<img width="1919" height="856" alt="Screenshot 2025-10-27 214442" src="https://github.com/user-attachments/assets/d2a76ce6-657e-4fa5-b91f-329eca099271" />

<img width="1918" height="850" alt="Screenshot 2025-10-27 214845" src="https://github.com/user-attachments/assets/bd852624-50b9-45b6-bb3c-d12a7b87c5f8" />


## 🔖 References

1. Government of India – Open Data Portal: Principal Commodity-wise Export Dataset (FY 2021–24). [Available Here](https://data.gov.in)
2. Streamlit Documentation, Streamlit Inc., 2024. [https://docs.streamlit.io/](https://docs.streamlit.io/)
3. Scikit-learn Documentation, 2024. [https://scikit-learn.org/stable/documentation.html](https://scikit-learn.org/stable/documentation.html)
4. Plotly Express Documentation, 2024. [https://plotly.com/python/plotly-express/](https://plotly.com/python/plotly-express/)
5. Pandas Documentation, 2024. [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)

---

## 🔹 Author Information

**Name:** Atharva Kale
**PRN:** 22070521071
**Section:** C
**Semester:** VI
**Institution:** Symbiosis Institute of Technology, Nagpur
**Project Mentor:** Dr. Piyush Chahuan

---

## 🎨 Acknowledgment

This project was completed as part of the **Machine Learning Daat Science Mini Project** under the guidance of our faculty mentor. Special thanks to open data initiatives and open-source ML tools that made real-world analytics and visualization possible.

---

## 📢 License

This project is developed for academic and research purposes only.
All dataset copyrights belong to **Government of India (data.gov.in)**.
