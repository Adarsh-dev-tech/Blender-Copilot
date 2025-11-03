"""
Integration tests for command parsing edge cases.

Tests unusual, extreme, or malformed command inputs to ensure
robust parsing behavior.

Run with: blender --background --python -m pytest tests/integration/test_command_edge_cases.py

NOTE: These tests will FAIL until the parser is fully implemented.
"""

import sys
from pathlib import Path

try:
    import bpy
except ImportError:
    print("ERROR: This test requires Blender. Run with: blender --background --python -m pytest")
    sys.exit(1)

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestVeryLongCommands:
    """Test parsing of very long command strings."""
    
    def test_command_with_1000_characters(self):
        """Test command with 1000+ characters doesn't break parser."""
        from copilot.utils.command_parser import parse_command
        
        long_command = "please " * 200 + "create an array"  # ~1200 chars
        result = parse_command(long_command)
        
        assert result == 'SMART_ARRAY'  # Should still find the keyword
    
    def test_very_verbose_command(self):
        """Test parser handles very verbose natural language."""
        from copilot.utils.command_parser import parse_command
        
        verbose = "I would really like to apply a hard-surface setup to this mesh object if that's possible please"
        result = parse_command(verbose)
        
        assert result == 'HARD_SURFACE'


class TestSpecialCharacters:
    """Test commands with unusual characters."""
    
    def test_unicode_characters(self):
        """Test commands with Unicode characters."""
        from copilot.utils.command_parser import parse_command
        
        # Unicode characters mixed with command
        commands = [
            "créate an array 🎨",  # Accented chars + emoji
            "make 配列 array",  # Japanese chars
            "solidify ✓",  # Checkmark
        ]
        
        results = [parse_command(cmd) for cmd in commands]
        
        # Should still recognize keywords despite Unicode
        assert 'SMART_ARRAY' in results or 'UNKNOWN' in results
        assert 'SOLIDIFY' in results or 'UNKNOWN' in results
    
    def test_special_punctuation(self):
        """Test commands with lots of punctuation."""
        from copilot.utils.command_parser import parse_command
        
        commands = [
            "!!!array!!!",
            "hard-surface???",
            "solidify...",
            "@#$%mirror^&*()",
        ]
        
        # Should handle gracefully (either parse or return UNKNOWN)
        for cmd in commands:
            result = parse_command(cmd)
            assert result in ['SMART_ARRAY', 'HARD_SURFACE', 'SOLIDIFY', 'SYMMETRIZE', 'UNKNOWN']


class TestMultipleKeywords:
    """Test commands containing multiple workflow keywords."""
    
    def test_command_with_two_keywords(self):
        """Test command containing keywords for two different workflows."""
        from copilot.utils.command_parser import parse_command
        
        # Contains both "array" and "mirror"
        result = parse_command("create an array and then mirror it")
        
        # Should return one of them consistently (first match priority)
        assert result in ['SMART_ARRAY', 'SYMMETRIZE']
    
    def test_command_with_all_keywords(self):
        """Test command containing keywords from all workflows."""
        from copilot.utils.command_parser import parse_command
        
        mega_command = "array hard-surface mirror curve solidify shrinkwrap"
        result = parse_command(mega_command)
        
        # Should return first matching workflow
        assert result != 'UNKNOWN'


class TestBareKeywords:
    """Test commands that are just the keyword alone."""
    
    def test_single_word_commands(self):
        """Test single-word workflow triggers."""
        from copilot.utils.command_parser import parse_command
        
        test_cases = [
            ("array", 'SMART_ARRAY'),
            ("solidify", 'SOLIDIFY'),
            ("mirror", 'SYMMETRIZE'),
            ("shrinkwrap", 'SHRINKWRAP'),
        ]
        
        for command, expected in test_cases:
            result = parse_command(command)
            assert result == expected, f"'{command}' should parse to {expected}"


class TestNearMisses:
    """Test commands that are almost valid but not quite."""
    
    def test_typos_one_char_off(self):
        """Test common typos that are one character different."""
        from copilot.utils.command_parser import parse_command
        
        typos = [
            "aray",  # array missing 'r'
            "mirro",  # mirror missing 'r'
            "solidfy",  # solidify missing 'i'
        ]
        
        for typo in typos:
            result = parse_command(typo)
            # Should return UNKNOWN (no fuzzy matching in spec)
            assert result == 'UNKNOWN'


class TestEmptyAndWhitespace:
    """Test edge cases with empty or whitespace-only commands."""
    
    def test_empty_string(self):
        """Test completely empty command."""
        from copilot.utils.command_parser import parse_command
        
        result = parse_command("")
        assert result == 'UNKNOWN'
    
    def test_only_whitespace(self):
        """Test command with only whitespace."""
        from copilot.utils.command_parser import parse_command
        
        result = parse_command("     \t\n   ")
        assert result == 'UNKNOWN'
    
    def test_only_punctuation(self):
        """Test command with only punctuation."""
        from copilot.utils.command_parser import parse_command
        
        result = parse_command("!@#$%^&*()")
        assert result == 'UNKNOWN'


class TestCommandHistoryPatterns:
    """Test patterns users might use from command history."""
    
    def test_command_with_previous_result(self):
        """Test command that includes feedback from previous execution."""
        from copilot.utils.command_parser import parse_command
        
        # User might copy/paste including the result message
        command = "solidify (thickness: 0.01m)"
        result = parse_command(command)
        
        assert result == 'SOLIDIFY'
    
    def test_command_with_error_message(self):
        """Test command that accidentally includes an error message."""
        from copilot.utils.command_parser import parse_command
        
        command = "array - Please select an object first"
        result = parse_command(command)
        
        assert result == 'SMART_ARRAY'


class TestCaseVariations:
    """Test various case combinations."""
    
    def test_all_caps(self):
        """Test all uppercase commands."""
        from copilot.utils.command_parser import parse_command
        
        commands = [
            "CREATE AN ARRAY",
            "HARD-SURFACE",
            "SYMMETRIZE",
        ]
        
        expected = ['SMART_ARRAY', 'HARD_SURFACE', 'SYMMETRIZE']
        
        for cmd, exp in zip(commands, expected):
            assert parse_command(cmd) == exp
    
    def test_mixed_case(self):
        """Test mixed case variations."""
        from copilot.utils.command_parser import parse_command
        
        commands = [
            "CrEaTe ArRaY",
            "HaRd-SuRfAcE",
            "MiRrOr",
        ]
        
        expected = ['SMART_ARRAY', 'HARD_SURFACE', 'SYMMETRIZE']
        
        for cmd, exp in zip(commands, expected):
            assert parse_command(cmd) == exp


class TestNumericAndSymbolicCommands:
    """Test commands with numbers and symbols."""
    
    def test_commands_with_numbers(self):
        """Test commands that include numeric values."""
        from copilot.utils.command_parser import parse_command
        
        commands = [
            "create array of 10 copies",
            "mirror on X axis",
            "solidify with 0.5 thickness",
        ]
        
        expected = ['SMART_ARRAY', 'SYMMETRIZE', 'SOLIDIFY']
        
        for cmd, exp in zip(commands, expected):
            result = parse_command(cmd)
            assert result == exp, f"'{cmd}' should parse to {exp}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
