import psutil
from rich.console import Console, Group
import time

from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

def make_table():
    """
    Builds a Rich table displaying ram usage info.
    """

    mem = psutil.virtual_memory()

    table = Table(box=None, show_header=False)
    table.add_row("Total", f"{mem.total / (1024**3):.2f} GB")
    table.add_row("Available", f"{mem.available / (1024**3):.2f} GB ([bold magenta]{mem.percent:.1f}%[/bold magenta])")
    table.add_row("Used", f"{mem.used / (1024**3):.2f} GB ([bold magenta]{mem.percent:.1f}%[/bold magenta])")
    panel = Panel(
        table,
        title="RAM Usage",
        border_style="cyan",
        expand=False,
        padding=(0, 0),
    )
    return panel


def make_group():
    """
    Get final renderable element.
    """

    table = make_table()
    text = Text("Press ^C to exit...")
    return Group(table, text)

def main(interval: float = 0):
    """
    Show RAM usage, updating every N seconds if specified.
    """

    try:
        interval = float(interval)
    except ValueError:
        interval = 0

    if interval == 0:
        console.print(make_table())
        return

    try:
        with Live(make_group(), refresh_per_second=2/interval, console=console, transient=False) as live:
            while True:
                live.update(make_group())
                time.sleep(interval)
    except KeyboardInterrupt:
        return