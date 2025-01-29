from typing import Callable
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

INCLUDE_FOOTER = False

def main():
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

    description = input("(optional) Enter a longer description of the changes made in this commit:\n")

    if INCLUDE_FOOTER:
        footer = input("Footer information (referenced issues, breaking changes, etc.):\n")
    else:
        footer = ""

    print(f"{commit_type}{scope}: {gitmoji} {msg}")

if __name__ == "__main__":
    main()
