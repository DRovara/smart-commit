"""Provides functionality for working with git commits."""

from __future__ import annotations

import git  # type: ignore[import-not-found]


def get_commit_types() -> list[str]:
    """Get a list of all possible commit types.

    Returns:
        list[str]: A list of all possible commit types.
    """
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
    """Get a list of all scopes used in previous commits.

    Returns:
        list[str]: A list of all scopes used in previous commits.
    """

    def get_scope(message: str) -> str:
        front = message.split(":")[0]
        if "(" in front and ")" in front:
            return front[front.index("(") + 1 : front.index(")")]
        return ""

    repo = git.Repo(".")
    previous_scopes = [get_scope(commit.message) for commit in repo.iter_commits()] if repo.head.is_valid() else []
    options = []
    for prev in previous_scopes:
        if not prev:
            continue
        if prev not in options:
            options.append(prev)
    return ["None", *options]


def check_commit_message(msg: str) -> tuple[bool, str]:
    """Check if a commit message is valid.

    Args:
        msg (str): The commit message to check.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating if the message is valid and the message itself.
    """
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


def get_gitmojis(filter_string: str = "", start_index: int = 0) -> list[str]:
    """Get a list of 7 gitmojis, ordered by frequency of use in previous commits.

    Args:
        filter_string (str, optional): A filter to apply to the list. Defaults to "".
        start_index (int, optional): The index to start from. Defaults to 0.

    Returns:
        list[str]: _description_
    """
    gitmoji_list = get_gitmoji_list()
    gitmoji_dict = {}
    for gm in gitmoji_list:
        key = gm.split(" - ")[1].strip()
        gitmoji_dict[key] = gm
    gitmoji_count = dict.fromkeys(gitmoji_dict.keys(), 0)
    repo = git.Repo(".")
    for commit in repo.iter_commits() if repo.head.is_valid() else []:
        message = commit.message
        if message.count(":") < 3:
            continue
        gitmoji = message.split(":")[2]
        if gitmoji != gitmoji.strip():
            continue
        gitmoji = f":{gitmoji}:"
        if gitmoji not in gitmoji_count:
            gitmoji_count[gitmoji] = 0
            gitmoji_dict[gitmoji] = f"?? - {gitmoji} - Unknown gitmoji"
        gitmoji_count[gitmoji] += 1
    gitmoji_list = list(gitmoji_dict.values())
    gitmoji_list.sort(key=lambda x: gitmoji_count[x.split(" - ")[1].strip()], reverse=True)
    gitmoji_list = [gm for gm in gitmoji_list if filter_string.lower() in gm.lower()]
    if start_index >= len(gitmoji_list):
        start_index = 0
    return gitmoji_list[start_index : start_index + 7] + ["..."]


def get_gitmoji_list() -> list[str]:
    """Get a list of all possible gitmojis.

    Returns:
        list[str]: A list of all possible gitmojis.
    """
    return [
        "🎨 - :art: - Improve structure / format of the code.",
        "⚡️ - :zap: - Improve performance.",
        "🔥 - :fire: - Remove code or files.",
        "🐛 - :bug: - Fix a bug.",
        "🚑️ - :ambulance: - Critical hotfix.",
        "✨ - :sparkles: - Introduce new features.",
        "📝 - :memo: - Add or update documentation.",
        "🚀 - :rocket: - Deploy stuff.",
        "💄 - :lipstick: - Add or update the UI and style files.",
        "🎉 - :tada: - Begin a project.",
        "✅ - :white_check_mark: - Add, update, or pass tests.",
        "🔒️ - :lock: - Fix security or privacy issues.",
        "🔐 - :closed_lock_with_key: - Add or update secrets.",
        "🔖 - :bookmark: - Release / Version tags.",
        "🚨 - :rotating_light: - Fix compiler / linter warnings.",
        "🚧 - :construction: - Work in progress.",
        "💚 - :green_heart: - Fix CI Build.",
        "⬇️ - :arrow_down: - Downgrade dependencies.",
        "⬆️ - :arrow_up: - Upgrade dependencies.",
        "📌 - :pushpin: - Pin dependencies to specific versions.",
        "👷 - :construction_worker: - Add or update CI build system.",
        "📈 - :chart_with_upwards_trend: - Add or update analytics or track code.",
        "♻️ - :recycle: - Refactor code.",
        "➕ - :heavy_plus_sign: - Add a dependency.",  # noqa: RUF001
        "➖ - :heavy_minus_sign: - Remove a dependency.",  # noqa: RUF001
        "🔧 - :wrench: - Add or update configuration files.",
        "🔨 - :hammer: - Add or update development scripts.",
        "🌐 - :globe_with_meridians: - Internationalization and localization.",
        "✏️ - :pencil2: - Fix typos.",
        "💩 - :poop: - Write bad code that needs to be improved.",
        "⏪️ - :rewind: - Revert changes.",
        "🔀 - :twisted_rightwards_arrows: - Merge branches.",
        "📦️ - :package: - Add or update compiled files or packages.",
        "👽️ - :alien: - Update code due to external API changes.",
        "🚚 - :truck: - Move or rename resources (e.g.: files, paths, routes).",
        "📄 - :page_facing_up: - Add or update license.",
        "💥 - :boom: - Introduce breaking changes.",
        "🍱 - :bento: - Add or update assets.",
        "♿️ - :wheelchair: - Improve accessibility.",
        "💡 - :bulb: - Add or update comments in source code.",
        "🍻 - :beers: - Write code drunkenly.",
        "💬 - :speech_balloon: - Add or update text and literals.",
        "🗃️ - :card_file_box: - Perform database related changes.",
        "🔊 - :loud_sound: - Add or update logs.",
        "🔇 - :mute: - Remove logs.",
        "👥 - :busts_in_silhouette: - Add or update contributor(s).",
        "🚸 - :children_crossing: - Improve user experience / usability.",
        "🏗️ - :building_construction: - Make architectural changes.",
        "📱 - :iphone: - Work on responsive design.",
        "🤡 - :clown_face: - Mock things.",
        "🥚 - :egg: - Add or update an easter egg.",
        "🙈 - :see_no_evil: - Add or update a .gitignore file.",
        "📸 - :camera_flash: - Add or update snapshots.",
        "⚗️ - :alembic: - Perform experiments.",
        "🔍️ - :mag: - Improve SEO.",
        "🏷️ - :label: - Add or update types.",
        "🌱 - :seedling: - Add or update seed files.",
        "🚩 - :triangular_flag_on_post: - Add, update, or remove feature flags.",
        "🥅 - :goal_net: - Catch errors.",
        "💫 - :dizzy: - Add or update animations and transitions.",
        "🗑️ - :wastebasket: - Deprecate code that needs to be cleaned up.",
        "🛂 - :passport_control: - Work on code related to authorization, roles and permissions.",
        "🩹 - :adhesive_bandage: - Simple fix for a non-critical issue.",
        "🧐 - :monocle_face: - Data exploration/inspection.",
        "⚰️ - :coffin: - Remove dead code.",
        "🧪 - :test_tube: - Add a failing test.",
        "👔 - :necktie: - Add or update business logic.",
        "🩺 - :stethoscope: - Add or update healthcheck.",
        "🧱 - :bricks: - Infrastructure related changes.",
        "🧑‍💻 - :technologist: - Improve developer experience.",
        "💸 - :money_with_wings: - Add sponsorships or money related infrastructure.",
        "🧵 - :thread: - Add or update code related to multithreading or concurrency.",
        "🦺 - :safety_vest: - Add or update code related to validation.",
    ]
