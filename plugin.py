import shutil
import os
import sublime

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig


package_path = os.path.dirname(__file__)
server_path = os.path.join(package_path, 'node_modules', 'vscode-css-languageserver-bin', 'cssServerMain.js')


def plugin_loaded():
    print('LSP-css: Server {} installed.'.format('is' if os.path.isfile(server_path) else 'is not' ))

    if not os.path.isdir(os.path.join(package_path, 'node_modules')):
        # install server if no node_modules
        print('LSP-css: Installing server.')
        sublime.active_window().run_command(
            "exec", {
                "cmd": [
                    "npm",
                    "install",
                    "--verbose",
                    "--prefix",
                    package_path
                ]
            }
        )
        sublime.message_dialog('LSP-css\n\nRestart sublime after the server has been installed successfully.')


def is_node_installed():
    return shutil.which('node') is not None


class LspCssPlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'lsp-css'

    @property
    def config(self) -> ClientConfig:
        return ClientConfig(
            name='lsp-css',
            binary_args=[
                'node',
                server_path,
                '--stdio'
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

    def on_start(self, window) -> bool:
        if not is_node_installed():
            sublime.status_message('Please install Node.js for the CSS Language Server to work.')
            return False
        return True

    def on_initialized(self, client) -> None:
        pass   # extra initialization here.
