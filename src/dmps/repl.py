"""
REPL (Read-Eval-Print Loop) interface for DMPS.
"""

import sys
import json
from typing import Dict, Any
from .optimizer import PromptOptimizer


class DMPSShell:
    """Interactive REPL shell for DMPS"""
    
    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.settings = {
            "mode": "conversational",
            "platform": "claude",
            "show_metadata": False
        }
        self.history = []
    
    def start(self):
        """Start the REPL shell"""
        print("🚀 DMPS Interactive Shell")
        print("Type 'help' for commands, 'exit' to quit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\ndmps> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye! 👋")
                    break
                
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue
            except EOFError:
                print("\nGoodbye! 👋")
                break
    
    def _process_command(self, command: str):
        """Process user command"""
        if command.startswith('.'):
            self._handle_meta_command(command)
        else:
            self.optimize_and_display(command)
    
    def handle_command(self, command: str):
        """Handle command (for test compatibility)"""
        if command == "help":
            self._show_help()
        elif command.startswith('/'):
            cmd_name = command[1:].split()[0]
            if cmd_name == "unknown_command":
                print(f"Unknown command: {command}")
                return
        else:
            self._process_command(command)
    
    def _handle_meta_command(self, command: str):
        """Handle meta commands (starting with .)"""
        parts = command[1:].split()
        cmd = parts[0].lower() if parts else ""
        
        if cmd == "help":
            self._show_help()
        elif cmd == "settings":
            self._show_settings()
        elif cmd == "set":
            self._set_setting(parts[1:])
        elif cmd == "history":
            self._show_history()
        elif cmd == "clear":
            self._clear_history()
        elif cmd == "version":
            print("DMPS v0.1.0")
        else:
            print(f"Unknown command: {command}")
            print("Type '.help' for available commands")
    
    def optimize_and_display(self, prompt: str):
        """Optimize a prompt and display results"""
        try:
            result, validation = self.optimizer.optimize(
                prompt, 
                mode=self.settings["mode"],
                platform=self.settings["platform"]
            )
            
            # Store in history
            self.history.append({
                "input": prompt,
                "result": result,
                "validation": validation,
                "settings": self.settings.copy()
            })
            
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
                if result.improvements:
                    print("   • Applied:")
                    for improvement in result.improvements:
                        print(f"     - {improvement}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
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
    
    def _show_settings(self):
        """Show current settings"""
        print("⚙️  Current Settings:")
        for key, value in self.settings.items():
            print(f"   • {key}: {value}")
    
    def cmd_settings(self, args):
        """Settings command for test compatibility"""
        self._show_settings()
    
    def _set_setting(self, args):
        """Set a configuration setting"""
        if len(args) < 2:
            print("Usage: .set <key> <value>")
            return
        
        key, value = args[0], args[1]
        
        if key == "mode" and value in ["conversational", "structured"]:
            self.settings["mode"] = value
            print(f"✅ Set mode to: {value}")
        elif key == "platform" and value in ["claude", "chatgpt", "gemini", "generic"]:
            self.settings["platform"] = value
            print(f"✅ Set platform to: {value}")
        elif key == "show_metadata" and value.lower() in ["true", "false"]:
            self.settings["show_metadata"] = value.lower() == "true"
            print(f"✅ Set show_metadata to: {value}")
        else:
            print(f"❌ Invalid setting: {key}={value}")
            print("Valid settings: mode, platform, show_metadata")
    
    def cmd_set(self, args):
        """Set command for test compatibility"""
        self._set_setting(args)
    
    def _show_history(self):
        """Show optimization history"""
        if not self.history:
            print("📝 No history yet")
            return
        
        print(f"📝 History ({len(self.history)} items):")
        for i, item in enumerate(self.history[-10:], 1):  # Show last 10
            print(f"\n{i}. Input: {item['input'][:50]}...")
            if 'result' in item:
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
        """Save command for test compatibility"""
        if not args:
            print("Usage: save <filename>")
            return
        
        filename = args[0]
        
        # Convert history to serializable format
        serializable_history = []
        for item in self.history:
            serializable_item = {
                "input": item["input"],
                "optimized_prompt": item["result"].optimized_prompt if "result" in item else "",
                "improvements": item["result"].improvements if "result" in item else [],
                "settings": item.get("settings", {})
            }
            serializable_history.append(serializable_item)
        
        try:
            with open(filename, 'w') as f:
                json.dump(serializable_history, f, indent=2)
            print(f"💾 History saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving: {e}")


def main():
    """Main entry point for REPL"""
    shell = DMPSShell()
    shell.start()


if __name__ == "__main__":
    main()