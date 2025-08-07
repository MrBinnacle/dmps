"""
Validation tests to ensure refactoring doesn't break functionality.
"""

import pytest
from dmps import optimize_prompt, PromptOptimizer
from dmps.engine import OptimizationEngine
from dmps.repl import DMPSShell
from dmps.formatters import ConversationalFormatter, StructuredFormatter


class TestRefactoringValidation:
    """Validate that refactoring maintains functionality"""
    
    def test_convenience_function_works(self):
        """Test that optimize_prompt convenience function still works"""
        result = optimize_prompt("Write a story about AI", "conversational", "claude")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_engine_refactored_methods_work(self):
        """Test that refactored engine methods maintain functionality"""
        engine = OptimizationEngine()
        
        # Test renamed method
        output_format = engine._determine_expected_output_format("Create a list of items")
        assert output_format in ["list", "explanation", "code", "creative", "general"]
        
        # Test constraint extraction
        constraints = engine._extract_user_constraints("Write 500 words about AI")
        assert isinstance(constraints, list)
    
    def test_repl_refactored_methods_work(self):
        """Test that refactored REPL methods maintain functionality"""
        shell = DMPSShell()
        
        # Test configuration display (renamed method)
        shell._display_current_configuration()
        
        # Test setting update (renamed method)
        shell._update_configuration_setting(["mode", "structured"])
        assert shell.settings["mode"] == "structured"
    
    def test_formatters_performance_optimization(self):
        """Test that formatter optimizations don't break functionality"""
        from dmps.schema import OptimizationRequest
        
        # Mock data
        optimization_data = {
            "improvements": ["Enhanced clarity", "Added structure"],
            "techniques_applied": ["develop_clarity", "design_structure"]
        }
        
        request = OptimizationRequest(
            raw_input="Test prompt",
            intent="general",
            output_type="general",
            platform="claude",
            constraints=[],
            missing_info=["More context needed"]
        )
        
        # Test conversational formatter
        conv_formatter = ConversationalFormatter()
        conv_result = conv_formatter.format(optimization_data, request, "Optimized test prompt")
        assert conv_result.format_type == "conversational"
        assert "Enhanced clarity" in conv_result.optimized_prompt
        
        # Test structured formatter
        struct_formatter = StructuredFormatter()
        struct_result = struct_formatter.format(optimization_data, request, "Optimized test prompt")
        assert struct_result.format_type == "structured"
        assert "optimization_result" in struct_result.optimized_prompt
    
    def test_naming_conventions_followed(self):
        """Test that naming conventions are properly followed"""
        # Test that key functions use descriptive names
        optimizer = PromptOptimizer()
        
        # Should have descriptive method names
        assert hasattr(optimizer, 'optimize')
        
        # Engine should have refactored method names
        engine = OptimizationEngine()
        assert hasattr(engine, '_determine_expected_output_format')
        assert hasattr(engine, '_extract_user_constraints')
        
        # REPL should have clear method names
        shell = DMPSShell()
        assert hasattr(shell, '_display_current_configuration')
        assert hasattr(shell, '_update_configuration_setting')
    
    def test_performance_monitoring_integration(self):
        """Test that performance monitoring doesn't break functionality"""
        from dmps.intent import IntentClassifier
        
        classifier = IntentClassifier()
        intent = classifier.classify("Write a technical document about AI")
        assert intent in ["creative", "technical", "educational", "analytical", "conversational", "general"]


if __name__ == "__main__":
    pytest.main([__file__])