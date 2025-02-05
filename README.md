# smart-commit

`smart-commit` is a CLI-based git commit automation tool that helps you follow the _Conventional Commits_ specification.

The main features include:

- automatic generation of commit messages based on the _Conventional Commits_ specification with gitmoji support.
- filter functions to find your desired commit types, scopes, and gitmojis.
- sorting methods to give you your most commonly/recently used gitmojis and scopes right away.
- commit message validation to ensure your commit messages are formatted correctly.
- a simple and easy-to-use interface.
- a customisable configuration file to suit your needs.

`smart-commit` is designed to help you write better commit messages and make your git history more readable and understandable with the least amount of effort.

## Installation

To install `smart-commit`, you can use the following command:

```bash
pipx install smart-commit
```

This installs the `smart-commit` python application (requires Python 3.10 or later) and makes it available as a command-line tool.

## Usage

To use `smart-commit`, you can run the following command:

```bash
smart-commit
```

This will open the `smart-commit` CLI interface where you can customise your commit message.
Starting `smart-commit` with the `-a` flag additionally stages all modified files for the commit.

If you wish to include a footer in your commit message, use the flag `--footer` (or enable it by default in the configuration file).

To mark breaking changes in your commit message, use the flag `--breaking`.

## Configuration

`smart-commit` uses a configuration file to store your preferences. A configuration file can be stored locally
for your project at `.smart-commit-config.yaml` or globally in your user-config directory (`/home/username/.config/smart-commit/config.yaml` for Linux, or `C:\Users\username\AppData\Roaming\smart-commit\config.yaml` for Windows).

An example configuration file that shows off all supported settings is as follows:

```yaml
types:
  exclude:
    - chore
    - revert
  add:
    - name: my-commit-type
      description: My custom commit type
    - name: my-other-commit-type
      description: My other custom commit type
  priority:
    - feat
    - my-commit-type
    - my-other-commit-type

scopes:
  exclude:
    - deps
    - '#\d+'
  add:
    - my-new-scope
  prohibit-no-scope: true

message:
  custom-pattern: '^\w+\.'

gitmojis:
  exclude:
    - art
    - fire
  add:
    - icon: 🎨
      name: my-gitmoji
      description: My custom gitmoji.
    - icon: 🔥
      name: my-gitmoji-2
      description: My custom gitmoji number 2.
  priority:
    - sparkles
    - my-gitmoji
    - my-gitmoji-2

always-enable-footer: true
```
