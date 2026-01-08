# Instructions for GitHub Copilot

## Environment

- Mon environnement est sous Windows 11, avec PowerShell 7 comme shell par défaut.
- Recherche de texte dans une console: _ripgrep_ est installé et sa commande `rg` est disponible dans le terminal pour toutes les recherches de texte. N'utilise jamais la commande `grep` car il n'est pas disponible.

## Markdown Quality & Linting Rules

Always generate Markdown that complies with ['markdownlint' standards](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md).
Strictly follow these rules for every response involving Markdown:

- **MD001/heading-increment**: Headings must only increment by one level at a time.
- **MD002/first-heading-h1**: The first heading in the document must be a Level 1 heading (#).
- **MD003/heading-style**: Use the 'atx' style (starting with #) for all headings.
- **MD004/ul-style**: Use dashes (`-`) for unordered lists.
- **MD007/ul-indent**: Use an indentation of 2 spaces for nested lists.
- **MD009/no-trailing-spaces**: No trailing spaces at the end of lines.
- **MD012/no-multiple-blanks**: No consecutive blank lines.
- **MD018/no-missing-space-atx**: One space after the # in ATX-style headings.
- **MD019/no-multiple-space-atx**: Only one space after the # in ATX-style headings.
- **MD020/no-missing-space-closed-atx**: One space before the closing # in closed ATX-style headings.
- **MD021/no-multiple-space-closed-atx**: Only one space before the closing # in closed ATX-style headings.
- **MD022/blanks-around-headings**: One blank line before and after headings.
- **MD023/heading-start-left**: Headings must start at the beginning of the line (no leading spaces).
- **MD024/duplicate-heading**: No duplicate headings in the same document.
- **MD025/single-title**: Only one Level 1 heading (#) per document.
- **MD026/trailing-punctuation**: No trailing punctuation in headings.
- **MD027/no-multiple-space-blockquote**: Only one space after the `>` in blockquotes.
- **MD028/no-blanks-blockquote**: No blank lines inside blockquotes.
- **MD030/spaces-after-list-markers**: Exactly one space after list markers.
- **MD031/blanks-around-fences**: One blank line before and after fenced code blocks.
- **MD032/blanks-around-lists**: One blank line before and after lists.
- **MD033/no-inline-html**: Do not use inline HTML; use pure Markdown - Exceptions:
  - `<kbd>` is allowed for keyboard key representation.
  - `<summary>` with `<details>` are allowed for collapsible sections.
- **MD034/no-bare-urls**: Do not use bare URLs; always format them as links.
- **MD035/horizontal-rule-style**: Use three dashes (`---`) for horizontal rules.
- **MD036/no-emphasis-as-header**: Do not use emphasis (bold/italic) for headings.
- **MD037/no-space-in-emphasis**: No spaces inside emphasis markers (e.g., `*text*`, not `* text *`).
- **MD038/no-space-in-code**: No spaces inside code markers (e.g., `` `code` ``, not `` ` code ` ``).
- **MD039/no-space-in-links**: No spaces inside link text or URLs.
- **MD040/fenced-code-language**: Always specify the language for fenced code blocks.
- **MD041/first-line-heading**: The first line of the document must be a Level 1 heading (#).
- **MD047/single-trailing-newline**: End every file with a single newline character.

When writing Markdown code snippets, ensure they are also lint-clean.
