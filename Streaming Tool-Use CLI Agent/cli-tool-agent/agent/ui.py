import os
import sys

if sys.platform == "win32":
    os.system("")

R      = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
AMBER  = "\033[33m"
CYAN   = "\033[36m"
PURPLE = "\033[35m"
GREEN  = "\033[32m"
GRAY   = "\033[90m"
RED    = "\033[31m"

W = 50


def print_banner():
    print()
    print(f"  {DIM}{GRAY}{'━' * W}{R}")
    print()
    print(f"  {BOLD}{AMBER}◆  TUTOR AGENT{R}")
    print(f"  {DIM}{GRAY}{'─' * 14}{R}")
    print(f"  {DIM}Streaming Tool-Use CLI  ·  claude-sonnet-4-6{R}")
    print(f"  {DIM}Tools: get_current_time, save_note{R}")
    print()
    print(f"  {DIM}{GRAY}{'━' * W}{R}")
    print()


def print_hint():
    print(f"  {DIM}Type {R}quit{DIM} or {R}exit{DIM} to end the session.{R}")
    print()


def get_input():
    label = " You"
    dashes = "─" * (W - len(label))
    print(f"\n  {DIM}{GRAY}{dashes}{R}{CYAN}{BOLD}{label}{R}")
    return input(f"\n  {CYAN}{BOLD}❯{R}  ")


def tutor_start():
    label = " Tutor"
    dashes = "─" * (W - len(label))
    print(f"\n  {DIM}{GRAY}{dashes}{R}{AMBER}{BOLD}{label}{R}")
    print(f"\n  {AMBER}◆{R}  ", end="", flush=True)


def tutor_chunk(chunk):
    print(chunk, end="", flush=True)


def tutor_end():
    print("\n")


def tool_call(name, tool_input):
    print(f"  {DIM}{GRAY}{'┄' * W}{R}")
    print(f"  {PURPLE}{BOLD}⚙  {name}{R}")
    for k, v in tool_input.items():
        print(f"     {DIM}{k}{R} → {v}")


def tool_result(result, is_error):
    icon = f"{RED}✗" if is_error else f"{GREEN}✓"
    tag = "error" if is_error else "result"
    print(f"  {icon}  {DIM}{tag}:{R} {result}")
    print(f"  {DIM}{GRAY}{'┄' * W}{R}\n")


def print_goodbye():
    print()
    print(f"  {DIM}{GRAY}{'━' * W}{R}")
    print(f"  {DIM}Session ended. Goodbye!{R}")
    print(f"  {DIM}{GRAY}{'━' * W}{R}")
    print()
