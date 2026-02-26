from __future__ import annotations

import os
from typing import final

import sublime
from LSP.plugin import ClientConfig, Session
from lsp_utils import ApiWrapperInterface, NpmClientHandler
from typing_extensions import override

from .constants import PACKAGE_NAME
from .data_types import CustomDataChangedNotification


def plugin_loaded() -> None:
    LspCssPlugin.setup()


def plugin_unloaded() -> None:
    LspCssPlugin.cleanup()


@final
class LspCssPlugin(NpmClientHandler):
    package_name = PACKAGE_NAME
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "css-language-features",
        "server",
        "out",
        "node",
        "cssServerNodeMain.js",
    )

    @override
    @classmethod
    def required_node_version(cls) -> str:
        return ">=14"

    @override
    @classmethod
    def is_applicable(cls, view: sublime.View, config: ClientConfig) -> bool:
        return bool(
            super().is_applicable(view, config)
            # REPL views (https://github.com/sublimelsp/LSP-pyright/issues/343)
            and not view.settings().get("repl")
        )

    @override
    def on_ready(self, api: ApiWrapperInterface) -> None:
        if not (session := self.weaksession()):
            return
        self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths: list[str] = session.config.settings.get("css.customData")
        resolved_custom_data_paths: list[str] = []
        for folder in session.get_workspace_folders():
            # Converting to URI as server can't handle reading the content if it's a file path.
            resolved_custom_data_paths.extend(os.path.abspath(os.path.join(folder.path, p)) for p in custom_data_paths)
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))
