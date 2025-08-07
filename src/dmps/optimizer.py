"""
Main orchestrator for prompt optimization.
"""

from typing import Tuple
from .schema import OptimizedResult, ValidationResult
from .engine import OptimizationEngine
from .validation import InputValidator
from .formatters import ConversationalFormatter, StructuredFormatter


class PromptOptimizer:
    """Main orchestrator for prompt optimization"""
    
    def __init__(self):
        self.engine = OptimizationEngine()
        self.validator = InputValidator()
        self.conv_formatter = ConversationalFormatter()
        self.struct_formatter = StructuredFormatter()
    
    def optimize(self, prompt_input: str, mode: str = "conversational", platform: str = "claude") -> Tuple[OptimizedResult, ValidationResult]:
        """Main optimization entry point"""
        # Validate input
        validation = self.validator.validate_input(prompt_input, mode)
        if not validation.is_valid:
            return self._create_error_result(validation.errors, mode), validation
        
        try:
            # Extract intent and create optimization request
            request = self.engine.extract_intent(validation.sanitized_input)
            request.platform = platform
            
            # Apply optimization techniques
            optimization_data = self.engine.apply_optimization(request)
            
            # Assemble optimized prompt
            optimized_prompt = self.engine.assemble_prompt(optimization_data, request)
            
            # Format output based on mode
            if mode == "structured":
                result = self.struct_formatter.format(optimization_data, request, optimized_prompt)
            else:
                result = self.conv_formatter.format(optimization_data, request, optimized_prompt)
            
            return result, validation
        
        except Exception as e:
            return self._create_fallback_result(validation.sanitized_input, str(e), mode), ValidationResult(
                is_valid=False,
                errors=[f"Optimization failed: {str(e)}"],
                warnings=["Using emergency fallback"],
                sanitized_input=validation.sanitized_input
            )
    
    def _create_error_result(self, errors: list, mode: str) -> OptimizedResult:
        """Create error result for validation failures"""
        error_message = "Optimization failed due to input validation errors:\n" + "\n".join(f"• {error}" for error in errors)
        
        if mode == "structured":
            import json
            error_prompt = json.dumps({
                "error": True,
                "message": error_message,
                "errors": errors
            }, indent=2)
        else:
            error_prompt = f"**Error:**\n{error_message}"
        
        return OptimizedResult(
            optimized_prompt=error_prompt,
            improvements=[],
            methodology_applied="Error Handling",
            metadata={"error": True, "error_count": len(errors)},
            format_type=mode
        )
    
    def _create_fallback_result(self, input_text: str, error: str, mode: str) -> OptimizedResult:
        """Create fallback result for processing failures"""
        fallback_message = f"Processing failed, but here's your original input with basic formatting:\n\n{input_text}\n\nError details: {error}"
        
        if mode == "structured":
            import json
            fallback_prompt = json.dumps({
                "status": "fallback",
                "original_prompt": input_text,
                "optimized_prompt": input_text,
                "error": error,
                "message": "Optimization failed, returning original input"
            }, indent=2)
        else:
            fallback_prompt = f"**Fallback Result:**\n{fallback_message}"
        
        return OptimizedResult(
            optimized_prompt=fallback_prompt,
            improvements=["Emergency fallback applied"],
            methodology_applied="Fallback Mode",
            metadata={"fallback": True, "error": error},
            format_type=mode
        )
