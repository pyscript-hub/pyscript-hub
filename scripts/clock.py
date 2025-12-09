import time
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()


def make_clock():
    dots = True

    def clock(seconds: bool = False):
        nonlocal dots
        if seconds:
            return Text(time.strftime("%H:%M:%S", time.localtime()))

        if dots:
            dots = False
            return Text(time.strftime("%H:%M", time.localtime()))
        else:
            dots = True
            return Text(time.strftime("%H %M", time.localtime()))

    return clock


def main(seconds: bool = False):
    """
    Show the clock.
    """

    clock = make_clock()
    try:
        with Live(clock(seconds), auto_refresh=False, console=console) as live:
            while True:
                live.update(clock(seconds))
                live.refresh()
                time.sleep(1)

    except KeyboardInterrupt:
        return