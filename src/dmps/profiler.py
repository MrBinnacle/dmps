"""
Performance profiling and monitoring utilities.
"""

import time
from functools import wraps
from typing import Any, Callable


def performance_monitor(threshold: float = 0.1):
    """Decorator to monitor function performance"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start_time
                if duration > threshold:
                    from .error_handler import error_handler

                    error_handler.log_performance_issue(
                        f"{func.__module__}.{func.__name__}", duration, threshold
                    )

        return wrapper

    return decorator


class PerformanceTracker:
    """Track performance metrics"""

    def __init__(self):
        self.metrics = {}

    def track_operation(self, operation: str, duration: float):
        """Track operation performance"""
        if operation not in self.metrics:
            self.metrics[operation] = []
        self.metrics[operation].append(duration)

    def get_average_time(self, operation: str) -> float:
        """Get average execution time for operation"""
        times = self.metrics.get(operation, [])
        return sum(times) / len(times) if times else 0.0

    def get_slow_operations(self, threshold: float = 0.1) -> dict:
        """Get operations exceeding threshold"""
        return {
            op: self.get_average_time(op)
            for op in self.metrics
            if self.get_average_time(op) > threshold
        }


# Global performance tracker
performance_tracker = PerformanceTracker()
