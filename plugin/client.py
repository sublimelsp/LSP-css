from __future__ import annotations

from pathlib import Path
from typing import final

from LSP.plugin import LspPlugin, OnPreStartContext, Session
from lsp_utils import NodeManager
from sublime_lib import ResourcePath
from typing_extensions import override

from .data_types import CustomDataChangedNotification


@final
class LspCssPlugin(LspPlugin):
    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath("Packages", package_name, "language-server"),
            Path("css-language-features", "server", "out", "node", "cssServerNodeMain.js"),
            node_version_requirement=">=14",
        )

    @override
    def on_initialized_async(self) -> None:
        if session := self.weaksession():
            self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths: list[str] = session.config.settings.get("css.customData")
        resolved_custom_data_paths: list[str] = []
        for folder in session.get_workspace_folders():
            # Converting to URI as server can't handle reading the content if it's a file path.
            resolved_custom_data_paths.extend(str(Path(folder.path, p).absolute()) for p in custom_data_paths)
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))
