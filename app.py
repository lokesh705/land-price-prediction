from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load trained 4-feature model
with open("land_price_model_4features.pkl", "rb") as f:
    model = pickle.load(f)

with open("imputer_4features.pkl", "rb") as f:
    imputer = pickle.load(f)

FEATURES = ["CRIM", "RM", "TAX", "LSTAT"]

@app.route("/")
def home():
    return render_template("index.html")  # Serve your HTML page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # JSON sent from JS

        # Extract features in correct order
        input_list = []
        for feature in FEATURES:
            value = data.get(feature, 0)  # default 0 if missing
            input_list.append(float(value))

        # Apply imputer for missing values
        input_array = imputer.transform([input_list])

        # Predict price
        predicted_price = round(model.predict(input_array)[0] * 1000, 2)  # MEDV in $1000s

        return jsonify({"price": predicted_price})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
