from bare_estate.commands import Command
from bare_estate.config import Configs


class TestEstateClone:
    """Test estate clone command"""

    def test_clone(self):
        """clone repository with a custom work tree path"""

        configs = Configs.from_dict({
            "config": {
                "base_dir": "/home/john",
                "git_dir": ".local/share/bare_estate",
            }
        })
        command = Command(configs)

        action = command.parse_shell_cmd
        name = "emacs"
        url = "git@github.com:johndoe/emacs-config.git"
        work_tree = ".emacs.d"
        argv = ["clone", "-r", name, url, work_tree]
        env = {"HOME": "/home/john"}

        commands = list(command.clone(action, argv, env))

        assert commands[0] == [
            "git",
            "-C",
            "/home/john",
            "clone",
            "--separate-git-dir=.local/share/bare_estate/emacs",
            "git@github.com:johndoe/emacs-config.git",
            ".emacs.d",
        ]

    def test_clone_at_home(self):
        """clone repository into home directory"""

        configs = Configs.from_dict({
            "config": {
                "base_dir": "/home/john",
                "git_dir": ".local/share/bare_estate",
            }
        })
        command = Command(configs)

        action = command.parse_shell_cmd
        name = "bashrc"
        url = "git@github.com:johndoe/bashrc.git"
        argv = ["clone", url]
        env = {"HOME": "/home/john"}

        commands = list(command.clone(action, argv, env=env))

        assert commands[0] == [
            "git",
            "-C",
            "/home/john",
            "clone",
            "--separate-git-dir=.local/share/bare_estate/bashrc",
            "git@github.com:johndoe/bashrc.git",
        ]
