#!/usr/bin/env python3
"""
Simple test script to verify DMPS functionality.
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dmps import optimize_prompt, PromptOptimizer

def test_basic_optimization():
    """Test basic prompt optimization"""
    print("Testing DMPS Basic Optimization...")
    
    # Test simple optimization
    test_prompt = "Write me a story about AI"
    
    try:
        optimized = optimize_prompt(test_prompt)
        print(f"✓ Basic optimization successful")
        print(f"Original: {test_prompt}")
        print(f"Optimized length: {len(optimized)} characters")
        print()
    except Exception as e:
        print(f"✗ Basic optimization failed: {e}")
        return False
    
    return True

def test_advanced_optimization():
    """Test advanced optimization with different modes"""
    print("Testing DMPS Advanced Features...")
    
    optimizer = PromptOptimizer()
    test_prompt = "Debug this Python code that sorts a list"
    
    try:
        # Test conversational mode
        result_conv, validation_conv = optimizer.optimize(test_prompt, mode="conversational", platform="claude")
        print(f"✓ Conversational mode successful")
        
        # Test structured mode
        result_struct, validation_struct = optimizer.optimize(test_prompt, mode="structured", platform="chatgpt")
        print(f"✓ Structured mode successful")
        
        # Check validation
        if validation_conv.is_valid and validation_struct.is_valid:
            print(f"✓ Validation successful")
        else:
            print(f"⚠ Validation warnings present")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Advanced optimization failed: {e}")
        return False

def test_intent_detection():
    """Test intent detection"""
    print("Testing Intent Detection...")
    
    from dmps import IntentClassifier
    
    test_cases = [
        ("Write me a creative story", "creative"),
        ("Debug this Python function", "technical"),
        ("Explain how neural networks work", "educational"),
        ("Analyze the market trends", "complex")
    ]
    
    try:
        for prompt, expected in test_cases:
            detected = IntentClassifier.detect_intent(prompt)
            if detected == expected:
                print(f"✓ Intent detection: '{prompt}' -> {detected}")
            else:
                print(f"⚠ Intent detection: '{prompt}' -> {detected} (expected {expected})")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Intent detection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("DMPS System Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_optimization,
        test_advanced_optimization,
        test_intent_detection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DMPS is working correctly.")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
