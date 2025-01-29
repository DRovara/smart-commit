from typing import Callable
import termios, tty, sys, os

COLOUR_YELLOW = "\033[33m"
STYLE_BOLD = "\033[1m"
COLOUR_RESET = "\033[0m"

def GET_FILTER_RULE(options: list[str]) -> Callable[[str, int, dict[str, any]], tuple[list[str], int]]:
    def fun(state, index, _tags):
        old_item = options[index]
        filtered = [option for option in options if state.lower() in option.lower()]
        index = filtered.index(old_item) if old_item in filtered else 0
        return filtered, index
    return fun

def getchar():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
                if k in [65, 66, 67, 68]:
                    k += 100
            else:
                k = ord(b)
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: ' ',
                9: 'tab',
                27: 'esc',
                165: 'up',
                166: 'down',
                167: 'right',
                168: 'left'
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def show(options: list[str], header: str, allow_keys: bool = True, on_update: Callable[[str, int, dict[str, any]], tuple[list[str], int]] = None, wrap_above: bool = True, wrap_below: bool = True) -> tuple[str, int, str]:
    state = ""
    running = True
    index = 0
    last_options = options
    original_options = options
    tags: dict[str, any] = {}

    def print_state():
        print(header + state)
        for i, option in enumerate(options):
            pre = f"{COLOUR_YELLOW}{STYLE_BOLD} » " if i == index else "   "
            print(f"{pre}{option}{COLOUR_RESET}")

    def refresh():
        reset_sequence = "\r                    " #"\r\033[K"
        print("\r\033[K", flush=True)
        for _ in last_options:
            print("\r\033[K", flush=True)
        for _ in range(len(last_options) + 1):
            print(f"\033[F", end="", flush=True)
    
    def return_caret():
        for _ in range(len(options) + 1):
            print(f"\033[F", end="", flush=True)
        print(f"\033[{len(header) + len(state)}C", end="", flush=True)

    def hide_cursor():
        print(f"\033[?25l", end="", flush=True)

    def show_cursor():
        print(f"\033[?25h", end="", flush=True)

    print_state()
    if allow_keys:
        return_caret()

    try:
        while running:
            if not allow_keys:
                return_caret()
            refresh()
            print_state()
            if allow_keys:
                return_caret()
            else:
                hide_cursor()
            last_options = options

            key = getchar()
            if len(key) == 1 and allow_keys:
                state += key
            elif key == "backspace":
                state = state[:-1]
            elif key == "up":
                index -= 1
                if index < 0:
                    index = 0 if not wrap_above else len(options) - 1
            elif key == "down":
                index += 1
                if index >= len(options):
                    index = len(options) - 1 if not wrap_below else 0
            elif key == "return":
                running = False
                show_cursor()
            else:
                continue

            if on_update:
                options, index = on_update(state, index, tags)
            if len(options) == 0:
                options = ["---"]
            if index < 0 or index >= len(options):
                index = 0
    except:
        show_cursor()
        if not allow_keys:
            return_caret()
        refresh()
        raise

    if not allow_keys:
        return_caret()
    refresh()
    print(header + f"{STYLE_BOLD}" + options[index] + f"{COLOUR_RESET}")
        
    if options[index] in original_options:
        index = original_options.index(options[index])
    return state, index, options[index]

def show_with_filter(options: list[str], header: str) -> tuple[str, int, str]:
    return show(options, header, True, GET_FILTER_RULE(options))

def multiline_input() -> str:
    result = ""
    first = True
    while True:
        line = input()
        if not line:
            break
        if not first:
            result += "\n"
        first = False
        result += line
    return result