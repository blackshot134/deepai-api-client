import asyncio
import sys
import os
from deepai_client import DeepAIClient
from config import USE_COLORS, SHOW_THINKING

if USE_COLORS:
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        C_USER = Fore.CYAN
        C_BOT = Fore.GREEN
        C_ERR = Fore.RED
        C_INFO = Fore.YELLOW
        C_DIM = Style.DIM
        C_RESET = Style.RESET_ALL
    except ImportError:
        C_USER = C_BOT = C_ERR = C_INFO = C_DIM = C_RESET = ""
else:
    C_USER = C_BOT = C_ERR = C_INFO = C_DIM = C_RESET = ""


def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{C_BOT}{'=' * 55}")
    print(f"{C_BOT}   DeepAI Chat  -  Terminal Edition")
    print(f"{C_BOT}{'=' * 55}{C_RESET}")
    print(f"{C_INFO}Special commands:{C_RESET}")
    print(f"  {C_DIM}/exit{C_RESET}     -> Quit")
    print(f"  {C_DIM}/clear{C_RESET}    -> Clear history")
    print(f"  {C_DIM}/img{C_RESET}      -> Generate image (e.g. /img a space cat)")
    print(f"  {C_DIM}/help{C_RESET}     -> Show help")
    print(f"{C_BOT}{'=' * 55}{C_RESET}\n")


async def show_thinking(stop_event: asyncio.Event):
    frames = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{C_INFO}{frames[i % len(frames)]} DeepAI is thinking...{C_RESET}")
        sys.stdout.flush()
        i += 1
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=0.1)
        except asyncio.TimeoutError:
            pass
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()


async def main():
    client = DeepAIClient()
    print_banner()

    try:
        while True:
            try:
                user_input = input(f"{C_USER}You:{C_RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{C_INFO}Goodbye!{C_RESET}")
                break

            if not user_input:
                continue

            if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
                print(f"{C_INFO}Goodbye!{C_RESET}")
                break

            if user_input.lower() == "/clear":
                await client.clear_history()
                print(f"{C_INFO}History cleared.{C_RESET}\n")
                continue

            if user_input.lower() == "/help":
                print_banner()
                continue

            if user_input.lower().startswith("/img "):
                prompt = user_input[5:].strip()
                if not prompt:
                    print(f"{C_ERR}Please provide a description after /img.{C_RESET}\n")
                    continue
                print(f"{C_INFO}Generating image...{C_RESET}")
                url = await client.generate_image(prompt)
                print(f"{C_BOT}Image:{C_RESET} {url}\n")
                continue

            stop_event = asyncio.Event()
            thinking_task = None
            if SHOW_THINKING:
                thinking_task = asyncio.create_task(show_thinking(stop_event))

            try:
                answer = await client.chat(user_input)
            finally:
                stop_event.set()
                if thinking_task:
                    await thinking_task

            print(f"{C_BOT}DeepAI:{C_RESET} {answer}\n")

    finally:
        await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{C_INFO}Goodbye!{C_RESET}")