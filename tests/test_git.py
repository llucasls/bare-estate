from bare_estate.commands import Command
from bare_estate.config import Configs


class TestEstate:
    """Test estate generic command"""

    def test_git(self):
        """return argv"""

        configs = Configs.from_dict({
            "config": {
                "base_dir": "/home/john",
                "git_dir": ".local/share/bare_estate",
            },
            "repo": [
                {"name": "dotfiles"},
            ],
        })
        command = Command(configs)

        name = "dotfiles"
        action = command.parse_shell_cmd
        argv = ["log"]

        result = list(command.git(action, argv, name=name))

        assert result[0] == [
            "git",
            "-C",
            "/home/john",
            "--git-dir=.local/share/bare_estate/dotfiles",
            "log",
        ]
