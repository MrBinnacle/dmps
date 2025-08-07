"""
Evaluation framework for context engineering effectiveness.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Final, List


class QualityMetric(Enum):
    CLARITY = "clarity"
    SPECIFICITY = "specificity"
    COMPLETENESS = "completeness"
    EFFICIENCY = "efficiency"


@dataclass
class EvaluationResult:
    """Result of context engineering evaluation"""

    overall_score: float
    metric_scores: Dict[str, float]
    token_efficiency: float
    degradation_detected: bool
    recommendations: List[str]


class ContextEvaluator:
    """Evaluates context engineering effectiveness"""

    # Quality thresholds
    DEGRADATION_THRESHOLD: Final = 0.7
    EFFICIENCY_THRESHOLD: Final = 0.8

    def __init__(self):
        self.baseline_scores: Dict[str, float] = {}
        self.evaluation_history: List[EvaluationResult] = []

    def evaluate_clarity(self, original: str, optimized: str) -> float:
        """Evaluate clarity improvement (0-1 score)"""
        # Simple heuristics for clarity
        vague_terms = ["something", "anything", "stuff", "things"]

        original_vague = sum(1 for term in vague_terms if term in original.lower())
        optimized_vague = sum(1 for term in vague_terms if term in optimized.lower())

        # Clarity improves when vague terms are reduced
        if original_vague == 0:
            return 1.0

        improvement = max(0, (original_vague - optimized_vague) / original_vague)
        return min(1.0, 0.5 + improvement * 0.5)

    def evaluate_specificity(self, original: str, optimized: str) -> float:
        """Evaluate specificity improvement (0-1 score)"""
        # Count specific indicators
        specific_indicators = ["please", "specific", "detailed", "example", "context"]

        # Count specific indicators in original (for reference)
        sum(1 for term in specific_indicators if term in original.lower())
        optimized_specific = sum(
            1 for term in specific_indicators if term in optimized.lower()
        )

        # Specificity improves when specific terms are added
        if len(original.split()) == 0:
            return 0.5

        specificity_ratio = optimized_specific / max(1, len(optimized.split()) / 10)
        return min(1.0, specificity_ratio)

    def evaluate_completeness(self, original: str, optimized: str) -> float:
        """Evaluate completeness (0-1 score)"""
        # Completeness based on information preservation and enhancement
        original_words = set(original.lower().split())
        optimized_words = set(optimized.lower().split())

        # Check information preservation
        preserved_ratio = len(original_words & optimized_words) / max(
            1, len(original_words)
        )

        # Check information enhancement
        enhancement_ratio = len(optimized_words - original_words) / max(
            1, len(original_words)
        )

        return min(1.0, preserved_ratio * 0.7 + min(enhancement_ratio, 0.5) * 0.3)

    def evaluate_efficiency(
        self, original_tokens: int, optimized_tokens: int, quality_maintained: bool
    ) -> float:
        """Evaluate token efficiency (0-1 score)"""
        if original_tokens == 0:
            return 1.0

        # Efficiency is good when tokens are reduced while maintaining quality
        token_ratio = optimized_tokens / original_tokens

        if not quality_maintained:
            return max(0.0, 0.5 - token_ratio * 0.5)  # Penalize quality loss

        # Reward token reduction with quality maintenance
        if token_ratio <= 1.0:
            return min(1.0, 1.0 - token_ratio * 0.3)
        else:
            return max(0.0, 1.0 - (token_ratio - 1.0) * 0.5)  # Penalize token increase

    def detect_degradation(self, current_scores: Dict[str, float]) -> bool:
        """Detect if context engineering caused quality degradation"""
        if not self.baseline_scores:
            return False

        # Check if any metric dropped significantly
        for metric, current_score in current_scores.items():
            baseline = self.baseline_scores.get(metric, 0.5)
            if current_score < baseline * self.DEGRADATION_THRESHOLD:
                return True

        return False

    def generate_recommendations(
        self, scores: Dict[str, float], token_efficiency: float
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []

        if scores.get("clarity", 1.0) < 0.7:
            recommendations.append("Reduce vague terms and add specific context")

        if scores.get("specificity", 1.0) < 0.7:
            recommendations.append("Add more specific instructions and examples")

        if scores.get("completeness", 1.0) < 0.7:
            recommendations.append("Ensure all original information is preserved")

        if token_efficiency < self.EFFICIENCY_THRESHOLD:
            recommendations.append("Optimize for better token efficiency")

        if not recommendations:
            recommendations.append("Context engineering is performing well")

        return recommendations

    def evaluate(
        self,
        original_prompt: str,
        optimized_prompt: str,
        original_tokens: int,
        optimized_tokens: int,
    ) -> EvaluationResult:
        """Comprehensive evaluation of context engineering"""

        # Calculate individual metrics
        clarity_score = self.evaluate_clarity(original_prompt, optimized_prompt)
        specificity_score = self.evaluate_specificity(original_prompt, optimized_prompt)
        completeness_score = self.evaluate_completeness(
            original_prompt, optimized_prompt
        )

        metric_scores = {
            "clarity": clarity_score,
            "specificity": specificity_score,
            "completeness": completeness_score,
        }

        # Calculate overall quality score
        overall_score = sum(metric_scores.values()) / len(metric_scores)

        # Calculate token efficiency
        quality_maintained = overall_score >= 0.7
        efficiency_score = self.evaluate_efficiency(
            original_tokens, optimized_tokens, quality_maintained
        )

        # Detect degradation
        degradation = self.detect_degradation(metric_scores)

        # Generate recommendations
        recommendations = self.generate_recommendations(metric_scores, efficiency_score)

        result = EvaluationResult(
            overall_score=round(overall_score, 3),
            metric_scores={k: round(v, 3) for k, v in metric_scores.items()},
            token_efficiency=round(efficiency_score, 3),
            degradation_detected=degradation,
            recommendations=recommendations,
        )

        # Update baseline if this is better
        if overall_score > sum(self.baseline_scores.values()) / max(
            1, len(self.baseline_scores)
        ):
            self.baseline_scores = metric_scores.copy()

        self.evaluation_history.append(result)
        return result

    def get_performance_trend(self) -> Dict:
        """Get performance trend over time"""
        if len(self.evaluation_history) < 2:
            return {"trend": "insufficient_data"}

        recent_scores = [r.overall_score for r in self.evaluation_history[-5:]]
        older_scores = [r.overall_score for r in self.evaluation_history[-10:-5]] or [
            0.5
        ]

        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)

        trend = (
            "improving"
            if recent_avg > older_avg
            else "declining"
            if recent_avg < older_avg
            else "stable"
        )

        return {
            "trend": trend,
            "recent_average": round(recent_avg, 3),
            "change": round(recent_avg - older_avg, 3),
            "total_evaluations": len(self.evaluation_history),
        }


# Global evaluator instance
context_evaluator = ContextEvaluator()
