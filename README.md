# LSP-css

CSS, SCSS, LESS support for Sublime's LSP plugin provided through [VS Code's CSS language server](https://github.com/microsoft/vscode/tree/main/extensions/css-language-features/server).

## Installation

- Install [LSP](https://packagecontrol.io/packages/LSP) and `LSP-css` from Package Control.
  If you use Sass install [Sass](https://packagecontrol.io/packages/Sass).
  If you use Less install [LESS](https://packagecontrol.io/packages/LESS).
- Restart Sublime.

## Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-css`
- From the command palette `Preferences: LSP-css Settings`

## FAQs

- I'm getting duplicate suggestions in the completion popup.

  Sublime Text comes with a plugin that provides completions for the CSS and HTML syntaxes. This results in duplicate completions when using this package.

  To disable ST's built-in completions for CSS syntax, for example:
   - open any CSS file
   - run `Preferences: Settings - Syntax Specific` from the `Command Pallete`
   - add `"disable_default_completions": true` in the view on the right

  Repeat for other syntaxes that provide built-in completions. Same applies to third-party SASS package that provides SASS and SCSS support.

- The server exited with status code 1.

  It's probably that the `node` executable on your system is outdated.
  This plugin requires v14 as of version [1.0.9](https://github.com/sublimelsp/LSP-css/releases/tag/1.0.9).
  If your OS is incapable of using Node v14 like Windows 7, you can

  - either download and use [1.0.8](https://github.com/sublimelsp/LSP-css/releases/tag/1.0.8) manually.
  - or if you want to try the hard way, you can use Node v14 on Windows 7 on your own risk.
    See https://github.com/nodejs/node/issues/33000#issuecomment-644530517.
