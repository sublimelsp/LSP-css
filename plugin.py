from .types import CustomDataChangedNotification
from LSP.plugin import filename_to_uri
from LSP.plugin.core.typing import List
from lsp_utils import ApiWrapperInterface, NpmClientHandler
from os import path


def plugin_loaded():
    LspCssPlugin.setup()


def plugin_unloaded():
    LspCssPlugin.cleanup()


class LspCssPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = path.join(
        server_directory,
        "css-language-features",
        "server",
        "out",
        "node",
        "cssServerNodeMain.js",
    )

    @classmethod
    def required_node_version(cls) -> str:
        return ">=14"

    def on_ready(self, api: ApiWrapperInterface) -> None:
        session = self.weaksession()
        if not session:
            return
        self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session) -> None:
        custom_data_paths = session.config.settings.get("css.customData")  # type: List[str]
        resolved_custom_data_paths = []  # type: List[str]
        for folder in session.get_workspace_folders():
            # Converting to URI as server can't handle reading the content if it's a file path.
            resolved_custom_data_paths.extend([
                filename_to_uri(path.abspath(path.join(folder.path, p))) for p in custom_data_paths
            ])
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))
