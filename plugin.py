import os
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspCssPlugin.setup()


def plugin_unloaded():
    LspCssPlugin.cleanup()


class LspCssPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'out', 'node', 'cssServerMain.js')

    @classmethod
    def install_in_cache(cls) -> bool:
        return False
