#!/usr/bin/env python3
"""
DMPS CLI Implementation
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .optimizer import PromptOptimizer
from .security import SecurityConfig


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="DMPS - Optimize AI prompts using 4-D methodology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Write me a story about AI"
  %(prog)s --mode structured "Debug this Python code"
  %(prog)s --platform chatgpt "Explain quantum"
  %(prog)s --file prompts.txt --output results.txt
  %(prog)s --interactive
        """,
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("prompt", nargs="?", help="Prompt to optimize")
    input_group.add_argument("--file", "-f", help="Read prompt from file")
    input_group.add_argument(
        "--interactive", "-i", action="store_true", help="Start interactive mode"
    )
    input_group.add_argument(
        "--shell", "-s", action="store_true", help="Start REPL shell mode"
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=["conversational", "structured"],
        default="conversational",
        help="Output format mode",
    )
    parser.add_argument(
        "--platform",
        "-p",
        choices=["claude", "chatgpt", "gemini", "generic"],
        default="claude",
        help="Target AI platform",
    )
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress progress messages"
    )
    parser.add_argument("--version", action="version", version="DMPS 0.2.1")
    parser.add_argument(
        "--metrics", action="store_true", help="Show context engineering metrics"
    )
    parser.add_argument(
        "--export-metrics", metavar="FILE", help="Export metrics to JSON file"
    )

    return parser


def read_file_content(filepath: str) -> str:
    """Read content from file with secure error handling"""
    from .error_handler import error_handler
    from .rbac import AccessControl, Role

    try:
        # RBAC validation
        if not AccessControl.validate_file_operation(Role.USER, "read", filepath):
            raise PermissionError("File access denied")

        # Validate against path traversal attacks BEFORE resolution
        if not SecurityConfig.validate_file_path(filepath):
            raise PermissionError(f"Unsafe file path: {filepath}")

        path = Path(filepath).resolve()

        # Additional validation after resolution
        if not SecurityConfig.validate_file_path(str(path)):
            raise PermissionError(f"Resolved path unsafe: {filepath}")

        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {filepath}")
        if path.stat().st_size > SecurityConfig.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {filepath}")

        return path.read_text(encoding="utf-8").strip()

    except (PermissionError, ValueError) as e:
        user_msg = error_handler.handle_security_error(e, f"read_file: {filepath}")
        print(user_msg, file=sys.stderr)
        sys.exit(1)
    except (OSError, FileNotFoundError) as e:
        user_msg = error_handler.handle_error(e, f"read_file: {filepath}")
        print(user_msg, file=sys.stderr)
        sys.exit(1)


def write_output(content: str, output_file: Optional[str] = None, quiet: bool = False):
    """Write output with secure error handling"""
    from .error_handler import error_handler
    from .rbac import AccessControl, Role

    try:
        if output_file:
            # RBAC validation
            if not AccessControl.validate_file_operation(
                Role.USER, "write", output_file
            ):
                raise PermissionError("File write access denied")

            # Validate against path traversal attacks BEFORE resolution
            if not SecurityConfig.validate_file_path(output_file):
                raise PermissionError(f"Unsafe output path: {output_file}")

            path = Path(output_file).resolve()

            # Additional validation after resolution
            if not SecurityConfig.validate_file_path(str(path)):
                raise PermissionError(f"Resolved output path unsafe: {output_file}")

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            if not quiet:
                print(f"Output written to: {output_file}", file=sys.stderr)
        else:
            print(content)

    except PermissionError as e:
        user_msg = error_handler.handle_security_error(
            e, f"write_output: {output_file}"
        )
        print(user_msg, file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as e:
        user_msg = error_handler.handle_error(e, f"write_output: {output_file}")
        print(user_msg, file=sys.stderr)
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

            if prompt.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if prompt.lower() == "help":
                print(
                    """
Available commands:
  help     - Show this help message
  quit     - Exit interactive mode
  mode     - Change output mode (conversational/structured)
  platform - Change target platform (claude/chatgpt/gemini/generic)

Just type your prompt to optimize it!
                """
                )
                continue

            if prompt.lower() == "mode":
                mode = input("Enter mode (conversational/structured): ").strip().lower()
                if mode in {"conversational", "structured"}:
                    print(f"Mode set to: {mode}")
                else:
                    print("Invalid mode. Use 'conversational' or 'structured'")
                continue

            if prompt.lower() == "platform":
                platform = input("Enter platform: ").strip().lower()
                if platform in {"claude", "chatgpt", "gemini", "generic"}:
                    print(f"Platform set to: {platform}")
                else:
                    print("Invalid platform.")
                continue

            print("Optimizing prompt...")
            result, validation = optimizer.optimize(
                prompt, mode="conversational", platform="claude"
            )

            if validation.warnings:
                print("Warnings:", file=sys.stderr)
                for warning in validation.warnings:
                    print(f"  - {warning}", file=sys.stderr)

            print("\n" + "=" * 60)
            print(result.optimized_prompt)
            print("=" * 60)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except (ValueError, TypeError) as e:
            from .error_handler import error_handler

            actionable_msg = error_handler.handle_error(e, "interactive_mode_input")
            print(f"Input error: {actionable_msg}", file=sys.stderr)
        except Exception as e:
            from .error_handler import error_handler

            actionable_msg = error_handler.handle_error(e, "interactive_mode_general")
            print(f"Error: {actionable_msg}", file=sys.stderr)


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    optimizer = PromptOptimizer()

    try:
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
            prompt_input = args.prompt if args.prompt is not None else ""

        if not prompt_input:
            print("Error: No prompt provided", file=sys.stderr)
            sys.exit(1)

        if not args.quiet:
            print(
                f"Optimizing prompt for {args.platform} in " f"{args.mode} mode...",
                file=sys.stderr,
            )

        result, validation = optimizer.optimize(
            prompt_input, mode=args.mode, platform=args.platform
        )

        if validation.warnings and not args.quiet:
            print("Warnings:", file=sys.stderr)
            for warning in validation.warnings:
                print(f"  - {warning}", file=sys.stderr)

        write_output(result.optimized_prompt, args.output, args.quiet)

        # Handle metrics options
        if args.metrics:
            from .observability import dashboard

            dashboard.print_session_summary()

        if args.export_metrics:
            from .observability import dashboard

            dashboard.export_metrics(args.export_metrics)

        if not args.quiet:
            techniques_count = len(result.improvements)
            print(
                f"Optimization complete! Applied {techniques_count} " f"improvements.",
                file=sys.stderr,
            )

            # Show token metrics if available
            if "token_metrics" in result.metadata:
                metrics = result.metadata["token_metrics"]
                print(
                    f"Token reduction: {
                        metrics['token_reduction']}, "
                    f"Cost estimate: ${
                        metrics['cost_estimate']:.4f}",
                    file=sys.stderr,
                )

            # Show evaluation warnings
            if (
                "evaluation" in result.metadata
                and result.metadata["evaluation"]["degradation_detected"]
            ):
                print("⚠️ Quality degradation detected", file=sys.stderr)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        from .error_handler import error_handler

        actionable_msg = error_handler.handle_error(e, "main_cli_execution")
        print(f"Error: {actionable_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
