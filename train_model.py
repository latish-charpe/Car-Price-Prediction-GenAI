import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("cleaned_car_data.csv")

print("\nDataset Loaded Successfully!")
print("Dataset Shape:", df.shape)


# =========================
# FEATURES AND TARGET
# =========================

feature_columns = [
    "car_name",
    "brand",
    "model",
    "vehicle_age",
    "km_driven",
    "seller_type",
    "fuel_type",
    "transmission_type",
    "mileage",
    "engine",
    "max_power",
    "seats"
]

X = df[feature_columns]

y = df["selling_price"]


# =========================
# CATEGORICAL COLUMNS
# =========================

categorical_columns = [
    "car_name",
    "brand",
    "model",
    "seller_type",
    "fuel_type",
    "transmission_type"
]


# =========================
# NUMERICAL COLUMNS
# =========================

numerical_columns = [
    "vehicle_age",
    "km_driven",
    "mileage",
    "engine",
    "max_power",
    "seats"
]


# =========================
# PREPROCESSOR
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)


# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================
# MODELS
# =========================

models = {

    # 1. LINEAR REGRESSION
    "Linear Regression": LinearRegression(),


    # 2. DECISION TREE
    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),


    # 3. RANDOM FOREST
    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),


    # 4. GRADIENT BOOSTING
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        random_state=42
    )
}


# =========================
# TRAIN & COMPARE MODELS
# =========================

results = {}

best_model_name = None
best_model = None
best_mae = float("inf")


for name, current_model in models.items():

    print("\n" + "=" * 45)
    print(f"Training {name}...")
    print("=" * 45)


    # CREATE PIPELINE
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", current_model)
        ]
    )


    # TRAIN MODEL
    pipeline.fit(
        X_train,
        y_train
    )


    # PREDICT
    predictions = pipeline.predict(
        X_test
    )


    # =========================
    # MODEL EVALUATION
    # =========================

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )


    # STORE RESULTS
    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2
    }


    # DISPLAY RESULTS
    print(f"MAE: ₹ {mae:,.2f}")
    print(f"RMSE: ₹ {rmse:,.2f}")
    print(f"R2 Score: {r2:.4f}")


    # =========================
    # SELECT BEST MODEL
    # =========================

    if mae < best_mae:

        best_mae = mae
        best_model_name = name
        best_model = pipeline


# =========================
# RESULTS SUMMARY
# =========================

print("\n" + "=" * 55)
print("MODEL COMPARISON RESULTS")
print("=" * 55)

results_df = pd.DataFrame(results).T

results_df = results_df.sort_values(
    by="MAE",
    ascending=True
)

print(results_df)


# =========================
# BEST MODEL
# =========================

print("\n🏆 BEST MODEL:", best_model_name)
print(f"Best MAE: ₹ {best_mae:,.2f}")


# =========================
# SAVE BEST MODEL
# =========================

joblib.dump(
    best_model,
    "car_price_model.pkl"
)

print("\n✅ Best Model Saved Successfully!")
print("File Name: car_price_model.pkl")


# =========================
# SAVE MODEL COMPARISON
# =========================

results_df.to_csv(
    "model_comparison.csv"
)

print("📊 Model comparison saved as: model_comparison.csv")