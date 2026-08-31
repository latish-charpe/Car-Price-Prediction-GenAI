import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("cardekho_dataset.csv")

# Display first 5 rows
print(df.head())

# Dataset information
print("\nDataset Information:")
print(df.info())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns.tolist())

# Remove unnecessary column
df.drop(columns=["Unnamed: 0"], inplace=True)

print("\nAfter removing unnecessary column:")
print(df.head())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Display duplicate rows
print("\nSample Duplicate Rows:")
print(df[df.duplicated()].head())

# Remove duplicate rows
df.drop_duplicates(inplace=True)

print("\nDataset Shape After Removing Duplicates:")
print(df.shape)

print("\nRemaining Duplicate Rows:")
print(df.duplicated().sum())

# Categorical columns
categorical_columns = df.select_dtypes(include="object").columns

print("\nCategorical Columns:")
print(categorical_columns.tolist())

# Check unique values
for column in categorical_columns:
    print(f"\n{column}:")
    print(f"Unique Values: {df[column].nunique()}")
    print(df[column].unique()[:20])

    # Numerical columns
numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

print("\nNumerical Columns:")
print(numerical_columns.tolist())

print("\nStatistical Summary:")
print(df[numerical_columns].describe())

# Check invalid seat values
print("\nInvalid Seat Records:")
print(df[df["seats"] <= 0])

# Check extremely high km_driven values
print("\nTop 10 Highest KM Driven Cars:")
print(
    df[["car_name", "vehicle_age", "km_driven", "selling_price"]]
    .sort_values(by="km_driven", ascending=False)
    .head(10)
)

# Check highest selling price cars
print("\nTop 10 Most Expensive Cars:")
print(
    df[["car_name", "brand", "vehicle_age", "selling_price"]]
    .sort_values(by="selling_price", ascending=False)
    .head(10)
)

# Remove invalid seat records
df = df[df["seats"] > 0]

# Remove the clearly unrealistic extreme kilometer record
df = df[df["km_driven"] < 2000000]

print("\nDataset Shape After Cleaning Invalid Records:")
print(df.shape)

print("\nRemaining Invalid Seats:")
print((df["seats"] <= 0).sum())

print("\nMaximum KM Driven:")
print(df["km_driven"].max())

# -------------------------------
# OUTLIER DETECTION USING IQR
# -------------------------------

outlier_columns = [
    "vehicle_age",
    "km_driven",
    "mileage",
    "engine",
    "max_power",
    "selling_price"
]

print("\nOUTLIER ANALYSIS USING IQR")

for column in outlier_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(f"\nColumn: {column}")
    print(f"Lower Bound: {lower_bound}")
    print(f"Upper Bound: {upper_bound}")
    print(f"Number of Outliers: {len(outliers)}")

    # -------------------------------
# INSPECT MILEAGE OUTLIERS
# -------------------------------

Q1 = df["mileage"].quantile(0.25)
Q3 = df["mileage"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

mileage_outliers = df[
    (df["mileage"] < lower_bound) |
    (df["mileage"] > upper_bound)
]

print("\nMILEAGE OUTLIERS:")
print(
    mileage_outliers[
        ["car_name", "brand", "fuel_type", "vehicle_age", "mileage"]
    ].sort_values(by="mileage")
)

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------

# Convert selling price into lakhs
df["price_in_lakh"] = df["selling_price"] / 100000

print("\nFeature Engineering Completed!")

print(
    df[["car_name", "selling_price", "price_in_lakh"]].head()
)

# -------------------------------
# SAVE CLEANED DATASET
# -------------------------------

df.to_csv("cleaned_car_data.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("File name: cleaned_car_data.csv")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Columns:")
print(df.columns.tolist())