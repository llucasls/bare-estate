import io
import os

from bare_estate.config import Configs


toml_config = b'''
[config]
base_dir = "/home/john"
git_dir = ".local/share/bare_estate"

[[repo]]
name = "emacs"
work_tree = ".emacs.d"
'''

toml_config2 = b'''
[config]
git_dir = ".local/git"

[[repo]]
name = "neovim"
git_dir = "nvim"
'''

toml_config3 = b'''
[config]
work_tree = ".config"

[[repo]]
name = "emacs"
work_tree = "emacs"
'''


class TestConfigs:
    """Test Configs class"""

    def test_create_configs_from_file(self):
        """create a new instance from a configuration file"""

        file = io.BytesIO()
        file.write(toml_config)
        file.seek(0)

        configs = Configs(file)

        assert configs.base_dir == "/home/john"
        assert configs.git_dir == ".local/share/bare_estate"
        assert configs.work_tree == ""

        assert configs.get("emacs", "name") == "emacs"
        assert configs.get("emacs", "git_dir") == ".local/share/bare_estate/emacs"
        assert configs.get("emacs", "work_tree") == ".emacs.d"

    def test_create_configs_from_dict(self):
        """create a new instance from dictionary"""

        configs = Configs.from_dict({
            "config": {
                "base_dir": "/home/john",
                "git_dir": ".local/share/bare_estate",
            },
            "repo": [
                {"name": "neovim", "work_tree": ".config/nvim"},
                {"name": "emacs", "git_dir": "emacs", "work_tree": ".emacs.d"},
                {"name": "vim", "git_dir": "vim"},
            ]
        })

        assert configs.base_dir == "/home/john"
        assert configs.git_dir == ".local/share/bare_estate"
        assert configs.work_tree == ""

        assert configs.get("emacs").name == "emacs"
        assert configs.get("emacs").git_dir == "emacs"
        assert configs.get("emacs").work_tree == ".emacs.d"

        assert configs.get("vim").name == "vim"
        assert configs.get("vim").git_dir == "vim"
        assert configs.get("vim").work_tree == ""

        assert configs.get("neovim").name == "neovim"
        assert configs.get("neovim").git_dir == "neovim"
        assert configs.get("neovim").work_tree == ".config/nvim"

        assert configs.get("emacs", "name") == "emacs"
        assert configs.get("emacs", "git_dir") == ".local/share/bare_estate/emacs"
        assert configs.get("emacs", "work_tree") == ".emacs.d"

        assert configs.get("vim", "name") == "vim"
        assert configs.get("vim", "git_dir") == ".local/share/bare_estate/vim"
        assert configs.get("vim", "work_tree") == ""

        assert configs.get("neovim", "name") == "neovim"
        assert configs.get("neovim", "git_dir") == ".local/share/bare_estate/neovim"
        assert configs.get("neovim", "work_tree") == ".config/nvim"

    def test_concatenate_git_dir(self):
        """get git dir from repo config"""

        file = io.BytesIO()
        file.write(toml_config2)
        file.seek(0)

        configs = Configs(file)

        assert configs.get("neovim", "git_dir") == ".local/git/nvim"

    def test_concatenate_work_tree(self):
        """get work tree from repo config"""

        file = io.BytesIO()
        file.write(toml_config3)
        file.seek(0)

        configs = Configs(file)

        assert configs.get("emacs", "work_tree") == ".config/emacs"
