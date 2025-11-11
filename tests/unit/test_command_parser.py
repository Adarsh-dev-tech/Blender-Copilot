"""
Unit tests for command parser module.

These tests verify that natural language commands are correctly parsed
into workflow type identifiers. All tests use no Blender context (pure string parsing).

NOTE: These tests will FAIL until copilot/utils/command_parser.py is implemented.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# This import will fail until implementation exists - that's expected for TDD!
try:
    from copilot.utils.command_parser import parse_command
except ImportError:
    # Create a placeholder that will make all tests fail
    def parse_command(command_text: str) -> str:
        raise NotImplementedError("command_parser module not yet implemented")


class TestBasicCommandParsing:
    """Test basic command pattern matching for each workflow."""
    
    def test_parse_smart_array_simple(self):
        """Test simple array command patterns."""
        assert parse_command("create an array") == 'SMART_ARRAY'
        assert parse_command("make array") == 'SMART_ARRAY'
        assert parse_command("add array modifier") == 'SMART_ARRAY'
    
    def test_parse_hard_surface_simple(self):
        """Test hard-surface command patterns."""
        assert parse_command("make hard-surface") == 'HARD_SURFACE'
        assert parse_command("hard surface setup") == 'HARD_SURFACE'
        assert parse_command("apply hard-surface") == 'HARD_SURFACE'
    
    def test_parse_symmetrize_simple(self):
        """Test symmetrize/mirror command patterns."""
        assert parse_command("mirror on X") == 'SYMMETRIZE'
        assert parse_command("symmetrize") == 'SYMMETRIZE'
        assert parse_command("make symmetric") == 'SYMMETRIZE'
    
    def test_parse_curve_deform_simple(self):
        """Test curve deform command patterns."""
        assert parse_command("curve deform") == 'CURVE_DEFORM'
        assert parse_command("bend along curve") == 'CURVE_DEFORM'
        assert parse_command("deform to curve") == 'CURVE_DEFORM'
    
    def test_parse_solidify_simple(self):
        """Test solidify command patterns."""
        assert parse_command("solidify") == 'SOLIDIFY'
        assert parse_command("add thickness") == 'SOLIDIFY'
        assert parse_command("make solid") == 'SOLIDIFY'
    
    def test_parse_shrinkwrap_simple(self):
        """Test shrinkwrap command patterns."""
        assert parse_command("shrinkwrap") == 'SHRINKWRAP'
        assert parse_command("wrap to surface") == 'SHRINKWRAP'
        assert parse_command("conform to mesh") == 'SHRINKWRAP'


class TestCaseInsensitivity:
    """Test that command parsing is case-insensitive."""
    
    def test_uppercase_commands(self):
        """Test all uppercase variations."""
        assert parse_command("MAKE ARRAY") == 'SMART_ARRAY'
        assert parse_command("HARD-SURFACE") == 'HARD_SURFACE'
        assert parse_command("SYMMETRIZE") == 'SYMMETRIZE'
    
    def test_mixed_case_commands(self):
        """Test mixed case variations."""
        assert parse_command("Make Array") == 'SMART_ARRAY'
        assert parse_command("Hard-Surface") == 'HARD_SURFACE'
        assert parse_command("SoLiDiFy") == 'SOLIDIFY'
    
    def test_lowercase_commands(self):
        """Test lowercase variations."""
        assert parse_command("curve deform") == 'CURVE_DEFORM'
        assert parse_command("shrinkwrap") == 'SHRINKWRAP'


class TestUnknownCommands:
    """Test that unrecognized commands return UNKNOWN."""
    
    def test_random_text(self):
        """Test completely unrelated text."""
        assert parse_command("xyz random text") == 'UNKNOWN'
        assert parse_command("blah blah blah") == 'UNKNOWN'
        assert parse_command("asdfghjkl") == 'UNKNOWN'
    
    def test_partial_matches_insufficient(self):
        """Test that partial keyword matches don't trigger workflow."""
        # These should NOT match (too ambiguous)
        assert parse_command("arr") == 'UNKNOWN'  # Too short
        assert parse_command("hard") == 'UNKNOWN'  # Incomplete
    
    def test_typos_return_unknown(self):
        """Test that typos don't match workflows."""
        assert parse_command("aray") == 'UNKNOWN'  # Misspelled array
        assert parse_command("mirro") == 'UNKNOWN'  # Misspelled mirror
        assert parse_command("soldify") == 'UNKNOWN'  # Misspelled solidify


