"""
REPL (Read-Eval-Print Loop) interface for DMPS.
"""

import hashlib
import json
import sys
import time
from typing import Any, Dict, Final

from .optimizer import PromptOptimizer
from .rbac import AccessControl, Role
from .security import SecurityConfig


class DMPSShell:
    def _show_settings(self):
        """Show current shell settings"""
        print("Current settings:")
        for k, v in self.settings.items():
            print(f"  {k}: {v}")

    def _set_setting(self, key: str, value: str):
        """Set a configuration setting."""
        self.settings[key] = value
        print(f"Setting '{key}' updated to: {value}")

    """Interactive REPL shell for DMPS"""

    # Valid settings for validation
    _VALID_MODES: Final = frozenset({"conversational", "structured"})
    _VALID_PLATFORMS: Final = frozenset({"claude", "chatgpt", "gemini", "generic"})

    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.settings = {
            "mode": "conversational",
            "platform": "claude",
            "show_metadata": False,
        }
        self.history = []
        self.max_history = SecurityConfig.MAX_HISTORY_SIZE
        self.request_count = 0
        self.max_requests = SecurityConfig.MAX_REQUESTS_PER_SESSION
        self.session_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.failed_attempts = 0
        self.last_activity = time.time()
        self._audit_log = []

    def start(self):
        """Start the REPL shell with security monitoring"""
        self._log_security_event("session_start", {"session_id": self.session_id})
        print("DMPS Interactive Shell")
        print("Type 'help' for commands, 'exit' to quit")
        print("=" * 50)

        while True:
            try:
                user_input = input("\ndmps> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Goodbye! 👋")
                    break

                if self._validate_session():
                    self._process_command(user_input)
                    self.last_activity = time.time()
                else:
                    print("Session expired. Please restart.")
                    break

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue
            except EOFError:
                print("\nGoodbye! 👋")
                break

    def _process_command(self, command: str):
        """Process user command"""
        if command.startswith("."):
            self._handle_meta_command(command)
        else:
            self.optimize_and_display(command)

    def handle_command(self, command: str):
        """Handle command with RBAC validation"""
        from .rbac import AccessControl, Role

        # Validate user role and command authorization
        # Validate user role and command authorization
        if not AccessControl.is_command_allowed(Role.USER, command):
            print(f"Access denied: {command}")
            return

        if command == "help":
            self._show_help()
        elif command.startswith("/"):
            print(f"Access denied: {command}")
            return
        else:
            self._process_command(command)

    def _handle_meta_command(self, command: str):
        """Handle meta commands with RBAC validation"""
        from .rbac import AccessControl, Role

        parts = command[1:].split()
        cmd = parts[0].lower() if parts else ""

        # Comprehensive RBAC validation
        if not AccessControl.validate_command_access(Role.USER, f".{cmd}"):
            print(f"Access denied: {command}")
            print("Type '.help' for available commands")
            return

        # Additional validation for sensitive commands
        if cmd in ["export", "clear"] and not AccessControl.validate_file_operation(
            Role.USER, "write", "."
        ):
            print(f"Insufficient permissions for: {command}")
            return

        if cmd == "help":
            self._show_help()
        elif cmd == "settings":
            self._display_current_configuration()
        elif cmd == "set":
            if len(parts) < 3:
                print("Usage: .set <setting_name> <setting_value>")
            else:
                self._update_configuration_setting(parts[1], parts[2])
        elif cmd == "history":
            self._show_history()
        elif cmd == "clear":
            self._clear_history()
        elif cmd == "version":
            print("DMPS v0.1.0")
        elif cmd == "metrics":
            from .observability import dashboard

            dashboard.print_session_summary()
        elif cmd == "export":
            filename = parts[1] if len(parts) > 1 else "repl_metrics.json"
            from .observability import dashboard

            dashboard.export_metrics(filename)

    def optimize_and_display(self, prompt: str):
        """Optimize a prompt and display results with security validation"""
        try:
            # Security validation
            if not self._validate_command_security(prompt):
                print("❌ Command blocked by security policy")
                return

            # Rate limiting check
            self.request_count += 1
            if self.request_count > self.max_requests:
                self._log_security_event(
                    "rate_limit_exceeded", {"request_count": self.request_count}
                )
                print("❌ Rate limit exceeded. Please restart the session.")
                return

            result, validation = self.optimizer.optimize(
                prompt, mode=self.settings["mode"], platform=self.settings["platform"]
            )

            # Store in history with size limit
            self.history.append(
                {
                    "input": prompt,
                    "result": result,
                    "validation": validation,
                    "settings": self.settings.copy(),
                }
            )

            # Maintain history size limit
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history :]

            # Show warnings if any
            if validation.warnings:
                print("⚠️  Warnings:")
                for warning in validation.warnings:
                    print(f"   • {warning}")
                print()

            # Show result
            print("✨ Optimized Result:")
            print("-" * 30)
            print(result.optimized_prompt)

            # Show metadata if enabled
            if self.settings["show_metadata"]:
                print("\n📊 Metadata:")
                print(f"   • Improvements: {len(result.improvements)}")
                print(f"   • Methodology: {result.methodology_applied}")

                # Show token metrics
                if "token_metrics" in result.metadata:
                    metrics = result.metadata["token_metrics"]
                    token_reduction = metrics["token_reduction"]
                    cost_estimate = metrics["cost_estimate"]
                    print(
                        f"Token reduction: {token_reduction}, "
                        f"Cost estimate: ${cost_estimate:.4f}",
                        file=sys.stderr,
                    )

                # Show evaluation metrics
                if "evaluation" in result.metadata:
                    eval_data = result.metadata["evaluation"]
                    overall_score = eval_data["overall_score"]
                    token_efficiency = eval_data["token_efficiency"]
                    print(f"   • Quality Score: {overall_score}")
                    print(f"   • Token Efficiency: {token_efficiency}")

                if result.improvements:
                    techniques_count = len(result.improvements)
                    print(
                        f"Optimization complete! Applied {techniques_count} improvements.",
                        file=sys.stderr,
                    )

                for improvement in result.improvements:
                    print(f"     - {improvement}")

        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled")

        except (ValueError, TypeError) as e:
            from .error_handler import error_handler

            user_msg = error_handler.handle_error(e, "optimize_and_display")
            print(f"❌ {user_msg}")

        except Exception as e:
            from .error_handler import error_handler

            user_msg = error_handler.handle_error(e, "optimize_and_display")
            print(f"❌ {user_msg}")

    def _show_help(self):
        """Show help information"""
        help_text = """
📚 DMPS Shell Commands:

Prompt Optimization:
  <your prompt>     - Optimize the given prompt

Meta Commands:
  .help            - Show this help message
  .settings        - Show current settings
  .set <key> <val> - Change setting (mode, platform, show_metadata)
  .history         - Show optimization history
  .clear           - Clear history
  .version         - Show version
  .metrics         - Show context engineering metrics
  .export [file]   - Export metrics to JSON file
  exit/quit        - Exit the shell

Settings:
  mode: conversational, structured
  platform: claude, chatgpt, gemini, generic
  show_metadata: true, false

Examples:
  dmps> Write a story about AI
  dmps> .set mode structured
  dmps> .set platform chatgpt
        """
        print(help_text)

    def _display_current_configuration(self):
        """Display current REPL configuration settings"""
        print("⚙️  Current Configuration:")
        for setting_name, setting_value in self.settings.items():
            print(f"   • {setting_name}: {setting_value}")

    def cmd_settings(self, args):
        """Settings command for test compatibility"""
        self._show_settings()

    def _update_configuration_setting(self, command_args):
        """Update a specific configuration setting"""
        if len(command_args) < 2:
            print("Usage: .set <setting_name> <setting_value>")
            return

        setting_name, new_value = command_args[0], command_args[1]

        if setting_name == "mode" and new_value in self._VALID_MODES:
            self.settings["mode"] = new_value
            print(f"✅ Updated mode to: {new_value}")
        elif setting_name == "platform" and new_value in self._VALID_PLATFORMS:
            self.settings["platform"] = new_value
            print(f"✅ Updated platform to: {new_value}")
        elif setting_name == "show_metadata" and new_value.lower() in ["true", "false"]:
            self.settings["show_metadata"] = new_value.lower() == "true"
            print(f"✅ Updated show_metadata to: {new_value}")
        else:
            print(f"❌ Invalid configuration: {setting_name}={new_value}")
            print("Valid settings: mode, platform, show_metadata")

    def cmd_set(self, args):
        """Set command for test compatibility"""
        if len(args) < 2:
            print("Usage: .set <setting_name> <setting_value>")
            return
        setting_name, new_value = args[0], args[1]
        self._set_setting(setting_name, new_value)

    def _show_history(self):
        """Show optimization history"""
        if not self.history:
            print("📝 No history yet")
            return

        print(f"📝 History ({len(self.history)} items):")
        for i, item in enumerate(self.history[-10:], 1):  # Show last 10
            print(f"\n{i}. Input: {item['input'][:50]}...")
            if "result" in item:
                print(f"   Improvements: {len(item['result'].improvements)}")

    def cmd_history(self, args):
        """History command for test compatibility"""
        self._show_history()

    def _clear_history(self):
        """Clear optimization history"""
        self.history.clear()
        print("🗑️  History cleared")

    def cmd_clear(self, args):
        """Clear command for test compatibility"""
        self._clear_history()

    def cmd_examples(self, args):
        """Examples command for test compatibility"""
        print("📚 Example prompts:")
        print("• Write a story about AI")
        print("• Explain quantum computing")
        print("• Debug this Python code")

    def cmd_stats(self, args):
        """Stats command for test compatibility"""
        if not self.history:
            print("📊 No statistics yet")
            return
        print(f"📊 Total optimizations: {len(self.history)}")

    def cmd_quit(self, args):
        """Quit command for test compatibility"""
        print("Goodbye! 👋")
        sys.exit(0)

    def cmd_save(self, args):
        """Save command with path traversal protection"""
        if not args:
            print("Usage: save <filename>")
            return

        filename = args[0]

        try:
            from pathlib import Path

            # Validate path before resolving to prevent traversal
            if not SecurityConfig.validate_file_path(filename):
                print(f"❌ Invalid file path: {filename}")
                return

            # Additional RBAC validation for save operation
            if not AccessControl.validate_file_operation(Role.USER, "write", filename):
                print(f"❌ Access denied for file operation: {filename}")
                return

            path = Path(filename).resolve()

            # Critical: Re-validate resolved path to prevent bypass
            if not SecurityConfig.validate_file_path(str(path)):
                print(f"❌ Unsafe resolved path: {filename}")
                return

            # Validate file extension
            if not SecurityConfig.validate_file_extension(filename):
                print("❌ Only .json and .txt files are allowed")
                return

            # Sanitize filename
            filename = SecurityConfig.sanitize_filename(filename)

            # Convert history to serializable format
            serializable_history = []
            for item in self.history:
                serializable_item = {
                    "input": item["input"],
                    "optimized_prompt": (
                        item["result"].optimized_prompt if "result" in item else ""
                    ),
                    "improvements": (
                        item["result"].improvements if "result" in item else []
                    ),
                    "settings": item.get("settings", {}),
                }
                serializable_history.append(serializable_item)

            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(serializable_history, f, indent=2)
            print(f"💾 History saved to {filename}")

        except (OSError, ValueError, TypeError) as e:
            self._log_security_event(
                "file_operation_failed", {"error": str(e), "filename": filename}
            )
            print(f"❌ Error saving: {e}")
        except Exception as e:
            self._log_security_event(
                "file_operation_failed", {"error": str(e), "filename": filename}
            )
            print(f"❌ Error saving: {e}")

    def _validate_session(self) -> bool:
        """Validate session security constraints"""
        # Session timeout check (30 minutes)
        if time.time() - self.last_activity > 1800:
            self._log_security_event("session_timeout", {"session_id": self.session_id})
            return False

        # Rate limiting validation
        if self.request_count > self.max_requests:
            self._log_security_event(
                "rate_limit_exceeded", {"session_id": self.session_id}
            )
            return False

        return True

    def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for audit trail"""
        event = {
            "timestamp": time.time(),
            "session_id": self.session_id,
            "event_type": event_type,
            "details": details,
        }
        self._audit_log.append(event)

        # Maintain audit log size
        if len(self._audit_log) > 1000:
            self._audit_log = self._audit_log[-1000:]

    def _validate_command_security(self, command: str) -> bool:
        """Validate command against security policies"""
        # Block potentially dangerous commands
        dangerous_patterns = ["eval", "exec", "import", "__", "subprocess"]
        if any(pattern in command.lower() for pattern in dangerous_patterns):
            self._log_security_event("dangerous_command_blocked", {"command": command})
            return False

        # RBAC validation
        if not AccessControl.validate_command_access(Role.USER, command):
            self._log_security_event("access_denied", {"command": command})
            return False

        return True


def main():
    """Main entry point for REPL"""
    shell = DMPSShell()
    shell.start()


if __name__ == "__main__":
    main()
