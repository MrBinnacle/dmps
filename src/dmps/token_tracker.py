"""
Token tracking and tracing for context engineering optimization.
"""

import json
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Dict, Final, List, Optional


@dataclass
class TokenMetrics:
    """Token usage metrics for a single operation"""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_estimate: float
    processing_time: float
    timestamp: float


@dataclass
class ContextTrace:
    """Trace of context engineering operations"""

    operation_id: str
    original_prompt: str
    optimized_prompt: str
    token_reduction: int
    quality_score: float
    techniques_applied: List[str]
    metrics: TokenMetrics


class TokenTracker:
    """Tracks token usage and context engineering impact"""

    # Token cost estimates (per 1K tokens)
    TOKEN_COSTS: Final = {
        "claude": {"input": 0.008, "output": 0.024},
        "chatgpt": {"input": 0.0015, "output": 0.002},
        "gemini": {"input": 0.00125, "output": 0.00375},
    }

    def __init__(self):
        self.traces: List[ContextTrace] = []
        self.session_metrics = defaultdict(list)
        self.baseline_metrics: Optional[TokenMetrics] = None

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation: 4 chars = 1 token)"""
        return max(1, len(text) // 4)

    def calculate_cost(
        self, input_tokens: int, output_tokens: int, platform: str
    ) -> float:
        """Calculate estimated cost for token usage"""
        costs = self.TOKEN_COSTS.get(platform, self.TOKEN_COSTS["chatgpt"])
        return (input_tokens * costs["input"] + output_tokens * costs["output"]) / 1000

    def start_trace(self, operation_id: str, original_prompt: str) -> Dict:
        """Start tracing a context engineering operation"""
        return {
            "operation_id": operation_id,
            "original_prompt": original_prompt,
            "start_time": time.time(),
            "original_tokens": self.estimate_tokens(original_prompt),
        }

    def complete_trace(
        self,
        trace_context: Dict,
        optimized_prompt: str,
        techniques: List[str],
        platform: str = "claude",
    ) -> ContextTrace:
        """Complete trace and calculate metrics"""
        end_time = time.time()
        processing_time = end_time - trace_context["start_time"]

        original_tokens = trace_context["original_tokens"]
        optimized_tokens = self.estimate_tokens(optimized_prompt)

        # Estimate output tokens (assume 1.5x input for response)
        estimated_output = int(optimized_tokens * 1.5)

        metrics = TokenMetrics(
            input_tokens=optimized_tokens,
            output_tokens=estimated_output,
            total_tokens=optimized_tokens + estimated_output,
            cost_estimate=self.calculate_cost(
                optimized_tokens, estimated_output, platform
            ),
            processing_time=processing_time,
            timestamp=end_time,
        )

        # Calculate quality score based on optimization
        token_reduction = original_tokens - optimized_tokens
        quality_score = min(1.0, max(0.0, token_reduction / original_tokens + 0.5))

        trace = ContextTrace(
            operation_id=trace_context["operation_id"],
            original_prompt=trace_context["original_prompt"],
            optimized_prompt=optimized_prompt,
            token_reduction=token_reduction,
            quality_score=quality_score,
            techniques_applied=techniques,
            metrics=metrics,
        )

        self.traces.append(trace)
        self.session_metrics[platform].append(metrics)

        return trace

    def get_session_summary(self) -> Dict:
        """Get summary of current session metrics"""
        if not self.traces:
            return {"total_operations": 0}

        total_operations = len(self.traces)
        total_token_reduction = sum(t.token_reduction for t in self.traces)
        avg_quality_score = sum(t.quality_score for t in self.traces) / total_operations
        total_cost_saved = sum(
            self.calculate_cost(
                abs(t.token_reduction), abs(t.token_reduction), "claude"
            )
            for t in self.traces
            if t.token_reduction > 0
        )

        return {
            "total_operations": total_operations,
            "total_token_reduction": total_token_reduction,
            "average_quality_score": round(avg_quality_score, 3),
            "estimated_cost_savings": round(total_cost_saved, 4),
            "processing_time_total": sum(
                t.metrics.processing_time for t in self.traces
            ),
        }

    def export_traces(self, filepath: str):
        """Export traces to JSON file"""
        data = {
            "session_summary": self.get_session_summary(),
            "traces": [asdict(trace) for trace in self.traces],
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


# Global token tracker instance
token_tracker = TokenTracker()
