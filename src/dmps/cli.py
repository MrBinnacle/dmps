#!/usr/bin/env python3
"""
Dual-Mode Prompt System (DMPS) - CLI Implementation
A system that optimizes AI prompts using the 4-D methodology.

Usage:
    python -m dmps.cli "Write me a story"
    python -m dmps.cli --mode structured --platform chatgpt "Debug this code"
    python -m dmps.cli --file input.txt --mode conversational
"""

import argparse
import sys
from pathlib import Path
from .optimizer import PromptOptimizer


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Dual-Mode Prompt System (DMPS) - Optimize AI prompts using 4-D methodology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Write me a story about AI"
  %(prog)s --mode structured "Debug this Python code"
  %(prog)s --platform chatgpt --mode conversational "Explain quantum computing"
  %(prog)s --file prompts.txt --output results.txt
  %(prog)s --interactive
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to optimize"
    )
    input_group.add_argument(
        "--file", "-f",
        type=str,
        help="Read prompt from file"
    )
    input_group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    input_group.add_argument(
        "--shell", "-s",
        action="store_true",
        help="Start REPL shell mode"
    )
    
    # Output options
    parser.add_argument(
        "--mode", "-m",
        choices=["conversational", "structured"],
        default="conversational",
        help="Output format mode (default: conversational)"
    )
    
    parser.add_argument(
        "--platform", "-p",
        choices=["claude", "chatgpt", "gemini", "generic"],
        default="claude",
        help="Target AI platform (default: claude)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file (default: stdout)"
    )
    
    # Additional options
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress messages"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="DMPS 0.1.0"
    )
    
    return parser


def show_examples():
    """Display usage examples"""
    examples = """
DMPS Usage Examples:

Basic Usage:
  python -m dmps.cli "Write a story about a robot learning to paint"
  python -m dmps.cli "Explain how neural networks work"
  python -m dmps.cli "Debug this Python function that sorts a list"

Advanced Usage:
  python -m dmps.cli --mode structured --platform chatgpt "Create a REST API"
  python -m dmps.cli --file my_prompt.txt --output optimized.txt
  python -m dmps.cli --platform gemini "Write a technical blog post"

Interactive Mode:
  python -m dmps.cli --interactive

File Processing:
  python -m dmps.cli --file batch_prompts.txt --mode structured --output results.json
    """
    print(examples)


def read_file_content(filepath: str) -> str:
    """Read content from file"""
    try:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        return path.read_text(encoding='utf-8').strip()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def write_output(content: str, output_file: str = None, quiet: bool = False):
    """Write output to file or stdout"""
    try:
        if output_file:
            Path(output_file).write_text(content, encoding='utf-8')
            if not quiet:
                print(f"Output written to: {output_file}", file=sys.stderr)
        else:
            print(content)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


def interactive_mode():
    """Run in interactive mode"""
    optimizer = PromptOptimizer()
    
    print("DMPS Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            prompt = input("\nEnter your prompt: ").strip()
            
            if not prompt:
                continue
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if prompt.lower() == 'help':
                print("""
Available commands:
  help     - Show this help message
  quit     - Exit interactive mode
  mode     - Change output mode (conversational/structured)
  platform - Change target platform (claude/chatgpt/gemini/generic)
  
Just type your prompt to optimize it!
                """)
                continue
            
            if prompt.lower() == 'mode':
                mode = input("Enter mode (conversational/structured): ").strip().lower()
                if mode in ['conversational', 'structured']:
                    print(f"Mode set to: {mode}")
                    # Store mode for next optimization
                else:
                    print("Invalid mode. Use 'conversational' or 'structured'")
                continue
            
            if prompt.lower() == 'platform':
                platform = input("Enter platform (claude/chatgpt/gemini/generic): ").strip().lower()
                if platform in ['claude', 'chatgpt', 'gemini', 'generic']:
                    print(f"Platform set to: {platform}")
                    # Store platform for next optimization
                else:
                    print("Invalid platform.")
                continue
            
            # Optimize the prompt
            print("Optimizing prompt...")
            result, validation = optimizer.optimize(prompt, mode="conversational", platform="claude")
            
            if validation.warnings:
                print("Warnings:", file=sys.stderr)
                for warning in validation.warnings:
                    print(f"  - {warning}", file=sys.stderr)
            
            print("\n" + "="*60)
            print(result.optimized_prompt)
            print("="*60)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle special cases
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Initialize optimizer
    optimizer = PromptOptimizer()
    
    try:
        # Determine input source
        if args.interactive:
            interactive_mode()
            return
        
        if args.shell:
            from .repl import main as repl_main
            repl_main()
            return
        
        if args.file:
            prompt_input = read_file_content(args.file)
        else:
            prompt_input = args.prompt or ""
        
        if not prompt_input:
            print("Error: No prompt provided", file=sys.stderr)
            sys.exit(1)
        
        # Progress message
        if not args.quiet:
            print(f"Optimizing prompt for {args.platform} in {args.mode} mode...", file=sys.stderr)
        
        # Optimize prompt
        result, validation = optimizer.optimize(
            prompt_input,
            mode=args.mode,
            platform=args.platform
        )
        
        # Show warnings
        if validation.warnings and not args.quiet:
            print("Warnings:", file=sys.stderr)
            for warning in validation.warnings:
                print(f"  - {warning}", file=sys.stderr)
        
        # Output result
        write_output(result.optimized_prompt, args.output, args.quiet)
        
        # Success message
        if not args.quiet:
            techniques_count = len(result.improvements)
            print(f"Optimization complete! Applied {techniques_count} improvements.", file=sys.stderr)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
