from LSP.plugin.core.typing import Tuple
from lsp_utils import NpmClientHandler
import os


def plugin_loaded():
    LspCssPlugin.setup()


def plugin_unloaded():
    LspCssPlugin.cleanup()


class LspCssPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "out",
        "node",
        "cssServerMain.js",
    )

    @classmethod
    def minimum_node_version(cls) -> Tuple[int, int, int]:
        # this should be aligned with VSCode's Nodejs version
        return (14, 0, 0)
