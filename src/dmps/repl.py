"""
DMPS REPL (Read-Eval-Print Loop) Interface
Interactive shell for prompt optimization.
"""

import sys
import os
import json
from typing import Dict, List, Optional
from .optimizer import PromptOptimizer
from .schema import OptimizedResult, ValidationResult


class DMPSShell:
    """Interactive REPL shell for DMPS"""
    
    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.history = []
        self.settings = {
            "mode": "conversational",
            "platform": "claude",
            "show_metadata": False,
            "auto_copy": False
        }
        self.commands = {
            "help": self.cmd_help,
            "quit": self.cmd_quit,
            "exit": self.cmd_quit,
            "q": self.cmd_quit,
            "settings": self.cmd_settings,
            "set": self.cmd_set,
            "history": self.cmd_history,
            "clear": self.cmd_clear,
            "save": self.cmd_save,
            "load": self.cmd_load,
            "examples": self.cmd_examples,
            "stats": self.cmd_stats
        }
    
    def start(self):
        """Start the REPL shell"""
        self.print_welcome()
        
        while True:
            try:
                prompt_input = input("\ndmps> ").strip()
                
                if not prompt_input:
                    continue
                
                # Check for commands
                if prompt_input.startswith("/"):
                    self.handle_command(prompt_input[1:])
                    continue
                
                # Optimize prompt
                self.optimize_and_display(prompt_input)
                
            except KeyboardInterrupt:
                print("\nUse /quit to exit")
                continue
            except EOFError:
                print("\nGoodbye!")
                break
    
    def print_welcome(self):
        """Print welcome message"""
        print("DMPS Interactive Shell")
        print("=" * 40)
        print("Type your prompts to optimize them instantly!")
        print("Commands start with '/' - try /help for options")
        print("Press Ctrl+C to interrupt, /quit to exit")
        print(f"Current settings: {self.settings['mode']} mode, {self.settings['platform']} platform")
    
    def handle_command(self, command_line: str):
        """Handle shell commands"""
        parts = command_line.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"Unknown command: /{cmd}")
            print("Type /help for available commands")
    
    def optimize_and_display(self, prompt_input: str):
        """Optimize prompt and display results"""
        try:
            result, validation = self.optimizer.optimize(
                prompt_input,
                mode=self.settings["mode"],
                platform=self.settings["platform"]
            )
            
            # Add to history
            self.history.append({
                "input": prompt_input,
                "result": result,
                "validation": validation,
                "settings": self.settings.copy()
            })
            
            # Display results
            if validation.is_valid:
                self.display_result(result, validation)
            else:
                self.display_errors(validation)
                
        except Exception as e:
            print(f"Error: {e}")
    
    def display_result(self, result: OptimizedResult, validation: ValidationResult):
        """Display optimization results"""
        print("\n" + "=" * 60)
        
        if self.settings["mode"] == "conversational":
            print(result.optimized_prompt)
        else:
            # Pretty print JSON for structured mode
            try:
                data = json.loads(result.optimized_prompt)
                print(json.dumps(data, indent=2))
            except:
                print(result.optimized_prompt)
        
        if validation.warnings:
            print(f"\nWarnings: {', '.join(validation.warnings)}")
        
        if self.settings["show_metadata"]:
            print(f"\nMetadata:")
            for key, value in result.metadata.items():
                print(f"  {key}: {value}")
        
        print("=" * 60)
    
    def display_errors(self, validation: ValidationResult):
        """Display validation errors"""
        print(f"\nValidation failed:")
        for error in validation.errors:
            print(f"  • {error}")
    
    def cmd_help(self, args: List[str]):
        """Show help information"""
        print("\nDMPS Shell Commands:")
        print("=" * 40)
        print("/help              - Show this help")
        print("/quit, /exit, /q   - Exit the shell")
        print("/settings          - Show current settings")
        print("/set <key> <value> - Change setting")
        print("/history           - Show optimization history")
        print("/clear             - Clear history")
        print("/save <file>       - Save history to file")
        print("/load <file>       - Load prompts from file")
        print("/examples          - Show example prompts")
        print("/stats             - Show usage statistics")
        print("\nAvailable Settings:")
        print("  mode: conversational, structured")
        print("  platform: claude, chatgpt, gemini, generic")
        print("  show_metadata: true, false")
        print("  auto_copy: true, false")
        print("\nExamples:")
        print("  /set mode structured")
        print("  /set platform chatgpt")
        print("  /save my_session.json")
    
    def cmd_quit(self, args: List[str]):
        """Exit the shell"""
        print("Thanks for using DMPS! Goodbye!")
        sys.exit(0)
    
    def cmd_settings(self, args: List[str]):
        """Show current settings"""
        print("\nCurrent Settings:")
        for key, value in self.settings.items():
            print(f"  {key}: {value}")
    
    def cmd_set(self, args: List[str]):
        """Change a setting"""
        if len(args) < 2:
            print("Usage: /set <key> <value>")
            return
        
        key, value = args[0], args[1]
        
        if key not in self.settings:
            print(f"Unknown setting: {key}")
            print(f"Available: {', '.join(self.settings.keys())}")
            return
        
        # Validate values
        if key == "mode" and value not in ["conversational", "structured"]:
            print("Mode must be 'conversational' or 'structured'")
            return
        
        if key == "platform" and value not in ["claude", "chatgpt", "gemini", "generic"]:
            print("Platform must be 'claude', 'chatgpt', 'gemini', or 'generic'")
            return
        
        if key in ["show_metadata", "auto_copy"]:
            value = value.lower() in ["true", "1", "yes", "on"]
        
        self.settings[key] = value
        print(f"Set {key} = {value}")
    
    def cmd_history(self, args: List[str]):
        """Show optimization history"""
        if not self.history:
            print("No history yet")
            return
        
        print(f"\nHistory ({len(self.history)} items):")
        print("=" * 40)
        
        for i, item in enumerate(self.history[-10:], 1):  # Show last 10
            print(f"{i}. {item['input'][:50]}{'...' if len(item['input']) > 50 else ''}")
            print(f"   Mode: {item['settings']['mode']}, Platform: {item['settings']['platform']}")
            if item['validation'].is_valid:
                improvements = len(item['result'].improvements)
                print(f"   Success: {improvements} improvements applied")
            else:
                print(f"   Failed validation")
            print()
    
    def cmd_clear(self, args: List[str]):
        """Clear history"""
        self.history.clear()
        print("History cleared")
    
    def cmd_save(self, args: List[str]):
        """Save history to file"""
        if not args:
            filename = "dmps_session.json"
        else:
            filename = args[0]
        
        try:
            # Prepare data for JSON serialization
            export_data = []
            for item in self.history:
                export_data.append({
                    "input": item["input"],
                    "optimized": item["result"].optimized_prompt if item["validation"].is_valid else None,
                    "improvements": item["result"].improvements if item["validation"].is_valid else [],
                    "settings": item["settings"],
                    "valid": item["validation"].is_valid,
                    "errors": item["validation"].errors
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(export_data)} items to {filename}")
            
        except Exception as e:
            print(f"Failed to save: {e}")
    
    def cmd_load(self, args: List[str]):
        """Load prompts from file"""
        if not args:
            print("Usage: /load <filename>")
            return
        
        filename = args[0]
        
        try:
            if filename.endswith('.json'):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "input" in item:
                            print(f"\nProcessing: {item['input'][:50]}...")
                            self.optimize_and_display(item["input"])
                else:
                    print("Invalid JSON format")
            else:
                # Plain text file - each line is a prompt
                with open(filename, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            print(f"\nProcessing line {line_num}: {line[:50]}...")
                            self.optimize_and_display(line)
            
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Failed to load: {e}")
    
    def cmd_examples(self, args: List[str]):
        """Show example prompts"""
        examples = [
            "Write a technical blog post about machine learning",
            "Create a user manual for a mobile app",
            "Explain quantum computing to a 10-year-old",
            "Debug this Python sorting function",
            "Generate test cases for a login system",
            "Write a creative story about time travel",
            "Analyze the pros and cons of remote work",
            "Create a marketing strategy for a startup"
        ]
        
        print("\nExample Prompts:")
        print("=" * 40)
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
        
        print("\nTry copying and pasting any of these!")
    
    def cmd_stats(self, args: List[str]):
        """Show usage statistics"""
        if not self.history:
            print("No statistics yet")
            return
        
        total = len(self.history)
        successful = sum(1 for item in self.history if item["validation"].is_valid)
        failed = total - successful
        
        # Intent distribution
        intents = {}
        platforms = {}
        modes = {}
        
        for item in self.history:
            if item["validation"].is_valid:
                intent = item["result"].metadata.get("intent", "unknown")
                intents[intent] = intents.get(intent, 0) + 1
            
            platform = item["settings"]["platform"]
            platforms[platform] = platforms.get(platform, 0) + 1
            
            mode = item["settings"]["mode"]
            modes[mode] = modes.get(mode, 0) + 1
        
        print(f"\nSession Statistics:")
        print("=" * 40)
        print(f"Total prompts: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        
        if intents:
            print(f"\nIntent Distribution:")
            for intent, count in sorted(intents.items(), key=lambda x: x[1], reverse=True):
                print(f"  {intent}: {count}")
        
        print(f"\nPlatform Usage:")
        for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
            print(f"  {platform}: {count}")
        
        print(f"\nMode Usage:")
        for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
            print(f"  {mode}: {count}")


def main():
    """Main entry point for DMPS shell"""
    shell = DMPSShell()
    shell.start()


if __name__ == "__main__":
    main()