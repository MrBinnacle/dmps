#!/usr/bin/env python3
"""
Basic DMPS Usage Examples

This script demonstrates the fundamental ways to use DMPS for prompt optimization.
"""

from dmps import optimize_prompt, PromptOptimizer


def example_1_quick_optimization():
    """Example 1: Quick optimization using the convenience function"""
    print("=" * 60)
    print("EXAMPLE 1: Quick Optimization")
    print("=" * 60)
    
    # Simple one-liner optimization
    original = "Write a story about AI"
    optimized = optimize_prompt(original)
    
    print(f"Original: {original}")
    print(f"\nOptimized:\n{optimized}")


def example_2_basic_optimizer():
    """Example 2: Using the PromptOptimizer class"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Basic PromptOptimizer Usage")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    
    # Optimize with default settings
    result, validation = optimizer.optimize("Explain machine learning")
    
    print("Validation Status:", "✓ Valid" if validation.is_valid else "✗ Invalid")
    if validation.warnings:
        print("Warnings:", validation.warnings)
    
    print(f"\nResult:\n{result.optimized_prompt}")
    print(f"\nImprovements Applied: {len(result.improvements)}")


def example_3_different_modes():
    """Example 3: Comparing conversational vs structured modes"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Different Output Modes")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    prompt = "Debug this Python function"
    
    # Conversational mode
    conv_result, _ = optimizer.optimize(prompt, mode="conversational")
    print("CONVERSATIONAL MODE:")
    print(conv_result.optimized_prompt[:200] + "...")
    
    print("\n" + "-" * 40)
    
    # Structured mode
    struct_result, _ = optimizer.optimize(prompt, mode="structured")
    print("STRUCTURED MODE:")
    print(struct_result.optimized_prompt[:200] + "...")


def example_4_platform_targeting():
    """Example 4: Platform-specific optimization"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Platform-Specific Optimization")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    prompt = "Create a REST API"
    
    platforms = ["claude", "chatgpt"]
    
    for platform in platforms:
        result, _ = optimizer.optimize(prompt, platform=platform)
        print(f"\n{platform.upper()} optimization:")
        print(result.optimized_prompt[:150] + "...")


def example_5_intent_detection():
    """Example 5: Demonstrating intent detection"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Intent Detection Examples")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    
    test_prompts = [
        "Write a poem about nature",
        "Debug this sorting algorithm",
        "Explain quantum physics to a child",
        "Analyze market trends and competition"
    ]
    
    for prompt in test_prompts:
        result, _ = optimizer.optimize(prompt, mode="conversational")
        intent = result.metadata.get("intent", "unknown")
        print(f"Prompt: '{prompt}'")
        print(f"Detected Intent: {intent.title()}")
        print(f"Techniques Applied: {len(result.improvements)}")
        print("-" * 40)


def main():
    """Run all examples"""
    print("DMPS Basic Usage Examples")
    print("This script demonstrates core DMPS functionality\n")
    
    try:
        example_1_quick_optimization()
        example_2_basic_optimizer()
        example_3_different_modes()
        example_4_platform_targeting()
        example_5_intent_detection()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("Try running: python -m dmps --help for CLI usage")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure DMPS is properly installed: pip install -e .")


if __name__ == "__main__":
    main()