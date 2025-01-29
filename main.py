from typing import Callable
import prompt
import commits

def new_filter_function(options: list[str]) -> Callable[[str, int], tuple[list[str], int]]:
    def fun(state, index):
        (new_options, new_index) = prompt.GET_FILTER_RULE(options)(state, index)
        if options[-1] not in new_options:
            new_options.append(options[-1])
        return new_options, new_index
    return fun

INCLUDE_FOOTER = True

def main():
    commit_types = commits.get_commit_types()
    (_, index) = prompt.show_with_filter(commit_types, "Select the type of change that you are committing: ")
    commit_type = commit_types[index].split(":")[0]

    scopes = commits.get_possible_scopes() + ["Create new scope from current input"]
    (text, index) = prompt.show(scopes, "Select the scope of the change that you are committing: ", on_update=new_filter_function(scopes))
    scope = scopes[index] if index != len(scopes) - 1 else text
    scope = "" if scope == "None" else f"({scope})"

    ok = False
    while not ok:
        msg = input("Select commit message: ")
        ok, msg = commits.check_commit_message(msg)
        if not ok:
            print("Invalid commit message format. Please try again or prepend '!'.")

    gitmojis = commits.get_gitmojis()
    (_, index) = prompt.show_with_filter(gitmojis, "Choose a gitmoji: ")
    gitmoji = gitmojis[index].split("-")[1].strip()

    description = input("(optional) Enter a longer description of the changes made in this commit:\n")

    if INCLUDE_FOOTER:
        footer = input("Footer information (referenced issues, breaking changes, etc.):\n")

    print(f"{commit_type}{scope}: {gitmoji} {msg}")

if __name__ == "__main__":
    main()
