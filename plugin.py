import shutil

import sublime
import sublime_plugin
from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig

default_name = 'css'
server_package_name = 'vscode-css-languageserver-bin'

default_config = ClientConfig(
    name=default_name,
    binary_args=[
        "css-languageserver",
        "--stdio"
    ],
    tcp_port=None,
    enabled=True,
    init_options=dict(),
    settings=dict(),
    env=dict(),
    languages=[
        LanguageConfig(
            'css',
            ['source.css'],
            ["Packages/CSS/CSS.sublime-syntax"]
        ),
        LanguageConfig(
            'scss',
            ['source.scss'],
            ["Packages/Sass/Syntaxes/SCSS.sublime-syntax"]
        ),
        LanguageConfig(
            'less',
            ['source.less'],
            ['Packages/LESS/Syntaxes/LESS.sublime-syntax']
        )
    ]
)

# Dependencies that needs to be installed for the server to work
dependencies = ['node', 'css-languageserver']


def is_installed(dependency):
    return shutil.which(dependency) is not None


class LspCssSetupCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        if not is_installed('node') or not is_installed('css-languageserver'):
            return True
        return False

    def run(self):
        if not is_installed('node'):
            sublime.message_dialog(
                "Please install Node.js before running setup."
            )
            return

        if not is_installed('css-languageserver'):
            should_install = sublime.ok_cancel_dialog(
                "css-languageserver was not in the PATH.\nInstall {} globally now?".format(
                    server_package_name)
            )
            if should_install:
                self.window.run_command(
                    "exec", {
                        "cmd": [
                            "npm",
                            "install",
                            "--verbose",
                            "-g",
                            server_package_name
                        ]
                    })
        else:
            sublime.message_dialog(
                "{} is already installed".format(server_package_name)
            )


class LspCssPlugin(LanguageHandler):
    def __init__(self):
        self._name = default_name
        self._config = default_config

    @property
    def name(self) -> str:
        return self._name

    @property
    def config(self) -> ClientConfig:
        return self._config

    def on_start(self, window) -> bool:
        for dependency in dependencies:
            if not is_installed(dependency):
                sublime.status_message('Run: LSP: Setup CSS server')
                return False
        return True

    def on_initialized(self, client) -> None:
        pass   # extra initialization here.
