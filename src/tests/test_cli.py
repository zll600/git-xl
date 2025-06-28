import cli
from io import StringIO
from unittest import TestCase, mock
from unittest.mock import call
import os
import sys
import platform


class TestLocalInstaller(TestCase):

    @mock.patch('cli.is_git_repository', return_value=True)
    def test_paths(self, mock_is_git_repository):
        test_path = os.path.join('path', 'to', 'repository')
        installer = cli.Installer(mode='local', path=test_path)
        expected_gitattributes = os.path.join(test_path, '.gitattributes')
        expected_gitignore = os.path.join(test_path, '.gitignore')
        
        self.assertEqual(installer.get_git_attributes_path(), expected_gitattributes)
        self.assertEqual(installer.get_git_ignore_path(), expected_gitignore)

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_frozen', return_value=True)
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=False)
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_install_when_files_do_not_exist_frozen(self, mock_file_open, mock_path_exists,
                                                 mock_is_git_repository, mock_is_frozen, mock_run):
        test_path = os.path.join('path', 'to', 'repository')
        installer = cli.Installer(mode='local', path=test_path)
        installer.install()
        
        # Should call git config with some executable
        self.assertTrue(mock_run.called)
        call_args = mock_run.call_args[0][0]
        self.assertEqual(call_args[:3], ['git', 'config', 'diff.xl.command'])
        
        gitattributes_path = os.path.join(test_path, '.gitattributes')
        gitignore_path = os.path.join(test_path, '.gitignore')
        
        # Verify files are created
        mock_file_open.assert_any_call(gitattributes_path, 'w')
        mock_file_open.assert_any_call(gitignore_path, 'w')

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_frozen', return_value=True)
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=True)
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something\n')
    def test_can_install_when_files_exist(self, mock_file_open, mock_path_exists,
                                          mock_is_git_repository, mock_is_frozen, mock_run):
        test_path = os.path.join('path', 'to', 'repository')
        installer = cli.Installer(mode='local', path=test_path)
        installer.install()
        
        # Check that subprocess was called (exact command varies by platform)
        self.assertTrue(mock_run.called)
        
        gitattributes_path = os.path.join(test_path, '.gitattributes')
        gitignore_path = os.path.join(test_path, '.gitignore')
        
        # Verify files were opened for reading and writing
        mock_file_open.assert_any_call(gitattributes_path, 'r')
        mock_file_open.assert_any_call(gitattributes_path, 'w')
        mock_file_open.assert_any_call(gitignore_path, 'r')
        mock_file_open.assert_any_call(gitignore_path, 'w')

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=False)
    @mock.patch('cli.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_uninstall_when_files_do_not_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        test_path = os.path.join('path', 'to', 'repository')
        installer = cli.Installer(mode='local', path=test_path)
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd=test_path, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        mock_os_remove.assert_has_calls([])

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.is_git_repository', return_value=True)
    @mock.patch('cli.os.path.exists', return_value=True)
    @mock.patch('cli.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something')
    def test_can_uninstall_when_files_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        test_path = os.path.join('path', 'to', 'repository')
        installer = cli.Installer(mode='local', path=test_path)
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd=test_path, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        self.assertEqual(mock_os_remove.call_count, 0)
        
        gitattributes_path = os.path.join(test_path, '.gitattributes')
        
        # Verify gitattributes file was opened for reading and writing multiple times
        calls = [call_obj for call_obj in mock_file_open.call_args_list if call_obj[0][0] == gitattributes_path]
        read_calls = [call_obj for call_obj in calls if len(call_obj[0]) > 1 and 'r' in call_obj[0][1]]
        write_calls = [call_obj for call_obj in calls if len(call_obj[0]) > 1 and 'w' in call_obj[0][1]]
        
        # Should have at least 2 read and 2 write operations for gitattributes
        self.assertGreaterEqual(len(read_calls), 2)
        self.assertGreaterEqual(len(write_calls), 2)


class TestGlobalInstaller(TestCase):

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.Installer.get_git_attributes_path')
    @mock.patch('cli.Installer.get_git_ignore_path')
    def test_global_gitconfig_dir(self, mock_get_git_ignore_path, mock_get_git_attributes_path, mock_run):
        installer = cli.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_has_calls([
            mock.call(['git', 'config', '--global', '--list', '--show-origin'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8'),
            mock.call(['git', 'config', '--global', '--list'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')
        ])

    @mock.patch('cli.subprocess.run')
    @mock.patch('cli.Installer.get_global_gitconfig_dir')
    @mock.patch('cli.Installer.get_git_ignore_path')
    def test_global_gitattributes_path(self, mock_get_git_ignore_path, get_global_gitconfig_dir, mock_run):
        mock_completed_process = mock.Mock()
        mock_completed_process.configure_mock(**{'stdout': '.gitconfig'})
        mock_run.return_value = mock_completed_process
        installer = cli.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_once_with(['git', 'config', '--global', '--get', 'core.attributesfile'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True, encoding='utf-8')


class TestHelp(TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_generic_help(self, mock_stdout):
        command_parser = cli.CommandParser(['help'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_GENERIC + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_install(self, mock_stdout):
        command_parser = cli.CommandParser(['help', 'install'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_INSTALL + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_uninstall(self, mock_stdout):
        command_parser = cli.CommandParser(['help', 'uninstall'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.HELP_UNINSTALL + '\n')


class TestCommandParser(TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        command_parser = cli.CommandParser(['version'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), cli.GIT_XL_VERSION + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_env(self, mock_stdout):
        command_parser = cli.CommandParser(['env'])
        command_parser.execute()
        self.assertTrue(mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_unknown_command(self, mock_stdout):
        command_parser = cli.CommandParser(['unknown_command'])
        command_parser.execute()
        output = mock_stdout.getvalue()
        self.assertIn('Error: unknown command "unknown_command"', output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_install_command_local(self, mock_stdout):
        with mock.patch('cli.Installer') as mock_installer_class:
            mock_installer = mock.Mock()
            mock_installer_class.return_value = mock_installer
            
            command_parser = cli.CommandParser(['install', '--local'])
            command_parser.execute()
            
            mock_installer_class.assert_called_once_with(mode='local', path=os.getcwd())
            mock_installer.install.assert_called_once()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_install_command_global(self, mock_stdout):
        with mock.patch('cli.Installer') as mock_installer_class:
            mock_installer = mock.Mock()
            mock_installer_class.return_value = mock_installer
            
            command_parser = cli.CommandParser(['install'])
            command_parser.execute()
            
            mock_installer_class.assert_called_once_with(mode='global')
            mock_installer.install.assert_called_once()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_uninstall_command_local(self, mock_stdout):
        with mock.patch('cli.Installer') as mock_installer_class:
            mock_installer = mock.Mock()
            mock_installer_class.return_value = mock_installer
            
            command_parser = cli.CommandParser(['uninstall', '--local'])
            command_parser.execute()
            
            mock_installer_class.assert_called_once_with(mode='local', path=os.getcwd())
            mock_installer.uninstall.assert_called_once()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_uninstall_command_global(self, mock_stdout):
        with mock.patch('cli.Installer') as mock_installer_class:
            mock_installer = mock.Mock()
            mock_installer_class.return_value = mock_installer
            
            command_parser = cli.CommandParser(['uninstall'])
            command_parser.execute()
            
            mock_installer_class.assert_called_once_with(mode='global')
            mock_installer.uninstall.assert_called_once()


class TestInstallerValidation(TestCase):
    """Test installer validation logic"""

    def test_global_mode_with_path_raises_error(self):
        with self.assertRaises(ValueError) as context:
            cli.Installer(mode='global', path='/some/path')
        self.assertIn('must not specify repository path', str(context.exception))

    def test_local_mode_without_path_raises_error(self):
        with self.assertRaises(ValueError) as context:
            cli.Installer(mode='local', path=None)
        self.assertIn('must specify repository path', str(context.exception))

    @mock.patch('cli.is_git_repository', return_value=False)
    def test_local_mode_with_non_git_repo_raises_error(self, mock_is_git_repo):
        with self.assertRaises(ValueError) as context:
            cli.Installer(mode='local', path='/not/a/git/repo')
        self.assertIn('not a Git repository', str(context.exception))

    @mock.patch('cli.is_git_repository', return_value=True)
    def test_valid_local_installer_creation(self, mock_is_git_repo):
        installer = cli.Installer(mode='local', path='/valid/git/repo')
        self.assertEqual(installer.mode, 'local')
        self.assertEqual(installer.path, '/valid/git/repo')

    def test_valid_global_installer_creation(self):
        installer = cli.Installer(mode='global')
        self.assertEqual(installer.mode, 'global')
        self.assertIsNone(installer.path)


class TestUtilityFunctions(TestCase):
    """Test utility functions"""

    def test_is_frozen_when_not_frozen(self):
        # In test environment, sys.frozen should not exist
        result = cli.is_frozen()
        self.assertFalse(result)

    @mock.patch('cli.subprocess.run')
    def test_is_git_repository_true(self, mock_run):
        mock_run.return_value.stderr = ''
        result = cli.is_git_repository('/path/to/git/repo')
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ['git', 'rev-parse'], 
            cwd='/path/to/git/repo', 
            stdout=mock.ANY, 
            stderr=mock.ANY,
            universal_newlines=True, 
            encoding='utf-8'
        )

    @mock.patch('cli.subprocess.run')
    def test_is_git_repository_false(self, mock_run):
        mock_run.return_value.stderr = 'fatal: not a git repository'
        result = cli.is_git_repository('/path/to/not/git/repo')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

