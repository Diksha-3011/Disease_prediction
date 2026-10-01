# Symptom Check: Flask API + HTML/CSS/JS frontend

A patient enters age, gender, temperature and symptoms. The page sends them to a Flask API, which uses your saved Decision Tree model (`decision_tree_model.joblib`) to predict the most likely condition.

```
health_app/
├── backend/
│   ├── app.py               Flask API (loads your saved model)
│   ├── train_model.py       optional: trains and saves a Decision Tree
│   ├── model/               put decision_tree_model.joblib here
│   ├── Copy_of_Health.csv
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## How to run

**1. Add your model**

Copy `decision_tree_model.joblib` into `backend/model/`.

**2. Start the backend**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API runs at http://127.0.0.1:5000. Keep this terminal open.

**3. Open the frontend**

Double-click `frontend/index.html`, fill in the form and choose **Predict condition**.

## What kinds of saved model work

`app.py` checks your file when it starts and tells you if something is wrong.

| How the model was saved | What to do |
|---|---|
| `joblib.dump(model, "decision_tree_model.joblib")` trained on the raw features | Works as is |
| Trained on scaled data (`StandardScaler`) | Also save the scaler with `joblib.dump(scaler, "scaler.joblib")` and put it in `backend/model/` |
| A dictionary like `{"model": ..., "scaler": ...}` or a scikit-learn Pipeline | Works as is |
| Target was `PID` (numbers) instead of `Problem` | Works: numbers are converted back to disease names |
| Trained with the `id` or `PID` columns as inputs | Retrain without them: `X = df.drop(columns=["id", "PID", "Problem"])` |

The 16 inputs, in dataset order, are: age, gender, bodypain, Hollow, cold and cough, cough, fever, chest pain, breathing problem, Throat pain, head pain, stomach pain, diarrhea, omitting, back pain, Swollen feet.

If you do not have a working model file, run `python train_model.py` inside `backend/`. It trains a Decision Tree and saves it to the right place.

## API

`POST /predict` with JSON. Symptoms use `1` = yes and `2` = no.

```json
{
  "age": 35, "gender": 1, "fever": 101,
  "bodypain": 1, "hollow": 2, "cold_and_cough": 2, "cough": 2,
  "chest_pain": 2, "breathing_problem": 2, "throat_pain": 2,
  "head_pain": 1, "stomach_pain": 2, "diarrhea": 2,
  "omitting": 2, "back_pain": 2, "swollen_feet": 2
}
```

Response:

```json
{
  "prediction": "Dengue",
  "confidence": 1.0,
  "top": [
    { "condition": "Dengue", "probability": 1.0 },
    { "condition": "Acidity", "probability": 0.0 },
    { "condition": "Allergic Side Effects", "probability": 0.0 }
  ]
}
```

Invalid input returns status `400` with `{"error": "..."}`.

Allowed values: age 15 to 95, gender 1 or 2, fever 95 to 108 (the data covers 97 to 105).

## Notes

- Gender is mapped as `1` = male, `2` = female. The dataset does not say which is which, so change the labels in `index.html` if yours is the other way round.
- The dataset column `omitting` is shown as "Vomiting" in the form.
- A fully grown Decision Tree usually gives 100% to one condition and 0% to the rest, so the confidence shown is often 100%. That does not mean the prediction is certain.
- This project is for learning and is not medical advice.
