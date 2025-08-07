"""
Tests for the REPL interface.
"""

import pytest
from unittest.mock import patch, MagicMock
from dmps.repl import DMPSShell


class TestDMPSShell:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.shell = DMPSShell()
    
    def test_shell_initialization(self):
        """Test shell initializes with correct defaults"""
        assert self.shell.settings["mode"] == "conversational"
        assert self.shell.settings["platform"] == "claude"
        assert self.shell.settings["show_metadata"] == False
        assert len(self.shell.history) == 0
    
    def test_command_parsing(self):
        """Test command parsing"""
        # Test help command
        with patch('builtins.print') as mock_print:
            self.shell.handle_command("help")
            mock_print.assert_called()
    
    def test_settings_command(self):
        """Test settings display"""
        with patch('builtins.print') as mock_print:
            self.shell.cmd_settings([])
            mock_print.assert_called()
    
    def test_set_command_valid(self):
        """Test setting valid values"""
        with patch('builtins.print'):
            self.shell.cmd_set(["mode", "structured"])
            assert self.shell.settings["mode"] == "structured"
            
            self.shell.cmd_set(["platform", "chatgpt"])
            assert self.shell.settings["platform"] == "chatgpt"
            
            self.shell.cmd_set(["show_metadata", "true"])
            assert self.shell.settings["show_metadata"] == True
    
    def test_set_command_invalid(self):
        """Test setting invalid values"""
        with patch('builtins.print') as mock_print:
            self.shell.cmd_set(["mode", "invalid"])
            mock_print.assert_called()
            assert self.shell.settings["mode"] == "conversational"  # Unchanged
    
    def test_history_empty(self):
        """Test history when empty"""
        with patch('builtins.print') as mock_print:
            self.shell.cmd_history([])
            mock_print.assert_called_with("📝 No history yet")
    
    def test_clear_history(self):
        """Test clearing history"""
        # Add some fake history
        self.shell.history = [{"test": "data"}]
        
        with patch('builtins.print'):
            self.shell.cmd_clear([])
        
        assert len(self.shell.history) == 0
    
    def test_examples_command(self):
        """Test examples display"""
        with patch('builtins.print') as mock_print:
            self.shell.cmd_examples([])
            mock_print.assert_called()
    
    def test_stats_empty(self):
        """Test stats when no history"""
        with patch('builtins.print') as mock_print:
            self.shell.cmd_stats([])
            mock_print.assert_called_with("📊 No statistics yet")
    
    @patch('dmps.repl.sys.exit')
    def test_quit_command(self, mock_exit):
        """Test quit command"""
        with patch('builtins.print'):
            self.shell.cmd_quit([])
        mock_exit.assert_called_with(0)
    
    def test_optimize_and_display(self):
        """Test prompt optimization and display"""
        with patch('builtins.print'):
            self.shell.optimize_and_display("Write a story")
        
        # Should add to history
        assert len(self.shell.history) == 1
        assert self.shell.history[0]["input"] == "Write a story"
    
    @patch('builtins.open')
    @patch('json.dump')
    def test_save_command(self, mock_json_dump, mock_open):
        """Test saving history to file"""
        # Add some history
        self.shell.history = [{
            "input": "test",
            "result": MagicMock(optimized_prompt="optimized", improvements=[]),
            "validation": MagicMock(is_valid=True, errors=[]),
            "settings": {"mode": "conversational"}
        }]
        
        with patch('builtins.print'):
            self.shell.cmd_save(["test.json"])
        
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()
    
    def test_unknown_command(self):
        """Test handling unknown commands"""
        with patch('builtins.print') as mock_print:
            self.shell.handle_command("unknown_command")
            mock_print.assert_any_call("Unknown command: /unknown_command")