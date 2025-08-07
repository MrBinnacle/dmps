#!/usr/bin/env python3
"""
DMPS REPL Usage Examples

This script demonstrates how to use the DMPS REPL shell interface.
"""

import subprocess
import sys
import time
from pathlib import Path


def example_1_basic_repl_usage():
    """Example 1: Basic REPL usage demonstration"""
    print("=" * 60)
    print("EXAMPLE 1: Basic REPL Usage")
    print("=" * 60)
    
    print("The DMPS REPL provides an interactive shell for prompt optimization.")
    print("\nTo start the REPL:")
    print("  dmps-shell")
    print("  # or")
    print("  dmps --shell")
    print("  # or")
    print("  python -m dmps.repl")
    
    print("\nBasic REPL commands:")
    commands = [
        "/help - Show all available commands",
        "/settings - Display current settings",
        "/set mode structured - Change output mode",
        "/set platform chatgpt - Change target platform",
        "/history - Show optimization history",
        "/examples - Show example prompts",
        "/stats - Show usage statistics",
        "/quit - Exit the shell"
    ]
    
    for cmd in commands:
        print(f"  {cmd}")


def example_2_repl_session_simulation():
    """Example 2: Simulate a REPL session"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Simulated REPL Session")
    print("=" * 60)
    
    print("Here's what a typical REPL session looks like:")
    print()
    
    # Simulate REPL interaction
    session_commands = [
        ("dmps> Write a story about AI", "Optimizing prompt..."),
        ("dmps> /set mode structured", "✅ Set mode = structured"),
        ("dmps> Explain machine learning", "Optimizing in structured mode..."),
        ("dmps> /history", "📝 History (2 items)"),
        ("dmps> /stats", "📊 Session Statistics"),
        ("dmps> /save my_session.json", "💾 Saved 2 items to my_session.json"),
        ("dmps> /quit", "👋 Thanks for using DMPS! Goodbye!")
    ]
    
    for command, response in session_commands:
        print(f"{command}")
        time.sleep(0.5)  # Simulate typing delay
        print(f"  {response}")
        print()


def example_3_repl_features():
    """Example 3: Advanced REPL features"""
    print("=" * 60)
    print("EXAMPLE 3: Advanced REPL Features")
    print("=" * 60)
    
    print("🔧 Configuration Management:")
    print("  /set mode conversational    # Human-readable output")
    print("  /set mode structured        # JSON output")
    print("  /set platform claude        # Optimize for Claude")
    print("  /set platform chatgpt       # Optimize for ChatGPT")
    print("  /set show_metadata true     # Show optimization metadata")
    print()
    
    print("📝 History & Session Management:")
    print("  /history                    # Show recent optimizations")
    print("  /clear                      # Clear history")
    print("  /save session.json          # Save session to file")
    print("  /load prompts.txt           # Load prompts from file")
    print()
    
    print("📊 Analytics & Insights:")
    print("  /stats                      # Usage statistics")
    print("  /examples                   # Example prompts")
    print()
    
    print("💡 Pro Tips:")
    print("  - Use Ctrl+C to interrupt long operations")
    print("  - Commands start with '/' - everything else is a prompt")
    print("  - History persists during the session")
    print("  - Save sessions for later analysis")


def example_4_batch_processing():
    """Example 4: Batch processing with REPL"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Batch Processing")
    print("=" * 60)
    
    # Create sample prompts file
    sample_prompts = [
        "Write documentation for a REST API",
        "Create unit tests for a login function", 
        "Explain blockchain to beginners",
        "Debug a memory leak in C++",
        "Design a database schema for e-commerce"
    ]
    
    prompts_file = Path("sample_prompts.txt")
    
    try:
        # Write sample file
        with open(prompts_file, 'w') as f:
            for prompt in sample_prompts:
                f.write(f"{prompt}\n")
        
        print(f"Created sample file: {prompts_file}")
        print("\nTo process these prompts in REPL:")
        print("  1. Start REPL: dmps-shell")
        print("  2. Load file: /load sample_prompts.txt")
        print("  3. View results: /history")
        print("  4. Save results: /save results.json")
        
        print(f"\nSample prompts in {prompts_file}:")
        for i, prompt in enumerate(sample_prompts, 1):
            print(f"  {i}. {prompt}")
    
    except Exception as e:
        print(f"Error creating sample file: {e}")
    
    finally:
        # Clean up
        if prompts_file.exists():
            prompts_file.unlink()


def example_5_integration_patterns():
    """Example 5: Integration with other tools"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Integration Patterns")
    print("=" * 60)
    
    print("🔗 Integration with Development Workflow:")
    print()
    
    print("1. Code Documentation:")
    print("   dmps> Write API documentation for user authentication endpoint")
    print("   dmps> /set platform chatgpt")
    print("   dmps> Create inline comments for this sorting algorithm")
    print()
    
    print("2. Testing & QA:")
    print("   dmps> Generate test cases for password validation")
    print("   dmps> /set mode structured")
    print("   dmps> Create bug reproduction steps for login issue")
    print()
    
    print("3. Content Creation:")
    print("   dmps> Write a technical blog post about microservices")
    print("   dmps> /set show_metadata true")
    print("   dmps> Create user manual for mobile app features")
    print()
    
    print("4. Learning & Education:")
    print("   dmps> Explain design patterns to junior developers")
    print("   dmps> /examples")
    print("   dmps> Create coding exercises for Python beginners")
    print()
    
    print("💡 Workflow Tips:")
    print("  - Use /save to preserve optimization sessions")
    print("  - Switch modes based on output needs")
    print("  - Use /stats to track optimization patterns")
    print("  - Load common prompts from files for consistency")


def example_6_repl_vs_cli():
    """Example 6: When to use REPL vs CLI"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: REPL vs CLI Usage")
    print("=" * 60)
    
    print("🖥️  Use CLI for:")
    print("  - One-off optimizations")
    print("  - Scripting and automation")
    print("  - CI/CD pipeline integration")
    print("  - Batch file processing")
    print()
    print("  Examples:")
    print("    dmps 'Write unit tests' --mode structured")
    print("    dmps --file prompts.txt --output results.json")
    print()
    
    print("🐚 Use REPL for:")
    print("  - Interactive prompt engineering")
    print("  - Iterative optimization")
    print("  - Learning and experimentation")
    print("  - Session-based workflows")
    print()
    print("  Examples:")
    print("    dmps-shell")
    print("    dmps> Write a story about AI")
    print("    dmps> /set mode structured")
    print("    dmps> Write a story about AI  # Compare outputs")
    print()
    
    print("🔄 Hybrid Approach:")
    print("  - Use REPL for development and testing")
    print("  - Use CLI for production and automation")
    print("  - Save REPL sessions for reproducible results")


def main():
    """Run all REPL usage examples"""
    print("DMPS REPL Usage Examples")
    print("This script demonstrates the DMPS REPL shell interface\n")
    
    try:
        example_1_basic_repl_usage()
        example_2_repl_session_simulation()
        example_3_repl_features()
        example_4_batch_processing()
        example_5_integration_patterns()
        example_6_repl_vs_cli()
        
        print("\n" + "=" * 60)
        print("All REPL examples completed!")
        print("\nTo try the REPL yourself:")
        print("  pip install dmps")
        print("  dmps-shell")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running REPL examples: {e}")


if __name__ == "__main__":
    main()