# analytic_module.py

from typing import List, Dict
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ----------------------------
# ماژول تحلیلی نمونه
# ----------------------------
def analytic_module(inputs: List[float]) -> Dict[str, float]:
    """
    ورودی: لیستی از اعداد
    خروجی: دیکشنری شامل جمع و میانگین
    """
    total = sum(inputs)
    mean = total / len(inputs) if inputs else 0
    return {"total": total, "mean": mean}

# ----------------------------
# تست واحد
# ----------------------------
def test_analytic_module():
    sample_input = [1, 2, 3, 4]
    expected_output = {"total": 10, "mean": 2.5}
    output = analytic_module(sample_input)
    assert output == expected_output, f"Failed: {output}"
    print("Unit test passed ✅")

# ----------------------------
# تست انتها به انتها با معیار دقت
# ----------------------------
def evaluate_module(predictions: List[int], labels: List[int]):
    metrics = {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, zero_division=0),
        "recall": recall_score(labels, predictions, zero_division=0),
        "f1_score": f1_score(labels, predictions, zero_division=0)
    }
    return metrics

# ----------------------------
# مثال اجرا
# ----------------------------
if __name__ == "__main__":
    # اجرای ماژول
    data = [10, 20, 30]
    result = analytic_module(data)
    print("Output:", result)

    # اجرای تست واحد
    test_analytic_module()

    # تست انتها به انتها
    y_true = [1, 0, 1, 1]
    y_pred = [1, 0, 0, 1]
    metrics = evaluate_module(y_pred, y_true)
    print("Evaluation Metrics:", metrics)
