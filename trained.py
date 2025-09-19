import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error

# Load dataset
df = pd.read_csv("data.csv")

# Select only 4 features + target
FEATURES = ["CRIM", "RM", "TAX", "LSTAT"]
TARGET = "MEDV"

X = df[FEATURES]
y = df[TARGET]

# Handle missing values (if any)
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate model (optional)
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
print(f"✅ MSE on test set: {mse:.2f}")

# Save model + imputer
with open("land_price_model_4features.pkl", "wb") as f:
    pickle.dump(model, f)

with open("imputer_4features.pkl", "wb") as f:
    pickle.dump(imputer, f)

print("✅ Training complete! Model saved as land_price_model_4features.pkl")
