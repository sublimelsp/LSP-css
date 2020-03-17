import shutil
import os
import sublime

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, read_client_config
from lsp_utils import ServerNpmResource

PACKAGE_NAME = 'LSP-css'
SETTINGS_FILENAME = 'LSP-css.sublime-settings'
SERVER_DIRECTORY = 'vscode-css'
SERVER_BINARY_PATH = os.path.join(SERVER_DIRECTORY, 'out', 'cssServerMain.js')

server = ServerNpmResource(PACKAGE_NAME, SERVER_DIRECTORY, SERVER_BINARY_PATH)


def plugin_loaded():
    server.setup()


def plugin_unloaded():
    server.cleanup()


def is_node_installed():
    return shutil.which('node') is not None


class LspCssPlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return PACKAGE_NAME.lower()

    @property
    def config(self) -> ClientConfig:
        settings = sublime.load_settings(SETTINGS_FILENAME)
        client_configuration = settings.get('client')
        if client_configuration is None:
            client_configuration = {}

        # Calling setup() also here as this might run before `plugin_loaded`.
        # Will be a no-op if already ran.
        # See https://github.com/sublimelsp/LSP/issues/899
        server.setup()

        default_configuration = self.get_default_configuration()
        default_configuration.update(client_configuration)
        return read_client_config('lsp-css', default_configuration)

    def on_start(self, window) -> bool:
        if not is_node_installed():
            sublime.status_message('Please install Node.js for the CSS Language Server to work.')
            return False
        return True

    def on_initialized(self, client) -> None:
        pass   # extra initialization here.

    def get_default_configuration(self) -> dict:
        return {
            "enabled": True,
            "command": ['node', server.binary_path, '--stdio'],
            "languages": [
                {
                    "languageId": "css",
                    "scopes": ["source.css"],
                    "syntaxes": [
                        "Packages/CSS/CSS.sublime-syntax",
                        "Packages/CSS3/CSS3.sublime-syntax",
                    ],
                },
                {
                    "languageId": "scss",
                    "scopes": ["source.scss"],
                    "syntaxes": ["Packages/Sass/Syntaxes/SCSS.sublime-syntax"],
                },
                {
                    "languageId": "less",
                    "scopes": ["source.less"],
                    "syntaxes": ["Packages/LESS/Syntaxes/LESS.sublime-syntax"],
                },
            ],
            "initializationOptions": {
                "dataPaths": [],
            },
            "settings": {
                "css": {
                    "customData": [],
                    "completion": {
                        "triggerPropertyValueCompletion": True,
                        "completePropertyWithSemicolon": True,
                    },
                    "validate": True,
                    "lint": {
                        "compatibleVendorPrefixes": "ignore",
                        "vendorPrefix": "warning",
                        "duplicateProperties": "ignore",
                        "emptyRules": "warning",
                        "importStatement": "ignore",
                        "boxModel": "ignore",
                        "universalSelector": "ignore",
                        "zeroUnits": "ignore",
                        "fontFaceProperties": "warning",
                        "hexColorLength": "error",
                        "argumentsInColorFunction": "error",
                        "unknownProperties": "warning",
                        "validProperties": [],
                        "ieHack": "ignore",
                        "unknownVendorSpecificProperties": "ignore",
                        "propertyIgnoredDueToDisplay": "warning",
                        "important": "ignore",
                        "float": "ignore",
                        "idSelector": "ignore",
                        "unknownAtRules": "warning",
                    },
                },
                "scss": {
                    "completion": {
                        "triggerPropertyValueCompletion": True,
                        "completePropertyWithSemicolon": True,
                    },
                    "validate": True,
                    "lint": {
                        "compatibleVendorPrefixes": "ignore",
                        "vendorPrefix": "warning",
                        "duplicateProperties": "ignore",
                        "emptyRules": "warning",
                        "importStatement": "ignore",
                        "boxModel": "ignore",
                        "universalSelector": "ignore",
                        "zeroUnits": "ignore",
                        "fontFaceProperties": "warning",
                        "hexColorLength": "error",
                        "argumentsInColorFunction": "error",
                        "unknownProperties": "warning",
                        "validProperties": [],
                        "ieHack": "ignore",
                        "unknownVendorSpecificProperties": "ignore",
                        "propertyIgnoredDueToDisplay": "warning",
                        "important": "ignore",
                        "float": "ignore",
                        "idSelector": "ignore",
                        "unknownAtRules": "warning",
                    },
                },
                "less": {
                    "completion": {
                        "triggerPropertyValueCompletion": True,
                        "completePropertyWithSemicolon": True,
                    },
                    "validate": True,
                    "lint": {
                        "compatibleVendorPrefixes": "ignore",
                        "vendorPrefix": "warning",
                        "duplicateProperties": "ignore",
                        "emptyRules": "warning",
                        "importStatement": "ignore",
                        "boxModel": "ignore",
                        "universalSelector": "ignore",
                        "zeroUnits": "ignore",
                        "fontFaceProperties": "warning",
                        "hexColorLength": "error",
                        "argumentsInColorFunction": "error",
                        "unknownProperties": "warning",
                        "validProperties": [],
                        "ieHack": "ignore",
                        "unknownVendorSpecificProperties": "ignore",
                        "propertyIgnoredDueToDisplay": "warning",
                        "important": "ignore",
                        "float": "ignore",
                        "idSelector": "ignore",
                        "unknownAtRules": "warning",
                    },
                },
            },
        }
