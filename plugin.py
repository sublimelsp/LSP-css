from LSP.plugin.core.typing import Mapping, Any, Callable
from lsp_utils import NpmClientHandler
import os


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

    def on_pre_server_command(self, command: Mapping[str, Any], done_callback: Callable[[], None]) -> bool:
        if command['command'] == 'editor.action.triggerSuggest':
            session = self.weaksession()
            if session:
                view = session.window.active_view()
                if view and view.is_valid():
                    view.run_command("auto_complete")
                    done_callback()
                    return True
        return False
