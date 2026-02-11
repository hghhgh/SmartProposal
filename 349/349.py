from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol
import statistics
import time
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


@dataclass
class Alert:
    level: str
    message: str
    metric: str
    value: float
    threshold: float
    timestamp: float


class Notifier(Protocol):
    def send(self, alert: Alert) -> None:
        ...


class ConsoleNotifier:
    def send(self, alert: Alert) -> None:
        logging.warning(
            "ALERT-%s | %s | %s=%.4f (threshold=%.4f)",
            alert.level.upper(),
            alert.message,
            alert.metric,
            alert.value,
            alert.threshold
        )


class WebhookNotifier:
    def __init__(self, url: str):
        self.url = url

    def send(self, alert: Alert) -> None:
        payload = {
            "level": alert.level,
            "message": alert.message,
            "metric": alert.metric,
            "value": alert.value,
            "threshold": alert.threshold,
            "timestamp": alert.timestamp
        }
        try:
            requests.post(self.url, json=payload, timeout=2)
        except requests.RequestException as e:
            logging.error("Webhook ارسال نشد: %s", e)


class DataQualityMonitor:
    def __init__(self, notifier: Notifier, thresholds: Optional[Dict[str, float]] = None):
        self.notifier = notifier
        self.thresholds = thresholds or {
            "missing_ratio": 0.2,
            "outlier_ratio": 0.1,
            "std_min": 0.01
        }

    def analyze(self, data: List[Optional[float]]) -> Dict[str, float]:
        if not data:
            return {"missing_ratio": 1.0, "outlier_ratio": 0.0, "std_value": 0.0}

        missing_ratio = sum(x is None for x in data) / len(data)
        clean_data = [x for x in data if x is not None]

        if len(clean_data) < 2:
            return {"missing_ratio": missing_ratio, "outlier_ratio": 0.0, "std_value": 0.0}

        std_value = statistics.stdev(clean_data)

        if std_value == 0:
            outlier_ratio = 0.0
        else:
            mean = statistics.mean(clean_data)
            outlier_ratio = sum(abs(x - mean) > 3 * std_value for x in clean_data) / len(clean_data)

        return {"missing_ratio": missing_ratio, "outlier_ratio": outlier_ratio, "std_value": std_value}

    def check_and_alert(self, metrics: Dict[str, float]) -> None:
        now = time.time()

        if metrics["missing_ratio"] > self.thresholds["missing_ratio"]:
            self._emit(
                "critical",
                "نسبت داده‌های گمشده بیش از حد مجاز است",
                "missing_ratio",
                metrics["missing_ratio"],
                self.thresholds["missing_ratio"],
                now
            )

        if metrics["outlier_ratio"] > self.thresholds["outlier_ratio"]:
            self._emit(
                "warning",
                "داده‌های پرت مشکوک شناسایی شد",
                "outlier_ratio",
                metrics["outlier_ratio"],
                self.thresholds["outlier_ratio"],
                now
            )

        if metrics["std_value"] < self.thresholds["std_min"]:
            self._emit(
                "warning",
                "کاهش تنوع داده (احتمال فریز شدن منبع)",
                "std_value",
                metrics["std_value"],
                self.thresholds["std_min"],
                now
            )

    def _emit(self, level: str, message: str, metric: str, value: float, threshold: float, timestamp: float) -> None:
        alert = Alert(level=level, message=message, metric=metric, value=value, threshold=threshold, timestamp=timestamp)
        self.notifier.send(alert)


if __name__ == "__main__":
    # نمونه داده
    sample_data: List[Optional[float]] = [10, 11, 10, None, 10, 10, 500]

    # استفاده از notifier حرفه‌ای
    console_notifier = ConsoleNotifier()
    # webhook_notifier = WebhookNotifier("https://example.com/webhook")

    monitor = DataQualityMonitor(console_notifier)
    metrics = monitor.analyze(sample_data)
    monitor.check_and_alert(metrics)
