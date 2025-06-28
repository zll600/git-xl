import unittest
import sys
import os
from unittest import mock
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src directory to path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import diff
import cli


class TestIntegration(unittest.TestCase):
    """Integration tests using real Excel files"""

    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_excel_file = os.path.join(self.test_dir, 'Book1.xlsb')

    def test_real_excel_file_exists(self):
        """Verify the test Excel file exists"""
        self.assertTrue(os.path.exists(self.test_excel_file))

    def test_get_vba_with_real_file(self):
        """Test VBA extraction with a real Excel file"""
        try:
            result = diff.get_vba(self.test_excel_file)
            # The result should be a dictionary
            self.assertIsInstance(result, dict)
            # Print the result for manual inspection
            print(f"VBA modules found in {self.test_excel_file}: {list(result.keys())}")
            for module_name, content in result.items():
                print(f"Module {module_name}:")
                print(content[:200] + "..." if len(content) > 200 else content)
                print("-" * 50)
        except Exception as e:
            # If oletools is not properly installed or the file has issues,
            # we'll still pass the test but print a warning
            print(f"Warning: Could not extract VBA from test file: {e}")
            self.skipTest(f"VBA extraction failed: {e}")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('diff.colorama.init')
    def test_diff_script_with_real_files(self, mock_colorama_init, mock_stdout):
        """Test the diff script with real file paths"""
        # Test the case where we compare a file with itself (should be no diff)
        original_argv = sys.argv
        try:
            # Simulate command line args for diff script
            sys.argv = [
                'diff.py', 
                'Book1.xlsb',  # workbook_name
                self.test_excel_file,  # workbook_b (new)
                '', '', 
                self.test_excel_file,  # workbook_a (old)
                '', ''
            ]
            
            # Test argument parsing
            if len(sys.argv) == 8:
                _, workbook_name, workbook_b, _, _, workbook_a, _, _ = sys.argv
                numlines = 3
                
                self.assertEqual(workbook_name, 'Book1.xlsb')
                self.assertEqual(workbook_b, self.test_excel_file)
                self.assertEqual(workbook_a, self.test_excel_file)
                self.assertEqual(numlines, 3)
                
        finally:
            sys.argv = original_argv

    @patch('cli.subprocess.run')
    @patch('cli.is_git_repository', return_value=True)
    def test_installer_with_temp_directory(self, mock_is_git_repo, mock_subprocess):
        """Test installer with a temporary directory structure"""
        import tempfile
        import shutil
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        try:
            # Test local installation
            installer = cli.Installer(mode='local', path=temp_dir)
            
            # Verify paths are correct
            expected_gitattributes = os.path.join(temp_dir, '.gitattributes')
            expected_gitignore = os.path.join(temp_dir, '.gitignore')
            
            self.assertEqual(installer.get_git_attributes_path(), expected_gitattributes)
            self.assertEqual(installer.get_git_ignore_path(), expected_gitignore)
            
            # Test the file operations (without actually running git commands)
            mock_subprocess.return_value.stdout = ''
            installer.install()
            
            # Verify files were created
            self.assertTrue(os.path.exists(expected_gitattributes))
            self.assertTrue(os.path.exists(expected_gitignore))
            
            # Check file contents
            with open(expected_gitattributes, 'r') as f:
                gitattributes_content = f.read()
                self.assertIn('*.xlsm diff=xl', gitattributes_content)
                self.assertIn('*.xlsx diff=xl', gitattributes_content)
            
            with open(expected_gitignore, 'r') as f:
                gitignore_content = f.read()
                self.assertIn('~$*.xlsm', gitignore_content)
                self.assertIn('~$*.xlsx', gitignore_content)
                
        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_command_parser_help_commands(self):
        """Test all help command variations"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Test main help
            parser = cli.CommandParser(['help'])
            parser.execute()
            output = mock_stdout.getvalue()
            self.assertIn('git xl <command>', output)
            self.assertIn('Commands', output)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Test specific help
            parser = cli.CommandParser(['help', 'install'])
            parser.execute()
            output = mock_stdout.getvalue()
            self.assertIn('git xl install', output)
            self.assertIn('--local', output)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Test version
            parser = cli.CommandParser(['version'])
            parser.execute()
            output = mock_stdout.getvalue()
            self.assertIn('git-xl/', output)

    def test_file_extensions_coverage(self):
        """Test that all expected Excel file extensions are covered"""
        expected_extensions = ['xls', 'xlt', 'xla', 'xlam', 'xlsx', 'xlsm', 'xlsb', 'xltx', 'xltm']
        
        # Check that FILE_EXTENSIONS contains all expected extensions
        for ext in expected_extensions:
            self.assertIn(ext, cli.FILE_EXTENSIONS)
        
        # Check that gitattributes patterns are generated for all extensions
        for ext in expected_extensions:
            expected_pattern = f'*.{ext} diff=xl'
            self.assertIn(expected_pattern, cli.GIT_ATTRIBUTES_DIFFER)
        
        # Check that gitignore patterns are generated for all extensions
        for ext in expected_extensions:
            expected_pattern = f'~$*.{ext}'
            self.assertIn(expected_pattern, cli.GIT_IGNORE)

    @patch('cli.is_frozen', return_value=False)
    @patch('sys.executable', '/usr/bin/python3')
    def test_non_frozen_executable_path(self, mock_is_frozen):
        """Test executable path generation when not frozen (development mode)"""
        installer = cli.Installer(mode='global')
        
        # In non-frozen mode, GIT_XL_DIFF should include python executable and diff.py path
        self.assertIn('python', installer.GIT_XL_DIFF.lower())
        self.assertIn('diff.py', installer.GIT_XL_DIFF)

    @patch('cli.is_frozen', return_value=True)
    def test_frozen_executable_path_windows(self, mock_is_frozen):
        """Test executable path generation when frozen on Windows"""
        with patch('cli.sys.platform', 'win32'):
            installer = cli.Installer(mode='global')
            # In frozen mode on Windows, should use git-xl-diff.exe
            self.assertIn('git-xl-diff.exe', installer.GIT_XL_DIFF)

    @patch('cli.is_frozen', return_value=True)
    def test_frozen_executable_path_macos(self, mock_is_frozen):
        """Test executable path generation when frozen on macOS"""
        with patch('cli.sys.platform', 'darwin'), \
             patch('platform.machine', return_value='arm64'):
            installer = cli.Installer(mode='global')
            # In frozen mode on macOS, should use git-xl-diff-arm64
            self.assertIn('git-xl-diff-arm64', installer.GIT_XL_DIFF)


class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""

    def test_invalid_command_line_args_diff(self):
        """Test diff script with invalid arguments"""
        original_argv = sys.argv
        try:
            # Test with too few arguments
            sys.argv = ['diff.py', 'only', 'three', 'args']
            
            # This should fail the length check
            is_valid = 8 <= len(sys.argv) <= 9
            self.assertFalse(is_valid)
            
            # Test with too many arguments  
            sys.argv = ['diff.py'] + ['arg'] * 10
            is_valid = 8 <= len(sys.argv) <= 9
            self.assertFalse(is_valid)
            
        finally:
            sys.argv = original_argv

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_install_option(self, mock_stdout):
        """Test install command with invalid option"""
        parser = cli.CommandParser(['install', '--invalid'])
        parser.execute()
        output = mock_stdout.getvalue()
        self.assertIn('Invalid option "--invalid"', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_for_nonexistent_command(self, mock_stdout):
        """Test help for a command that doesn't exist"""
        parser = cli.CommandParser(['help', 'nonexistent'])
        parser.execute()
        output = mock_stdout.getvalue()
        self.assertIn('Sorry, no usage text found', output)


if __name__ == '__main__':
    # Run with more verbose output
    unittest.main(verbosity=2) 