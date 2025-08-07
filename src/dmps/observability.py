"""
Observability dashboard for context engineering metrics.
"""

from typing import List

from .evaluation import context_evaluator
from .token_tracker import token_tracker


class ObservabilityDashboard:
    """Dashboard for monitoring context engineering performance"""

    def print_session_summary(self):
        """Print current session summary"""
        summary = token_tracker.get_session_summary()
        trend = context_evaluator.get_performance_trend()

        print("=" * 60)
        print("CONTEXT ENGINEERING OBSERVABILITY DASHBOARD")
        print("=" * 60)

        # Token metrics
        print("Token Metrics:")
        print(f"   • Total Operations: {summary.get('total_operations', 0)}")
        print(f"   • Token Reduction: {summary.get('total_token_reduction', 0)}")
        print(f"   • Cost Savings: ${summary.get('estimated_cost_savings', 0):.4f}")
        print(f"   • Processing Time: {summary.get('processing_time_total', 0):.2f}s")

        # Quality metrics
        print("\nQuality Metrics:")
        print(f"   • Average Score: {summary.get('average_quality_score', 0)}")
        print(f"   • Performance Trend: {trend.get('trend', 'unknown')}")
        print(f"   • Recent Average: {trend.get('recent_average', 0)}")

        # Alerts
        if trend.get("trend") == "declining":
            change_val = trend.get("change", 0)
            print(f"\nALERT: Performance declining (change: {change_val:.3f})")

        print("=" * 60)

    def print_detailed_metrics(self):
        """Print detailed performance metrics"""
        if not token_tracker.traces:
            print("No traces available")
            return

        print("\nDetailed Performance Metrics:")
        print("-" * 40)

        for i, trace in enumerate(token_tracker.traces[-5:], 1):  # Last 5 traces
            print(f"\n{i}. Operation {trace.operation_id}:")
            print(f"   Token Reduction: {trace.token_reduction}")
            print(f"   Quality Score: {trace.quality_score:.3f}")
            print(f"   Cost Estimate: ${trace.metrics.cost_estimate:.4f}")
            print(f"   Techniques: {', '.join(trace.techniques_applied)}")

    def export_metrics(self, filepath: str = "context_metrics.json"):
        """Export all metrics to file"""
        token_tracker.export_traces(filepath)
        print(f"Metrics exported to {filepath}")

    def get_performance_alerts(self) -> List[str]:
        """Get performance alerts"""
        alerts = []

        # Check for degradation
        if context_evaluator.evaluation_history:
            recent_eval = context_evaluator.evaluation_history[-1]
            if recent_eval.degradation_detected:
                alerts.append("Quality degradation detected")

            if recent_eval.token_efficiency < 0.7:
                alerts.append("Low token efficiency")

        # Check token usage trends
        summary = token_tracker.get_session_summary()
        if summary.get("total_operations", 0) > 0:
            avg_reduction = (
                summary.get("total_token_reduction", 0) / summary["total_operations"]
            )
            if avg_reduction < 0:
                alerts.append("Token usage increasing")

        return alerts


# Global dashboard instance
dashboard = ObservabilityDashboard()
