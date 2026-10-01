# 🩺 Symptom Check — Disease Prediction System

A simple machine-learning based health prediction project that takes a user's **age, gender, temperature, and symptoms** and predicts the most likely health condition.

The project uses a **Flask backend** for prediction and a simple **HTML, CSS, and JavaScript frontend** for the user interface.

> **Note:** This project is created for learning and demonstration purposes. It is not intended to provide medical diagnosis or medical advice.

---

## ✨ Features

* Enter basic patient information
* Select symptoms from the frontend
* Send prediction requests to a Flask API
* Predict the most likely health condition
* Display prediction confidence
* Show other possible conditions
* Simple and lightweight frontend
* Easy to run locally

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Machine Learning

* Scikit-learn
* Decision Tree Classifier
* Pandas
* Joblib

### Dataset

* `Copy_of_Health.csv`

---

## 📁 Project Structure

```text
health_app/
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── Copy_of_Health.csv
│   ├── requirements.txt
│   │
│   └── model/
│       ├── decision_tree_model.joblib
│       └── scaler.joblib
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 🔄 How It Works

The basic workflow of the application is:

```text
User enters details
        ↓
Age + Gender + Temperature
        ↓
Select symptoms
        ↓
Frontend sends JSON request
        ↓
Flask API receives the data
        ↓
Machine Learning Model
        ↓
Prediction + Confidence
        ↓
Result shown on the webpage
```

---

## 📊 Input Features

The model uses the following 16 features:

| Feature             | Description          |
| ------------------- | -------------------- |
| `age`               | Patient age          |
| `gender`            | Gender value         |
| `bodypain`          | Body pain            |
| `Hollow`            | Hollow               |
| `cold and cough`    | Cold and cough       |
| `cough`             | Cough                |
| `fever`             | Temperature          |
| `chest pain`        | Chest pain           |
| `breathing problem` | Breathing difficulty |
| `Throat pain`       | Throat pain          |
| `head pain`         | Head pain            |
| `stomach pain`      | Stomach pain         |
| `diarrhea`          | Diarrhea             |
| `omitting`          | Vomiting             |
| `back pain`         | Back pain            |
| `Swollen feet`      | Swollen feet         |

For symptom fields:

```text
1 = Yes
2 = No
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd health_app
```

### 2. Go to the backend

```bash
cd backend
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

If the model file is not already available:

```bash
python train_model.py
```

This creates the trained model inside the `model` folder.

### 5. Start the Flask server

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

Keep this terminal running.

---

## 🌐 Run the Frontend

Open:

```text
frontend/index.html
```

in your browser.

Enter the required information, select symptoms, and click:

**Predict Condition**

The frontend sends the information to the Flask API and displays the prediction returned by the model.

---

## 🔌 API

### `POST /predict`

The API accepts patient information in JSON format.

Example:

```json
{
  "age": 35,
  "gender": 1,
  "fever": 101,
  "bodypain": 1,
  "hollow": 2,
  "cold_and_cough": 2,
  "cough": 2,
  "chest_pain": 2,
  "breathing_problem": 2,
  "throat_pain": 2,
  "head_pain": 1,
  "stomach_pain": 2,
  "diarrhea": 2,
  "omitting": 2,
  "back_pain": 2,
  "swollen_feet": 2
}
```

Example response:

```json
{
  "prediction": "Dengue",
  "confidence": 1.0,
  "top": [
    {
      "condition": "Dengue",
      "probability": 1.0
    },
    {
      "condition": "Acidity",
      "probability": 0.0
    },
    {
      "condition": "Allergic Side Effects",
      "probability": 0.0
    }
  ]
}
```

---

## ⚙️ Input Validation

The backend currently accepts:

* **Age:** 15–95
* **Gender:** 1 or 2
* **Temperature:** 95–108

The dataset itself contains temperature values mainly between **97 and 105**.

Invalid input is returned with HTTP status:

```text
400 Bad Request
```

---

## 🧠 Model

The current version uses a **Decision Tree Classifier** trained on the health dataset.

The model is saved using Joblib:

```text
decision_tree_model.joblib
```

If scaling was used during training, the corresponding scaler is also stored:

```text
scaler.joblib
```

The application loads these files when the Flask server starts.

---

## 📝 Important Notes

* The dataset uses `Problem` as the prediction target.
* `id` and `PID` are not used as model input features.
* The dataset column `omitting` is displayed as **Vomiting** in the frontend.
* Gender values depend on the original dataset encoding.
* A fully grown Decision Tree can produce very high confidence values, sometimes even 100%.
* High model confidence should not be interpreted as medical certainty.

---

## 🎯 Purpose

This project demonstrates how a machine-learning model can be connected to a web application.

It combines:

```text
Machine Learning
       +
Flask API
       +
HTML/CSS/JavaScript
       =
End-to-End ML Web Application
```

---
## User Interface
<img width="301" height="266" alt="Screenshot 2026-10-01 151450" src="https://github.com/user-attachments/assets/38818ebc-729d-498e-bf8d-43137076b499" />

---

## ⚠️ Disclaimer

This project is intended **only for educational and demonstration purposes**.

It should not be used as a substitute for professional medical advice, diagnosis, or treatment.
