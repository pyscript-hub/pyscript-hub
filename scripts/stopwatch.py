import time
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()


def format_time(elapsed_time: float, numbers):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    if numbers:
        milliseconds = int((elapsed_time * 100) % 100)
        return f"{minutes:02}:{seconds:02}:{milliseconds:02}"
    else:
        milliseconds = int((elapsed_time * 1000) % 1000)
        return f"{minutes}m {seconds}s {milliseconds}ms"


def main(rate: int = 0.01, numbers: bool = False):
    """
    Run a stopwatch, updating every N milliseconds (0.01 if not specified) and displaying in a specific format.
    """

    try:
        with Live("00:00:00" if numbers else "0m 0s 0ms", auto_refresh=False, console=console) as live:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                formatted_time = format_time(elapsed_time, numbers)
                live.update(Text(formatted_time))
                live.refresh()
                time.sleep(rate)
    except KeyboardInterrupt:
        return