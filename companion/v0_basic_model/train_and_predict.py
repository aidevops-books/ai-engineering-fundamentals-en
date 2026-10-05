"""AI Knowledge Assistant -- Version 0: Basic AI Application (Chapter 2).

A classical ML classifier wrapped in application code -- no LLM involved yet.
Verified runnable end to end with no external API or network access needed.

Run:
    python train_and_predict.py
"""

import sys
from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))
from churn_data import CHURN_DF, FEATURE_COLUMNS  # noqa: E402


def main() -> None:
    X = CHURN_DF[FEATURE_COLUMNS]
    y = CHURN_DF["churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    print("baseline accuracy:", accuracy_score(y_test, baseline.predict(X_test)))

    model = LogisticRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("model accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division=0))

    new_customer = pd.DataFrame({
        "tenure_months": [5], "monthly_spend": [84.99], "support_tickets": [3],
    })
    print("churn prediction for a new customer:", model.predict(new_customer))


if __name__ == "__main__":
    main()
