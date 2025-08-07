#!/usr/bin/env python3
"""
Advanced DMPS Usage Examples

This script demonstrates advanced features and use cases for DMPS.
"""

import json
from dmps import PromptOptimizer
from dmps.intent import IntentClassifier, GapAnalyzer
from dmps.techniques import OptimizationTechniques


def example_1_batch_processing():
    """Example 1: Batch processing multiple prompts"""
    print("=" * 60)
    print("EXAMPLE 1: Batch Processing")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    
    prompts = [
        "Write documentation for an API",
        "Create a marketing campaign",
        "Solve this math problem step by step",
        "Generate test cases for software"
    ]
    
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"Processing prompt {i}/{len(prompts)}: {prompt[:30]}...")
        result, validation = optimizer.optimize(prompt, mode="structured")
        
        if validation.is_valid:
            # Parse structured result for analysis
            data = json.loads(result.optimized_prompt)
            results.append({
                "original": prompt,
                "intent": data["analysis"]["intent"],
                "improvements": data["optimization"]["improvements_made"],
                "confidence": data["metadata"]["confidence_score"]
            })
    
    print(f"\nBatch Results Summary:")
    print(f"Total prompts processed: {len(results)}")
    avg_improvements = sum(r["improvements"] for r in results) / len(results)
    avg_confidence = sum(r["confidence"] for r in results) / len(results)
    print(f"Average improvements per prompt: {avg_improvements:.1f}")
    print(f"Average confidence score: {avg_confidence:.2f}")


def example_2_custom_analysis():
    """Example 2: Using individual components for custom analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Analysis Pipeline")
    print("=" * 60)
    
    test_prompt = "Create a machine learning model to predict customer behavior"
    
    # Step 1: Intent detection
    intent = IntentClassifier.detect_intent(test_prompt)
    print(f"Detected Intent: {intent}")
    
    # Step 2: Gap analysis
    gaps = GapAnalyzer.identify_gaps(test_prompt, intent)
    print(f"Identified Gaps: {gaps}")
    
    # Step 3: Get applicable techniques
    techniques = OptimizationTechniques.get_techniques_for_intent(intent)
    print(f"Applicable Techniques: {techniques}")
    
    # Step 4: Generate role
    role = OptimizationTechniques.generate_role(intent)
    print(f"Generated Role: {role[:50]}...")


def example_3_error_handling():
    """Example 3: Robust error handling and validation"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Error Handling and Validation")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    
    # Test various problematic inputs
    test_cases = [
        "",  # Empty input
        "Hi",  # Too short
        "x" * 15000,  # Too long
        "<script>alert('test')</script>Normal prompt",  # Suspicious content
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_input[:30]}{'...' if len(test_input) > 30 else ''}")
        
        try:
            result, validation = optimizer.optimize(test_input)
            
            if validation.is_valid:
                print("✓ Validation passed")
                print(f"  Optimized length: {len(result.optimized_prompt)} chars")
            else:
                print("✗ Validation failed")
                print(f"  Errors: {validation.errors}")
            
            if validation.warnings:
                print(f"  Warnings: {validation.warnings}")
                
        except Exception as e:
            print(f"✗ Exception occurred: {e}")


def example_4_performance_analysis():
    """Example 4: Performance analysis and optimization metrics"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Performance Analysis")
    print("=" * 60)
    
    import time
    
    optimizer = PromptOptimizer()
    
    # Test prompts of different complexities
    test_prompts = [
        "Simple prompt",
        "Write a comprehensive technical documentation for a REST API that handles user authentication, data validation, and error handling",
        "Create a detailed marketing strategy for a B2B SaaS product targeting enterprise customers in the healthcare industry with specific focus on compliance requirements"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: {len(prompt)} characters")
        
        start_time = time.time()
        result, validation = optimizer.optimize(prompt, mode="structured")
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        if validation.is_valid:
            data = json.loads(result.optimized_prompt)
            optimization_ratio = data["metadata"]["optimization_ratio"]
            improvements = data["optimization"]["improvements_made"]
            
            print(f"  Processing time: {processing_time:.3f}s")
            print(f"  Optimization ratio: {optimization_ratio:.2f}x")
            print(f"  Improvements applied: {improvements}")
        else:
            print(f"  Failed validation: {validation.errors}")


def example_5_integration_patterns():
    """Example 5: Common integration patterns"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Integration Patterns")
    print("=" * 60)
    
    # Pattern 1: API-style usage
    def optimize_for_api(prompt_text, user_preferences=None):
        """Simulate API endpoint usage"""
        optimizer = PromptOptimizer()
        
        # Use user preferences or defaults
        mode = user_preferences.get("mode", "conversational") if user_preferences else "conversational"
        platform = user_preferences.get("platform", "claude") if user_preferences else "claude"
        
        result, validation = optimizer.optimize(prompt_text, mode=mode, platform=platform)
        
        return {
            "success": validation.is_valid,
            "optimized_prompt": result.optimized_prompt if validation.is_valid else None,
            "errors": validation.errors if not validation.is_valid else None,
            "metadata": result.metadata if validation.is_valid else None
        }
    
    # Test API pattern
    api_result = optimize_for_api("Explain blockchain", {"mode": "structured", "platform": "chatgpt"})
    print("API Pattern Result:")
    print(f"  Success: {api_result['success']}")
    if api_result['success']:
        print(f"  Metadata keys: {list(api_result['metadata'].keys())}")
    
    # Pattern 2: Streaming/callback usage
    def optimize_with_callback(prompt_text, progress_callback=None):
        """Simulate streaming optimization with progress callbacks"""
        if progress_callback:
            progress_callback("Starting optimization...")
        
        optimizer = PromptOptimizer()
        
        if progress_callback:
            progress_callback("Analyzing intent...")
        
        result, validation = optimizer.optimize(prompt_text)
        
        if progress_callback:
            progress_callback("Optimization complete!")
        
        return result, validation
    
    # Test callback pattern
    def progress_printer(message):
        print(f"  Progress: {message}")
    
    print(f"\nCallback Pattern:")
    callback_result, _ = optimize_with_callback("Write unit tests", progress_printer)


def main():
    """Run all advanced examples"""
    print("DMPS Advanced Usage Examples")
    print("This script demonstrates advanced DMPS features and patterns\n")
    
    try:
        example_1_batch_processing()
        example_2_custom_analysis()
        example_3_error_handling()
        example_4_performance_analysis()
        example_5_integration_patterns()
        
        print("\n" + "=" * 60)
        print("All advanced examples completed!")
        print("These patterns can be adapted for your specific use cases.")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()