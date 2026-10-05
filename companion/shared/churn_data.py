"""Shared synthetic churn dataset used by Version 0 (Chapter 2) and referenced
in Chapters 3-4's evaluation and PyTorch examples. Centralized here so every
version of the AI Knowledge Assistant project uses the exact same data.
"""

import pandas as pd

CHURN_DF = pd.DataFrame({
    "tenure_months":   [24, 3, 41, 6, 30, 2, 55, 8, 12, 45, 36, 4, 60, 7, 28, 3, 48, 9, 18, 50],
    "monthly_spend":   [49.99, 89.99, 19.99, 79.99, 39.99, 99.99, 29.99, 69.99, 59.99, 24.99,
                        44.99, 94.99, 22.99, 84.99, 34.99, 92.99, 27.99, 74.99, 54.99, 21.99],
    "support_tickets": [0, 4, 1, 5, 0, 6, 0, 3, 2, 0, 1, 5, 0, 4, 0, 6, 0, 4, 1, 0],
    "churned":         [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
})

FEATURE_COLUMNS = ["tenure_months", "monthly_spend", "support_tickets"]
