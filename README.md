# Heart Disease Prediction System ❤️

An AI-powered full-stack web application designed to assess cardiovascular risk. It utilizes a **Random Forest Classifier** trained on real clinical data (from the UCI Heart Disease Dataset) to predict the likelihood of heart disease based on 13 patient physiological features. The application features a custom, responsive dark ECG-themed user interface.

## 🚀 Features
- **AI Prediction Engine:** Powered by a Random Forest model achieving **~98.5% accuracy** on the test set.
- **Three-Section Clinical Input Form:** Easy-to-use inputs grouped logically:
  1. **Personal Info:** Age and sex.
  2. **Cardiac Symptoms:** Chest pain type, exercise-induced angina, maximum heart rate, ST segment depression, and slope.
  3. **Vitals & Lab Results:** Resting blood pressure, serum cholesterol, fasting blood sugar, resting ECG, and thalassemia.
- **Dynamic Assessment:** Displays numerical risk probability alongside a clear visual indicator (High/Low risk).
- **Personalized Recommendations:** Provides age-specific and risk-specific cardiovascular diet recommendations (foods to eat and foods to avoid).
- **Presentation Generator:** Includes a built-in Python script (`make_ppt.py`) to generate a professional, custom-styled PowerPoint slide deck summarizing the project architecture, features, and results.
- **Unit & Integration Tests:** A comprehensive testing suite using `pytest` to validate preprocessing, training, model persistence, and prediction logic.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Jinja2 Templates, Gunicorn (WSGI)
- **Machine Learning:** Scikit-learn (Random Forest Classifier, StandardScaler), Pandas, NumPy
- **Frontend:** HTML5, CSS3 (Modern dark mode style with ECG-themed styling), JavaScript (Client-side validation and interactive loading indicators)
- **Presentation:** python-pptx (Custom automation script)
- **Testing:** Pytest, Hypothesis

---

## 📋 Medical Features Table
The prediction model requires the following 13 clinical inputs:

| Feature | Description | Range / Options |
| :--- | :--- | :--- |
| **age** | Patient age in years | 29 – 77 |
| **sex** | Biological sex | `0` = Female, `1` = Male |
| **cp** | Chest pain type | `0` = Typical Angina, `1` = Atypical Angina, `2` = Non-anginal, `3` = Asymptomatic |
| **trestbps**| Resting blood pressure (in mm Hg on admission to the hospital) | 94 – 200 |
| **chol** | Serum cholesterol in mg/dl | 126 – 564 |
| **fbs** | Fasting blood sugar > 120 mg/dl | `0` = Normal (≤120), `1` = High (>120) |
| **restecg** | Resting electrocardiographic results | `0` = Normal, `1` = ST-T Wave Abnormality, `2` = Left Ventricular Hypertrophy |
| **thalach** | Maximum heart rate achieved during exercise | 71 – 202 bpm |
| **exang** | Exercise induced angina | `0` = No, `1` = Yes |
| **oldpeak** | ST depression induced by exercise relative to rest | 0 – 6.2 |
| **slope** | The slope of the peak exercise ST segment | `0` = Upsloping, `1` = Flat, `2` = Downsloping |
| **ca** | Number of major vessels colored by fluoroscopy | 0 – 4 |
| **thal** | Thalassemia blood disorder type | `0` = Normal, `1` = Fixed Defect, `2` = Reversible Defect, `3` = Unknown |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/Gnaneswar-1214/Hearth-disease-.git
cd Hearth-disease-
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Obtain Dataset
1. Download the **Kaggle Heart Disease Dataset** (e.g., from [Kaggle UCI Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)).
2. Place the downloaded CSV file in the root folder of the project.
3. Rename the file to `dataset.csv`.

### 4. Train the Machine Learning Model
Run the offline training script to preprocess the data, train the Random Forest Classifier, and save the serialized model and scaler:
```bash
python train_model.py
```
This will save `model.pkl` and `scaler.pkl` under the `model/` directory.

### 5. Run the Web Server Locally
Start the Flask development server:
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to access the application.

---

## 🧪 Testing
Run the automated testing suite using `pytest`:
```bash
python -m pytest
```

---

## 📊 Presentation Slide Generation
To generate the PowerPoint presentation summarizing this project (`Heart_Disease_Prediction_PPT.pptx`), execute:
```bash
python make_ppt.py
```
