import psutil
import time
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def make_table():
    """
    Builds a Rich table displaying cpu usage info.
    """

    cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    avg = sum(cpu_percent) / len(cpu_percent)

    table = Table(box=None, show_header=False)

    # Righe per ogni core
    for i, usage in enumerate(cpu_percent, start=1):
        table.add_row(f"Core {i}", f"[bold magenta]{usage:5.1f}%[/bold magenta]")

    # Riga per la media totale
    table.add_row("", "")
    table.add_row("[cyan]Average[/cyan]", f"[bold cyan]{avg:5.1f}%[/bold cyan]")

    panel = Panel(
        table,
        title="CPU Usage",
        border_style="cyan",
        expand=False,
        padding=(0, 0),
    )
    text = Text("Press ^C to exit...")
    return Group(panel, text)


def main(interval: float = 1):
    """
    Show CPU usage, updating every N seconds (or 1 if not specified).
    """

    try:
        interval = float(interval)
    except ValueError:
        interval = 1

    if interval <= 0:
        interval = 1

    try:
        with Live(make_table(), refresh_per_second=2/interval, console=console, transient=False) as live:
            while True:
                live.update(make_table())
                time.sleep(interval)
    except KeyboardInterrupt:
        return