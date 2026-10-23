# 🚗 Car Price Prediction & Estimation System

A Machine Learning-based web application that estimates the selling price of used cars based on their specifications. The project includes data preprocessing, model comparison, price prediction, and PDF report generation through an interactive Streamlit dashboard.

## 📌 Project Overview

The system uses historical car data from the CarDekho dataset to predict estimated selling prices. Multiple regression algorithms are trained and evaluated to select the best-performing model.

## ✨ Key Features

- **Data Preprocessing:** Cleaned and prepared car data for model training.
- **Model Comparison:** Evaluated Linear Regression, Decision Tree, Random Forest, and Gradient Boosting.
- **Price Prediction:** Estimates used-car prices based on vehicle specifications.
- **Interactive Dashboard:** Provides a user-friendly interface using Streamlit.
- **PDF Report Generation:** Generates downloadable reports containing price estimation details.
- **Model Evaluation:** Uses MAE, RMSE, and R² Score to evaluate performance.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Model Serialization:** Joblib
- **Web Application:** Streamlit
- **PDF Reports:** ReportLab
- **Dataset:** CarDekho Used Car Dataset

## 📊 Dataset Information

- **Dataset:** CarDekho Used Car Dataset
- **Records:** 15,241 cleaned records
- **Target Variable:** `selling_price`

### Features Used

- Car name, brand, and model
- Vehicle age and kilometres driven
- Seller type and fuel type
- Transmission type
- Mileage, engine capacity, maximum power, and seating capacity

## 🤖 Machine Learning Models

The following regression models were trained and compared:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor

### Model Performance

| Model | MAE | RMSE | R² Score |
|---|---:|---:|---:|
| Random Forest | ₹1,10,155 | ₹5,91,486 | 0.7241 |
| Gradient Boosting | ₹1,25,175 | ₹5,94,829 | 0.7209 |
| Decision Tree | ₹1,25,643 | ₹6,18,326 | 0.6985 |
| Linear Regression | ₹2,51,904 | ₹7,68,829 | 0.5338 |

**Best Model:** Random Forest Regressor

*Note: These are results from the project's test set. Predictions are estimates and may differ from actual market prices.*

## 📂 Project Structure

```text
Car-Price-Prediction-GenAI/
│
├── app.py
├── preprocessing.py
├── train_model.py
├── requirements.txt
├── car_price_model.pkl
├── cardekho_dataset.csv
├── cleaned_car_data.csv
├── model_comparison.csv
├── car_showroom_bg.png
├── prediction_bg.png
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/latish-charpe/Car-Price-Prediction-GenAI.git
```

### 2. Navigate to the Project Folder

```bash
cd Car-Price-Prediction-GenAI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Machine Learning Model (Optional)

If the trained model file is unavailable, generate it using:

```bash
python train_model.py
```

This creates the trained model and updates the model comparison results.

### 5. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal to access the dashboard.

## 📈 Evaluation Metrics

- **MAE (Mean Absolute Error):** Measures the average absolute difference between actual and predicted prices.
- **RMSE (Root Mean Squared Error):** Penalizes larger prediction errors more heavily.
- **R² Score:** Measures how well the model explains variations in car prices.

## 🚀 Future Enhancements

- Improve prediction accuracy through hyperparameter tuning.
- Add more recent vehicle market data.
- Enhance model performance for different car segments.
- Deploy the application with improved availability and performance.

## 👨‍💻 Author

**Latish Charpe**

GitHub: [@latish-charpe](https://github.com/latish-charpe)

## 📄 License

This project is intended for educational and portfolio purposes. Add a license file if you wish to distribute it under a specific open-source license.
