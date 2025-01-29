def get_commit_types() -> list[str]:
    return [
        "feat:     A new feature",
        "fix:      A bug fix",
        "docs:     Documentation only changes",
        "style:    Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
        "refactor: A code change that neither fixes a bug nor adds a feature",
        "perf:     A code change that improves performance",
        "test:     Adding missing tests or correcting existing tests",
        "build:    Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)",
        "ci:       Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)",
        "chore:    Changes to the build process or auxiliary tools and libraries such as documentation generation",
        "revert:   Revert to a commit",
    ]

def get_possible_scopes() -> list[str]:
    return [
        "None",
        "frontend"
    ]

def check_commit_message(msg: str) -> tuple[bool, str]:
    if msg.startswith("!"):
        return True, msg[1:]
    msg = msg.strip()
    if not msg:
        return False, msg
    if msg.endswith("."):
        return False, msg
    if msg[0].isupper():
        return False, msg
    return True, msg

def get_gitmojis() -> list[str]:
    return [
        "🧪 - :test_tube: - Add a failing test",
        "✅ - :white_check_mark: - Add, update, or pass tests.",
    ]