from flask import Flask, render_template, request
import os
import pickle
import numpy as np

app = Flask(__name__)

FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol',
    'fbs', 'restecg', 'thalach', 'exang',
    'oldpeak', 'slope', 'ca', 'thal'
]

MODEL_PATH = os.path.join('model', 'model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET'])
def predict_form():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Extract and validate all 13 feature values
    values = []
    for feature in FEATURES:
        val = request.form.get(feature, '').strip()
        if val == '':
            return render_template('predict.html', error=f"Missing required field: {feature}")
        try:
            values.append(float(val))
        except ValueError:
            return render_template('predict.html', error=f"Invalid value for '{feature}': must be numeric")

    # Load model and scaler
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return render_template('error.html', message="Model files not found. Please train the model first."), 500

    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
    except Exception as e:
        return render_template('error.html', message=f"Failed to load model: {e}"), 500

    # Scale input and predict
    try:
        input_array = np.array(values).reshape(1, -1)
        scaled = scaler.transform(input_array)
        prediction = int(model.predict(scaled)[0])
        probability = float(model.predict_proba(scaled)[0][1])
    except Exception as e:
        return render_template('error.html', message=f"Prediction failed: {e}"), 500

    label = "Heart Disease Detected" if prediction == 1 else "No Heart Disease"
    probability_pct = int(round(probability * 100))

    return render_template(
        'result.html',
        label=label,
        prediction=prediction,
        probability=probability,
        probability_pct=probability_pct,
        age=int(values[0])
    )


if __name__ == '__main__':
    app.run(debug=True)
