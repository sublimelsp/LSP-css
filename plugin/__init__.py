from __future__ import annotations

from .client import LspCssPlugin

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    # ST: listeners
    # ...
    "LspCssPlugin",
)


def plugin_loaded() -> None:
    """Executed when this plugin is loaded."""
    LspCssPlugin.register()


def plugin_unloaded() -> None:
    """Executed when this plugin is unloaded."""
    LspCssPlugin.unregister()
