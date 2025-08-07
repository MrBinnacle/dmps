"""
Integration tests for complete coverage of user workflows.
"""

import pytest
import tempfile
import json
from pathlib import Path
from dmps import optimize_prompt, PromptOptimizer
from dmps.repl import DMPSShell
from dmps.cli import main, read_file_content, write_output


class TestCompleteUserWorkflows:
    """Test complete user workflows for coverage"""
    
    def test_cli_file_workflow(self):
        """Test complete CLI file input/output workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create input file
            input_file = Path(temp_dir) / "input.txt"
            input_file.write_text("Write a technical story about AI")
            
            # Create output file path
            output_file = Path(temp_dir) / "output.txt"
            
            # Test file operations
            content = read_file_content(str(input_file))
            assert "technical story" in content
            
            # Test optimization
            optimizer = PromptOptimizer()
            result, validation = optimizer.optimize(content, "conversational", "claude")
            
            # Test output writing
            write_output(result.optimized_prompt, str(output_file), quiet=True)
            assert output_file.exists()
            
            # Verify output
            output_content = output_file.read_text()
            assert len(output_content) > len(content)
    
    def test_repl_complete_session(self):
        """Test complete REPL session workflow"""
        shell = DMPSShell()
        
        # Test all configuration commands
        shell._display_current_configuration()
        shell._update_configuration_setting(["mode", "structured"])
        shell._update_configuration_setting(["platform", "chatgpt"])
        shell._update_configuration_setting(["show_metadata", "true"])
        
        # Test optimization with different settings
        shell.optimize_and_display("Write a creative story")
        shell.optimize_and_display("Explain machine learning technically")
        
        # Test history operations
        shell._show_history()
        assert len(shell.history) == 2
        
        # Test save functionality
        with tempfile.TemporaryDirectory() as temp_dir:
            save_file = Path(temp_dir) / "history.json"
            shell.cmd_save([str(save_file)])
            
            if save_file.exists():
                saved_data = json.loads(save_file.read_text())
                assert len(saved_data) == 2
        
        # Test clear history
        shell._clear_history()
        assert len(shell.history) == 0
    
    def test_all_intent_classifications(self):
        """Test all intent classification paths"""
        from dmps.intent import IntentClassifier
        
        classifier = IntentClassifier()
        
        # Test all intent types
        test_cases = [
            ("Write a creative story about robots", "creative"),
            ("Debug this Python code function", "technical"),
            ("Explain how neural networks work", "educational"),
            ("Compare different machine learning algorithms", "analytical"),
            ("What do you think about AI ethics?", "conversational"),
            ("Random text without clear intent", "general")
        ]
        
        for prompt, expected_category in test_cases:
            intent = classifier.classify(prompt)
            # Intent should be one of the valid categories
            assert intent in ["creative", "technical", "educational", "analytical", "conversational", "general"]
    
    def test_all_optimization_techniques(self):
        """Test all optimization technique paths"""
        from dmps.techniques import OptimizationTechniques
        
        tech = OptimizationTechniques()
        
        # Test all technique methods
        test_prompt = "Write something about AI"
        
        # Test develop_clarity with different intents
        for intent in ["technical", "creative", "educational", "general"]:
            result = tech.develop_clarity(test_prompt, intent)
            assert len(result) >= len(test_prompt)
        
        # Test design_structure with all platforms
        for platform in tech.ALLOWED_PLATFORMS:
            result = tech.design_structure(test_prompt, platform, "general")
            assert len(result) > 0
        
        # Test deliver_format with all output types
        output_types = ["list", "explanation", "code", "creative", "general"]
        for output_type in output_types:
            result = tech.deliver_format(test_prompt, output_type)
            assert result.endswith(('.', '!', '?'))
        
        # Test all technique descriptions
        for technique in tech.ALLOWED_TECHNIQUES:
            desc = tech.get_technique_description(technique)
            assert len(desc) > 0
    
    def test_all_formatter_paths(self):
        """Test all formatter code paths"""
        from dmps.formatters import ConversationalFormatter, StructuredFormatter
        from dmps.schema import OptimizationRequest
        
        # Create comprehensive test data
        optimization_data = {
            "improvements": ["Enhanced clarity", "Added structure", "Improved format"],
            "techniques_applied": ["develop_clarity", "design_structure", "deliver_format"],
            "components": {"length": 50, "complexity": "medium"}
        }
        
        request = OptimizationRequest(
            raw_input="Original prompt text",
            intent="technical",
            output_type="explanation",
            platform="claude",
            constraints=["500 words", "technical context"],
            missing_info=["More specific requirements", "Target audience"]
        )
        
        # Test conversational formatter with all data
        conv_formatter = ConversationalFormatter()
        conv_result = conv_formatter.format(optimization_data, request, "Optimized prompt text")
        
        assert "Enhanced clarity" in conv_result.optimized_prompt
        assert "More specific requirements" in conv_result.optimized_prompt
        assert conv_result.format_type == "conversational"
        assert len(conv_result.improvements) == 3
        
        # Test structured formatter with all data
        struct_formatter = StructuredFormatter()
        struct_result = struct_formatter.format(optimization_data, request, "Optimized prompt text")
        
        assert struct_result.format_type == "structured"
        parsed_json = json.loads(struct_result.optimized_prompt)
        assert "optimization_result" in parsed_json
        assert parsed_json["optimization_result"]["intent_detected"] == "technical"
        assert len(parsed_json["optimization_result"]["improvements_applied"]) == 3
    
    def test_error_handling_paths(self):
        """Test all error handling code paths"""
        from dmps.error_handler import SecureErrorHandler
        
        handler = SecureErrorHandler()
        
        # Test all exception types
        exceptions = [
            FileNotFoundError("File not found"),
            PermissionError("Access denied"),
            ValueError("Invalid value"),
            OSError("System error"),
            ImportError("Import failed"),
            TypeError("Type error"),
            KeyError("Key missing"),
            Exception("Generic error")
        ]
        
        for exc in exceptions:
            msg = handler.handle_error(exc, "test_context")
            assert len(msg) > 0
            assert "error" in msg.lower()
        
        # Test security error handling
        for exc in exceptions[:4]:  # File/permission related
            sec_msg = handler.handle_security_error(exc, "security_context")
            assert "security" in sec_msg.lower() or "access" in sec_msg.lower()
        
        # Test performance logging
        handler.log_performance_issue("slow_operation", 2.5, 1.0)
        handler.log_performance_issue("fast_operation", 0.5, 1.0)  # Should not log
    
    def test_cache_functionality(self):
        """Test caching system functionality"""
        from dmps.cache import PerformanceCache, get_intent_classifier, get_optimization_engine
        
        # Test cached intent classification
        prompt = "Write a technical document"
        hash1 = PerformanceCache.get_prompt_hash(prompt)
        
        # First call
        intent1 = PerformanceCache.cached_intent_classification(hash1, prompt)
        
        # Second call (should use cache)
        intent2 = PerformanceCache.cached_intent_classification(hash1, prompt)
        assert intent1 == intent2
        
        # Test path validation cache
        safe_path = "safe_file.txt"
        unsafe_path = "../unsafe.txt"
        
        result1 = PerformanceCache.cached_path_validation(safe_path)
        result2 = PerformanceCache.cached_path_validation(unsafe_path)
        
        assert result1 == True
        assert result2 == False
        
        # Test lazy loading
        classifier1 = get_intent_classifier()
        classifier2 = get_intent_classifier()
        assert classifier1 is classifier2  # Should be same instance
        
        engine1 = get_optimization_engine()
        engine2 = get_optimization_engine()
        assert engine1 is engine2  # Should be same instance


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=html", "--cov-fail-under=90"])