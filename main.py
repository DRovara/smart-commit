from typing import Callable
import subprocess
import argparse

import prompt
import commits

def new_filter_function(options: list[str]) -> Callable[[str, int, dict[str, any]], tuple[list[str], int]]:
    def fun(state, index, tags):
        (new_options, new_index) = prompt.GET_FILTER_RULE(options)(state, index, tags)
        if options[-1] not in new_options:
            new_options.append(options[-1])
        return new_options, new_index
    return fun

def show_more_filter_function(options: list[str]) -> Callable[[str, int, dict[str, any]], tuple[list[str], int]]:
    def fun(state, index, tags):
        current_options = tags.get("options", options)
        current_selection = current_options[index]
        page = tags.get("page", 0)
        if index != 0 and current_options[index] == "...":
            page += 1
            tags["page"] = page
            index = 0
        new_options = commits.get_gitmojis(state, page * 7)
        if current_selection != "..." and current_selection in new_options:
            index = new_options.index(current_selection)
        else:
            index = 0
        tags["options"] = new_options
        return new_options, index
    return fun

def main():
    parser = argparse.ArgumentParser(description="Write correct commit messages with gitmojis with ease.")
    parser.add_argument("-a", action="store_true", help="Stage all changes automatically.")
    parser.add_argument("--footer", "-f", action="store_true", help="Include a footer in the commit message.")
    parser.add_argument("--breaking", "-b", action="store_true", help="Mark the commit as a breaking change.")
    args = parser.parse_args()
    run(args.footer, args.breaking, args.a)

def run(include_footer: bool, breaking_change: bool, stage_all: bool):
    if stage_all:
        subprocess.run(["git", "add", "."])

    commit_types = commits.get_commit_types()
    (_, index, _) = prompt.show_with_filter(commit_types, "Select the type of change that you are committing: ")
    commit_type = commit_types[index].split(":")[0]

    scopes = commits.get_possible_scopes() + ["Create new scope from current input"]
    (text, index, _) = prompt.show(scopes, "Select the scope of the change that you are committing: ", on_update=new_filter_function(scopes))
    scope = scopes[index] if index != len(scopes) - 1 else text
    scope = "" if scope == "None" else f"({scope})"

    ok = False
    while not ok:
        msg = input("Select commit message: ")
        ok, msg = commits.check_commit_message(msg)
        if not ok:
            print("Invalid commit message format. Please try again or prepend '!'.")

    gitmojis = commits.get_gitmojis()
    (_, index, gitmoji) = prompt.show(gitmojis, "Choose a gitmoji: ", on_update=show_more_filter_function(gitmojis), wrap_above=False, wrap_below=False)
    gitmoji = gitmoji.split("-")[1].strip()

    print("(optional) Enter a longer description of the changes made in this commit (empty line to exit):")
    description = prompt.multiline_input()

    if include_footer or breaking_change:
        footer = input("Footer information (referenced issues, breaking changes, etc.):\n")
    else:
        footer = ""

    breaking = "!" if breaking_change else ""

    full_message = f"{commit_type}{scope}:{breaking} {gitmoji} {msg}"
    if description:
        full_message += f"\n\n{description}"
    if footer:
        full_message += f"\n\n{footer}"

    result = subprocess.run(["git", "commit", "-m", full_message], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
    else:
        print("Commited successfully:\n", full_message, sep="")

if __name__ == "__main__":
    main()
