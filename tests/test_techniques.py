"""
Tests for optimization techniques.
"""

import pytest
from dmps.techniques import OptimizationTechniques
from dmps.schema import OptimizationRequest


class TestOptimizationTechniques:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_request = OptimizationRequest(
            raw_input="Write a story",
            intent="creative",
            output_type="text",
            platform="claude",
            constraints=["500 words", "professional tone"],
            missing_info=["audience", "genre"]
        )
    
    def test_role_generation(self):
        """Test role assignment generation"""
        role = OptimizationTechniques.generate_role("creative")
        assert "creative writer" in role.lower()
        assert len(role) > 10
    
    def test_role_generation_all_intents(self):
        """Test role generation for all intent types"""
        intents = ["creative", "technical", "educational", "complex", "general"]
        for intent in intents:
            role = OptimizationTechniques.generate_role(intent)
            assert isinstance(role, str)
            assert len(role) > 0
    
    def test_context_enhancement(self):
        """Test context enhancement for missing info"""
        context = OptimizationTechniques.enhance_context(self.sample_request)
        assert "audience" in context
        assert "genre" in context or "creative" in context
    
    def test_structure_guidance(self):
        """Test structure guidance generation"""
        structure = OptimizationTechniques.build_structure_guidance("creative")
        assert "structure" in structure.lower()
        assert len(structure) > 20
    
    def test_constraint_formatting(self):
        """Test constraint formatting"""
        constraints = ["500 words", "formal tone"]
        formatted = OptimizationTechniques.format_constraints(constraints)
        assert "500 words" in formatted
        assert "formal tone" in formatted
        assert formatted.startswith("Please adhere")
    
    def test_empty_constraints(self):
        """Test handling of empty constraints"""
        formatted = OptimizationTechniques.format_constraints([])
        assert formatted == ""
    
    def test_techniques_for_intent(self):
        """Test getting techniques for specific intent"""
        techniques = OptimizationTechniques.get_techniques_for_intent("creative")
        assert isinstance(techniques, list)
        assert len(techniques) > 0
        assert "role_assignment" in techniques
    
    def test_apply_technique(self):
        """Test applying specific techniques"""
        result = OptimizationTechniques.apply_technique("role_assignment", self.sample_request)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_chain_of_thought_technique(self):
        """Test chain of thought technique"""
        result = OptimizationTechniques.apply_technique("chain_of_thought", self.sample_request)
        assert "step-by-step" in result.lower()
    
    def test_unknown_technique(self):
        """Test handling of unknown technique"""
        result = OptimizationTechniques.apply_technique("unknown_technique", self.sample_request)
        assert result == ""