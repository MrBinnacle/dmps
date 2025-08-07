"""
Tests for the optimization engine.
"""

import pytest
from dmps.engine import OptimizationEngine
from dmps.schema import OptimizationRequest


class TestOptimizationEngine:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = OptimizationEngine()
    
    def test_extract_intent(self):
        """Test intent extraction"""
        request = self.engine.extract_intent("Write a creative story about robots")
        
        assert isinstance(request, OptimizationRequest)
        assert request.intent == "creative"
        assert request.raw_input == "Write a creative story about robots"
    
    def test_constraint_extraction(self):
        """Test constraint extraction from text"""
        constraints = self.engine._extract_constraints("Write a 500 word formal essay")
        
        assert len(constraints) > 0
        assert any("500" in constraint for constraint in constraints)
        assert any("formal" in constraint.lower() for constraint in constraints)
    
    def test_output_type_inference(self):
        """Test output type inference"""
        list_type = self.engine._infer_output_type("Give me a list of items", "general")
        assert list_type == "list"
        
        json_type = self.engine._infer_output_type("Return JSON data", "technical")
        assert json_type == "structured"
        
        narrative_type = self.engine._infer_output_type("Tell a story", "creative")
        assert narrative_type == "narrative"
    
    def test_apply_optimization(self):
        """Test optimization application"""
        request = OptimizationRequest(
            raw_input="Debug code",
            intent="technical",
            output_type="code",
            platform="claude",
            constraints=[],
            missing_info=["technical_context"]
        )
        
        optimization_data = self.engine.apply_optimization(request)
        
        assert isinstance(optimization_data, dict)
        assert "techniques_applied" in optimization_data
        assert "optimizations" in optimization_data
        assert len(optimization_data["techniques_applied"]) > 0
    
    def test_assemble_prompt(self):
        """Test prompt assembly"""
        request = OptimizationRequest(
            raw_input="Test prompt",
            intent="general",
            output_type="text",
            platform="claude",
            constraints=["brief"],
            missing_info=[]
        )
        
        optimization_data = {
            "techniques_applied": ["role_assignment"],
            "optimizations": {},
            "role": "You are a helpful assistant",
            "structure_guidance": "Be clear and concise",
            "context_enhancements": "",
            "formatted_constraints": "Keep it brief"
        }
        
        assembled = self.engine.assemble_prompt(optimization_data, request)
        
        assert isinstance(assembled, str)
        assert len(assembled) > len(request.raw_input)
        assert "helpful assistant" in assembled
    
    def test_complete_optimization_pipeline(self):
        """Test the complete optimization pipeline"""
        optimized, data, request = self.engine.optimize_prompt("Explain AI to beginners")
        
        assert isinstance(optimized, str)
        assert isinstance(data, dict)
        assert isinstance(request, OptimizationRequest)
        assert len(optimized) > 0
        assert request.intent in ["educational", "general"]