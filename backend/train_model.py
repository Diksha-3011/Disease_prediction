
import os
import joblib
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "Copy_of_Health.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")


df = pd.read_csv(CSV_PATH)


X = df.drop(columns=["id", "PID", "Problem"])

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Problem"])


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


models = {

    "xgboost": XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        random_state=42,
        eval_metric="mlogloss"
    ),

    "lightgbm": LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=-1,
        random_state=42,
        verbosity=-1
    ),

    "decision_tree": DecisionTreeClassifier(
        random_state=42
    ),

    "random_forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "knn": KNeighborsClassifier(
        n_neighbors=5
    )
}


accuracies = {}

os.makedirs(MODEL_DIR, exist_ok=True)


for name, model in models.items():

    print("\nTraining:", name)

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)

    accuracies[name] = float(accuracy)

    print(f"{name} accuracy: {accuracy:.4f}")

    model_path = os.path.join(
        MODEL_DIR,
        f"{name}_model.joblib"
    )

    joblib.dump(model, model_path)

    print("Saved:", model_path)


joblib.dump(
    scaler,
    os.path.join(MODEL_DIR, "scaler.joblib")
)


joblib.dump(
    list(X.columns),
    os.path.join(MODEL_DIR, "feature_order.joblib")
)


joblib.dump(
    accuracies,
    os.path.join(MODEL_DIR, "accuracies.joblib")
)


joblib.dump(
    label_encoder,
    os.path.join(MODEL_DIR, "label_encoder.joblib")
)


print("\n-----------------------------")
print("ALL MODEL ACCURACIES")
print("-----------------------------")

for name, accuracy in accuracies.items():

    print(
        f"{name}: {accuracy * 100:.2f}%"
    )


print("\n-----------------------------")
print("CLASS NAMES")
print("-----------------------------")

for number, name in enumerate(label_encoder.classes_):

    print(
        f"{number} -> {name}"
    )


print("\nAll models and files saved successfully.")