class TestEmptyAndWhitespace:
    """Test edge cases with empty/whitespace commands."""
    
    def test_empty_string(self):
        """Test empty command string."""
        assert parse_command("") == 'UNKNOWN'
    
    def test_whitespace_only(self):
        """Test whitespace-only commands."""
        assert parse_command("   ") == 'UNKNOWN'
        assert parse_command("\t\n") == 'UNKNOWN'
        assert parse_command("     \t  ") == 'UNKNOWN'
    
    def test_very_short_commands(self):
        """Test commands under minimum length."""
        assert parse_command("a") == 'UNKNOWN'
        assert parse_command("ab") == 'UNKNOWN'


class TestLongerCommands:
    """Test that commands with extra words still parse correctly."""
    
    def test_verbose_array_commands(self):
        """Test array commands with extra descriptive words."""
        assert parse_command("please create an array of 5 copies") == 'SMART_ARRAY'
        assert parse_command("I want to make an array modifier") == 'SMART_ARRAY'
        assert parse_command("can you add an array?") == 'SMART_ARRAY'
    
    def test_verbose_hard_surface_commands(self):
        """Test hard-surface commands with context."""
        assert parse_command("apply hard-surface setup to this object") == 'HARD_SURFACE'
        assert parse_command("make this look hard-surface with bevel") == 'HARD_SURFACE'
    
    def test_verbose_mirror_commands(self):
        """Test mirror commands with axis specification."""
        assert parse_command("mirror this on the X axis") == 'SYMMETRIZE'
        assert parse_command("I need to symmetrize along X") == 'SYMMETRIZE'


class TestSpecialCharacters:
    """Test commands with special characters and punctuation."""
    
    def test_punctuation_ignored(self):
        """Test that punctuation doesn't break parsing."""
        assert parse_command("make array!") == 'SMART_ARRAY'
        assert parse_command("hard-surface?") == 'HARD_SURFACE'
        assert parse_command("solidify.") == 'SOLIDIFY'
    
    def test_hyphens_in_commands(self):
        """Test hyphenated command variations."""
        assert parse_command("hard-surface") == 'HARD_SURFACE'
        assert parse_command("hard surface") == 'HARD_SURFACE'  # Without hyphen


class TestPriorityAndAmbiguity:
    """Test workflow priority when multiple keywords might match."""
    
    def test_first_match_priority(self):
        """Test that first matching pattern wins."""
        # If command has multiple workflow keywords, first match should win
        # This requires parser to have defined priority order
        result = parse_command("array and mirror")  # Has both keywords
        # Should return the one checked first in parser priority
        assert result in ['SMART_ARRAY', 'SYMMETRIZE']  # One of them, consistently
    
    def test_longer_patterns_preferred(self):
        """Test that longer/more specific patterns match over shorter ones."""
        # "hard-surface" should match before just "hard"
        assert parse_command("hard-surface") == 'HARD_SURFACE'


class TestParserPerformance:
    """Test that parsing is fast enough (<10ms per contract)."""
    
    def test_parsing_performance(self):
        """Test that 100 parse operations complete in <1 second."""
        import time
        
        commands = [
            "create an array",
            "make hard-surface",
            "symmetrize",
            "curve deform",
            "solidify",
            "shrinkwrap",
            "unknown command xyz",
        ]
        
        start_time = time.time()
        for _ in range(100):
            for cmd in commands:
                parse_command(cmd)
        elapsed = time.time() - start_time
        
        # 100 iterations × 7 commands = 700 parse calls
        # Should complete in well under 1 second (target: <10ms each)
        assert elapsed < 1.0, f"Parsing too slow: {elapsed:.3f}s for 700 calls"
        
        # Average per call should be <10ms
        avg_per_call = elapsed / 700
        assert avg_per_call < 0.01, f"Average parse time {avg_per_call*1000:.2f}ms exceeds 10ms target"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
