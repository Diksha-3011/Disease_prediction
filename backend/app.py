
import os
import joblib
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

app = Flask(__name__)
CORS(app)


FIELDS = [
    ("age", "age"),
    ("gender", "gender"),
    ("bodypain", "bodypain"),
    ("hollow", "Hollow"),
    ("cold_and_cough", "cold and cough"),
    ("cough", "cough"),
    ("fever", "fever"),
    ("chest_pain", "chest pain"),
    ("breathing_problem", "breathing problem"),
    ("throat_pain", "Throat pain"),
    ("head_pain", "head pain"),
    ("stomach_pain", "stomach pain"),
    ("diarrhea", "diarrhea"),
    ("omitting", "omitting"),
    ("back_pain", "back pain"),
    ("swollen_feet", "Swollen feet")
]


DEFAULT_ORDER = [column for _, column in FIELDS]


MODEL_NAMES = [
    "xgboost",
    "lightgbm",
    "decision_tree",
    "random_forest",
    "knn"
]


models = {}

for name in MODEL_NAMES:

    model_path = os.path.join(
        MODEL_DIR,
        f"{name}_model.joblib"
    )

    models[name] = joblib.load(model_path)


scaler = joblib.load(
    os.path.join(MODEL_DIR, "scaler.joblib")
)


feature_order = joblib.load(
    os.path.join(MODEL_DIR, "feature_order.joblib")
)


accuracies = joblib.load(
    os.path.join(MODEL_DIR, "accuracies.joblib")
)


label_encoder = joblib.load(
    os.path.join(MODEL_DIR, "label_encoder.joblib")
)


print("\nModels loaded successfully.")

for name in MODEL_NAMES:
    print(
        f"{name}: {accuracies[name] * 100:.2f}%"
    )


def build_row(data):

    row = {}

    age = int(data.get("age", 0))
    gender = int(data.get("gender", 0))
    fever = float(data.get("fever", 0))


    if age < 15 or age > 95:
        raise ValueError(
            "Age must be between 15 and 95."
        )


    if gender not in [1, 2]:
        raise ValueError(
            "Invalid gender value."
        )


    if fever < 95 or fever > 108:
        raise ValueError(
            "Temperature must be between 95 and 108."
        )


    row["age"] = age
    row["gender"] = gender
    row["fever"] = fever


    for key, column in FIELDS:

        if key in ["age", "gender", "fever"]:
            continue

        value = int(data.get(key, 2))

        if value not in [1, 2]:
            raise ValueError(
                f"Invalid value for {key}."
            )

        row[column] = value


    return row


def prepare_input(row):

    values = []

    for column in feature_order:

        if column not in row:
            raise ValueError(
                f"Missing feature: {column}"
            )

        values.append(row[column])


    df = pd.DataFrame(
        [values],
        columns=feature_order
    )


    scaled = scaler.transform(df)

    return scaled


def get_model_predictions(input_data):

    all_predictions = {}

    for name in MODEL_NAMES:

        model = models[name]

        probabilities = model.predict_proba(
            input_data
        )[0]


        predictions = model.classes_

        model_results = []

        for class_id, probability in zip(
            predictions,
            probabilities
        ):

            disease = label_encoder.inverse_transform(
                [int(class_id)]
            )[0]


            model_results.append({
                "condition": disease,
                "confidence": float(probability)
            })


        all_predictions[name] = {
            "prediction": model_results[
                probabilities.argmax()
            ]["condition"],

            "confidence": float(
                probabilities.max()
            ),

            "probabilities": model_results,

            "accuracy": float(
                accuracies[name]
            )
        }


    return all_predictions


def calculate_ensemble(all_predictions):

    disease_scores = {}

    disease_model_count = {}


    for model_name, result in all_predictions.items():

        model_accuracy = result["accuracy"]


        for item in result["probabilities"]:

            disease = item["condition"]
            confidence = item["confidence"]


            weighted_score = (
                confidence * model_accuracy
            )


            if disease not in disease_scores:

                disease_scores[disease] = 0
                disease_model_count[disease] = 0


            disease_scores[disease] += weighted_score

            disease_model_count[disease] += 1


    final_results = []


    for disease, score in disease_scores.items():

        model_count = disease_model_count[disease]


        average_score = score / model_count


        final_results.append({
            "condition": disease,
            "probability": round(
                average_score,
                4
            ),
            "model_count": model_count
        })


    final_results.sort(
        key=lambda x: x["probability"],
        reverse=True
    )


    return final_results[:3]


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No input data received."
            }), 400


        row = build_row(data)

        input_data = prepare_input(row)


        all_predictions = get_model_predictions(
            input_data
        )


        final_results = calculate_ensemble(
            all_predictions
        )


        if not final_results:

            return jsonify({
                "error": "No prediction generated."
            }), 500


        top_result = final_results[0]


        response = {

            "prediction":
                top_result["condition"],

            "confidence":
                top_result["probability"],

            "top":
                final_results,

            "model_predictions":
                all_predictions
        }


        return jsonify(response)


    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            "error": str(error)
        }), 400


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "models": MODEL_NAMES
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

