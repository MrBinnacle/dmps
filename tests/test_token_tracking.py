"""
Tests for token tracking and evaluation systems.
"""

import pytest
import tempfile
from dmps.token_tracker import TokenTracker, TokenMetrics, ContextTrace
from dmps.evaluation import ContextEvaluator, EvaluationResult
from dmps.observability import ObservabilityDashboard
from dmps import optimize_prompt


class TestTokenTracking:
    """Test token tracking functionality"""
    
    def test_token_estimation(self):
        """Test token estimation accuracy"""
        tracker = TokenTracker()
        
        # Test basic estimation
        assert tracker.estimate_tokens("hello world") == 3  # 11 chars / 4 = 2.75 -> 3
        assert tracker.estimate_tokens("") == 1  # Minimum 1 token
        assert tracker.estimate_tokens("a") == 1
        
    def test_cost_calculation(self):
        """Test cost calculation for different platforms"""
        tracker = TokenTracker()
        
        # Test Claude costs
        cost = tracker.calculate_cost(1000, 500, "claude")
        expected = (1000 * 0.008 + 500 * 0.024) / 1000
        assert abs(cost - expected) < 0.001
        
        # Test unknown platform defaults to ChatGPT
        cost_unknown = tracker.calculate_cost(1000, 500, "unknown")
        cost_chatgpt = tracker.calculate_cost(1000, 500, "chatgpt")
        assert cost_unknown == cost_chatgpt
    
    def test_trace_lifecycle(self):
        """Test complete trace lifecycle"""
        tracker = TokenTracker()
        
        # Start trace
        trace_context = tracker.start_trace("test-001", "Write a story")
        assert trace_context["operation_id"] == "test-001"
        assert trace_context["original_prompt"] == "Write a story"
        assert "start_time" in trace_context
        
        # Complete trace
        optimized = "Please write a detailed story about artificial intelligence"
        techniques = ["develop_clarity", "design_structure"]
        
        trace = tracker.complete_trace(trace_context, optimized, techniques, "claude")
        
        assert isinstance(trace, ContextTrace)
        assert trace.operation_id == "test-001"
        assert trace.optimized_prompt == optimized
        assert trace.techniques_applied == techniques
        assert trace.token_reduction != 0  # Should have some change
        assert 0 <= trace.quality_score <= 1
    
    def test_session_summary(self):
        """Test session summary generation"""
        tracker = TokenTracker()
        
        # Empty session
        summary = tracker.get_session_summary()
        assert summary["total_operations"] == 0
        
        # Add some traces
        for i in range(3):
            trace_context = tracker.start_trace(f"test-{i}", f"prompt {i}")
            tracker.complete_trace(trace_context, f"optimized {i}", ["technique"], "claude")
        
        summary = tracker.get_session_summary()
        assert summary["total_operations"] == 3
        assert "total_token_reduction" in summary
        assert "average_quality_score" in summary


class TestEvaluation:
    """Test evaluation framework"""
    
    def test_clarity_evaluation(self):
        """Test clarity scoring"""
        evaluator = ContextEvaluator()
        
        # Improvement case
        original = "Write something about stuff"
        optimized = "Write a detailed technical article about machine learning"
        score = evaluator.evaluate_clarity(original, optimized)
        assert score > 0.5  # Should improve
        
        # No vague terms case
        original = "Write a detailed article"
        optimized = "Write a comprehensive detailed article"
        score = evaluator.evaluate_clarity(original, optimized)
        assert score == 1.0
    
    def test_specificity_evaluation(self):
        """Test specificity scoring"""
        evaluator = ContextEvaluator()
        
        original = "Tell me about AI"
        optimized = "Please provide specific examples of AI applications with detailed context"
        score = evaluator.evaluate_specificity(original, optimized)
        assert score > 0.5  # Should be more specific
    
    def test_efficiency_evaluation(self):
        """Test token efficiency scoring"""
        evaluator = ContextEvaluator()
        
        # Good efficiency: reduced tokens with quality maintained
        score = evaluator.evaluate_efficiency(100, 80, True)
        assert score > 0.7
        
        # Poor efficiency: increased tokens
        score = evaluator.evaluate_efficiency(100, 150, True)
        assert score < 0.7
        
        # Quality loss penalty
        score = evaluator.evaluate_efficiency(100, 80, False)
        assert score < 0.5
    
    def test_degradation_detection(self):
        """Test quality degradation detection"""
        evaluator = ContextEvaluator()
        
        # Set baseline
        evaluator.baseline_scores = {"clarity": 0.8, "specificity": 0.7}
        
        # No degradation
        current_scores = {"clarity": 0.8, "specificity": 0.75}
        assert not evaluator.detect_degradation(current_scores)
        
        # Degradation detected
        current_scores = {"clarity": 0.5, "specificity": 0.4}  # Below threshold
        assert evaluator.detect_degradation(current_scores)
    
    def test_complete_evaluation(self):
        """Test complete evaluation process"""
        evaluator = ContextEvaluator()
        
        original = "Write something about AI stuff"
        optimized = "Please write a detailed technical article about artificial intelligence applications"
        
        result = evaluator.evaluate(original, optimized, 25, 60)
        
        assert isinstance(result, EvaluationResult)
        assert 0 <= result.overall_score <= 1
        assert "clarity" in result.metric_scores
        assert "specificity" in result.metric_scores
        assert "completeness" in result.metric_scores
        assert 0 <= result.token_efficiency <= 1
        assert isinstance(result.degradation_detected, bool)
        assert isinstance(result.recommendations, list)


class TestObservability:
    """Test observability dashboard"""
    
    def test_dashboard_with_no_data(self):
        """Test dashboard with no tracking data"""
        dashboard = ObservabilityDashboard()
        
        # Should not crash with no data
        dashboard.print_session_summary()
        dashboard.print_detailed_metrics()
        
        alerts = dashboard.get_performance_alerts()
        assert isinstance(alerts, list)
    
    def test_metrics_export(self):
        """Test metrics export functionality"""
        dashboard = ObservabilityDashboard()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            dashboard.export_metrics(f.name)
            # Should create file without errors


class TestIntegration:
    """Test integration with main optimizer"""
    
    def test_optimization_with_tracking(self):
        """Test that optimization includes tracking data"""
        result = optimize_prompt("Write a story about AI", "conversational", "claude")
        
        # Should be a string (the optimized prompt)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_optimizer_metadata(self):
        """Test that optimizer includes tracking metadata"""
        from dmps import PromptOptimizer
        
        optimizer = PromptOptimizer()
        result, validation = optimizer.optimize("Write a story", "conversational", "claude")
        
        # Check for tracking metadata
        assert "token_metrics" in result.metadata
        assert "evaluation" in result.metadata
        assert "operation_id" in result.metadata
        
        # Check token metrics structure
        token_metrics = result.metadata["token_metrics"]
        assert "original_tokens" in token_metrics
        assert "optimized_tokens" in token_metrics
        assert "token_reduction" in token_metrics
        assert "cost_estimate" in token_metrics
        
        # Check evaluation structure
        evaluation = result.metadata["evaluation"]
        assert "overall_score" in evaluation
        assert "token_efficiency" in evaluation
        assert "degradation_detected" in evaluation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])