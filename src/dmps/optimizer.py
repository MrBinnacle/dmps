"""
Main orchestrator for prompt optimization.
"""

import json
from typing import Tuple, Literal
from .schema import OptimizedResult, ValidationResult
from .engine import OptimizationEngine
from .validation import InputValidator
from .formatters import ConversationalFormatter, StructuredFormatter


class PromptOptimizer:
    """Main orchestrator for prompt optimization"""
    
    def __init__(self):
        self.engine = OptimizationEngine()
        self.validator = InputValidator()
        self.formatters = {
            "conversational": ConversationalFormatter(),
            "structured": StructuredFormatter()
        }
    
    def optimize(
        self, prompt_input: str, mode: str = "conversational", platform: str = "claude"
    ) -> Tuple[OptimizedResult, ValidationResult]:
        """Main optimization entry point"""
        validation = self.validator.validate_input(prompt_input, mode)
        if not validation.is_valid:
            return self._create_error_result(validation.errors, mode), validation
        
        try:
            sanitized_input = validation.sanitized_input or ""
            request = self.engine.extract_intent(sanitized_input)
            request.platform = platform
            
            optimization_data = self.engine.apply_optimization(request)
            optimized_prompt = self.engine.assemble_prompt(
                optimization_data, request
            )
            
            formatter = self.formatters[mode]
            result = formatter.format(
                optimization_data, request, optimized_prompt
            )
            
            return result, validation
        
        except Exception as e:
            return self._create_fallback_result(
                validation.sanitized_input or "", str(e), mode
            ), ValidationResult(
                is_valid=False,
                errors=[f"Optimization failed: {str(e)}"],
                warnings=["Using emergency fallback"],
                sanitized_input=validation.sanitized_input
            )
    
    def _create_error_result(self, errors: list, mode: str) -> OptimizedResult:
        """Create error result for validation failures"""
        error_message = "Optimization failed:\n" + "\n".join(
            f"• {error}" for error in errors
        )
        
        error_prompt = json.dumps({
            "error": True,
            "message": error_message,
            "errors": errors
        }, indent=2) if mode == "structured" else (
            f"**Error:**\n{error_message}"
        )
        
        format_type: Literal['conversational', 'structured'] = (
            'structured' if mode == 'structured' else 'conversational'
        )
        
        return OptimizedResult(
            optimized_prompt=error_prompt,
            improvements=[],
            methodology_applied="Error Handling",
            metadata={"error": True, "error_count": len(errors)},
            format_type=format_type
        )
    
    def _create_fallback_result(
        self, input_text: str, error: str, mode: str
    ) -> OptimizedResult:
        """Create fallback result for processing failures"""
        fallback_prompt = json.dumps({
            "status": "fallback",
            "original_prompt": input_text,
            "error": error
        }, indent=2) if mode == "structured" else (
            f"**Fallback:**\n{input_text}\n\nError: {error}"
        )
        
        format_type: Literal['conversational', 'structured'] = (
            'structured' if mode == 'structured' else 'conversational'
        )
        
        return OptimizedResult(
            optimized_prompt=fallback_prompt,
            improvements=["Emergency fallback applied"],
            methodology_applied="Fallback Mode",
            metadata={"fallback": True, "error": error},
            format_type=format_type
        )