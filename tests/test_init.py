from bare_estate.commands import Command
from bare_estate.config import Configs


class TestEstateInit:
    """Test estate init command"""

    def test_create_without_work_tree(self):
        """create repo without specifying work tree"""

        configs = Configs.from_dict({
            "base_dir": "/home/john",
            "git_dir": ".local/share/bare_estate",
        })
        command = Command(configs)
        action = command.parse_shell_cmd
        argv = ["init", "scripts"]
        env = {"HOME": "/home/john"}

        commands = list(command.init(action, argv, env))
        return

        assert commands[0] == [
            "git",
            "-C",
            "/home/john",
            "--git-dir=.local/share/bare_estate/scripts",
            "init",
        ]

        assert commands[1] == [
            "git",
            "-C",
            "/home/john",
            "--git-dir=.local/share/bare_estate/scripts",
            "config",
            "core.bare",
            "false",
        ]

        assert commands[2] == [
            "git",
            "-C",
            "/home/john",
            "--git-dir=.local/share/bare_estate/scripts",
            "config",
            "status.showUntrackedFiles",
            "no",
        ]

    def test_create_with_work_tree(self):
        """create repo with a custom work tree"""

        configs = Configs.from_dict({
            "base_dir": "/home/john",
            "git_dir": ".local/share/bare_estate",
            "work_tree": ".config/nvim",
        })
        command = Command(configs)
        action = command.parse_shell_cmd
        argv = ["init", "neovim"]
        env = {"HOME": "/home/john"}

        commands = list(command.init(action, argv, env))

        assert commands[0] == [
            "git",
            "-C",
            "/home/john",
            "init",
            "--separate-git-dir=.local/share/bare_estate/neovim",
            ".config/nvim",
        ]

        assert commands[1] == [
            "git",
            "-C",
            "/home/john",
            "--git-dir=.local/share/bare_estate/neovim",
            "config",
            "status.showUntrackedFiles",
            "all",
        ]
