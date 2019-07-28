import shutil
import os
import sublime
import threading
import subprocess

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig


def plugin_loaded():
    package_path = os.path.join(sublime.packages_path(), 'LSP-css')
    server_path = os.path.join(package_path, 'node_modules', 'vscode-css-languageserver-bin', 'cssServerMain.js')
    print('LSP-css: Server {} installed.'.format('is' if os.path.isfile(server_path) else 'is not' ))

    # install the node_modules if not installed
    if not os.path.isdir(os.path.join(package_path, 'node_modules')):
        # this will be called only when the plugin gets:
        # - installed for the first time,
        # - or when updated on package control
        logAndShowMessage('LSP-css: Installing server.')

        runCommand(
            onCommandDone,
            ["npm", "install", "--verbose", "--prefix", package_path]
        )


def onCommandDone():
    logAndShowMessage('LSP-css: Server installed.')


def runCommand(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        try:
            subprocess.check_call(popenArgs)
            onExit()
        except subprocess.CalledProcessError as error:
            logAndShowMessage('LSP-css: Error while installing the server.', error)
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread


def is_node_installed():
    return shutil.which('node') is not None


def logAndShowMessage(msg, additional_logs=None):
    print(msg, '\n', additional_logs) if additional_logs else print(msg)
    sublime.active_window().status_message(msg)


class LspCssPlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'lsp-css'

    @property
    def config(self) -> ClientConfig:
        package_path = os.path.join(sublime.packages_path(), 'LSP-css')
        server_path = os.path.join(package_path, 'node_modules', 'vscode-css-languageserver-bin', 'cssServerMain.js')
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
                    ["Packages/CSS/CSS.sublime-syntax", "Packages/CSS3/CSS3.sublime-syntax"]
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
