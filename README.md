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
