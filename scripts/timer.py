import time
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()


def format_time(remaining_time: float):
    if remaining_time < 0:
        remaining_time = 0

    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    milliseconds = int((remaining_time * 100) % 100)

    return f"{minutes:02}:{seconds:02}:{milliseconds:02}"


def main(seconds: int, end_message: Optional[str] = None, rate: float = 0.01):
    """
    Run a countdown timer of N seconds, updating every M seconds (default 0.01), optionally showing an end message.
    """

    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    # Initial display
    initial_text = f"{hours:02}:{minutes:02}:{secs:02}"

    final_msg = end_message if end_message else "⏱️  Time's up!"

    try:
        with Live(initial_text, auto_refresh=False, console=console) as live:
            start_time = time.time()

            while True:
                elapsed = time.time() - start_time
                remaining = total_seconds - elapsed

                # Stop at zero
                if remaining <= 0:
                    live.update(Text(format_time(0)))
                    live.refresh()
                    break

                formatted_time = format_time(remaining)
                live.update(Text(formatted_time))
                live.refresh()
                time.sleep(rate)

    except KeyboardInterrupt:
        return

    console.print(f"\n[bold green]{final_msg}[/bold green]")