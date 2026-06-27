from agent.loop import agent_turn
from agent.messages import add_user_message
from agent import ui


def main():
    ui.print_banner()
    ui.print_hint()
    messages = []

    while True:
        user_input = ui.get_input().strip()
        if user_input.lower() in ("quit", "exit"):
            ui.print_goodbye()
            break
        if not user_input:
            continue
        add_user_message(messages, user_input)
        agent_turn(messages)


if __name__ == "__main__":
    main()
