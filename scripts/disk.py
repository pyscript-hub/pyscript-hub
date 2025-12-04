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
    Builds a Rich table displaying disk usage info.
    """

    partitions = psutil.disk_partitions(all=False)

    table = Table(box=None, show_header=True, header_style="bold cyan")
    table.add_column("Mount", style="bold white", no_wrap=True)
    table.add_column("Filesystem", style="dim")
    table.add_column("Used", justify="right")
    table.add_column("Free", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Usage", justify="center")

    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            # Alcuni mount point possono non essere accessibili
            continue

        used_gb = usage.used / (1024**3)
        free_gb = usage.free / (1024**3)
        total_gb = usage.total / (1024**3)
        percent = usage.percent

        # Bar color dinamico in base al livello di utilizzo
        if percent < 60:
            color = "green"
        elif percent < 85:
            color = "yellow"
        else:
            color = "red"

        # Creiamo una mini progress bar inline (testuale)
        bar = f"[{color}]{'█' * int(percent / 10)}[dim]{'░' * (10 - int(percent / 10))}[/dim][/{color}]"

        table.add_row(
            f"{part.mountpoint}",
            f"{part.fstype or '-'}",
            f"{used_gb:5.1f} GB",
            f"{free_gb:5.1f} GB",
            f"{total_gb:5.1f} GB",
            f"{percent:5.1f}% {bar}",
        )

    panel = Panel(
        table,
        title="Disk Usage",
        border_style="cyan",
        padding=(0, 1),
        expand=False,
    )
    return panel


def make_group():
    """
    Get final renderable object.
    """

    table = make_table()
    text = Text("Press ^C to exit...")
    return Group(table, text)


def main(interval: float = 0):
    """
    Show disk usage for all partitions, refreshing every N seconds.
    """

    try:
        interval = float(interval)
    except ValueError:
        interval = 0

    if interval == 0:
        console.print(make_table())
        return

    try:
        with Live(make_table(), refresh_per_second=2/interval, console=console, transient=False) as live:
            while True:
                live.update(make_group())
                time.sleep(interval)
    except KeyboardInterrupt:
        return