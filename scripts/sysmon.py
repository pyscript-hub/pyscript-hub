import os
from datetime import timedelta

import psutil
import time
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def format_bytes(n_bytes):
    """
    Convert bytes to human-readable GB or MB.
    """

    if n_bytes > 1024**3:
        return f"{n_bytes / (1024**3):.2f} GB"
    else:
        return f"{n_bytes / (1024**2):.2f} MB"


def get_uptime():
    """
    Return system uptime as a string.
    """

    uptime_sec = time.time() - psutil.boot_time()
    return str(timedelta(seconds=int(uptime_sec)))


def make_panel():
    """
    Create the panel for CPU and RAM.
    """

    # --- CPU ---
    cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    cpu_avg = sum(cpu_percent) / len(cpu_percent)

    cpu_table = Table(box=None, show_header=False, pad_edge=False)
    cpu_table.add_row("[bold cyan]💻 CPU Usage[/bold cyan]", "")
    cpu_table.add_row("", "")
    for i, usage in enumerate(cpu_percent, start=1):
        cpu_table.add_row(f"Core {i}", f"[bold magenta]{usage:5.1f}%[/bold magenta]")
    cpu_table.add_row("", "")
    cpu_table.add_row("[cyan]Average[/cyan]", f"[bold cyan]{cpu_avg:5.1f}%[/bold cyan]")

    # --- RAM ---
    mem = psutil.virtual_memory()
    ram_table = Table(box=None, show_header=False, pad_edge=False)
    ram_table.add_row("[bold green]💾 RAM Usage[/bold green]", "")
    ram_table.add_row("", "")
    ram_table.add_row("Total:", f"{mem.total / (1024**3):.2f} GB")
    ram_table.add_row("Available:", f"{mem.available / (1024**3):.2f} GB")
    ram_table.add_row(
        "Used:", f"{mem.used / (1024**3):.2f} GB ([bold magenta]{mem.percent:.1f}%[/bold magenta])"
    )

    # --- Disk ---
    disk = psutil.disk_usage(os.path.expanduser("~"))
    disk_table = Table(box=None, show_header=False, pad_edge=False)
    disk_table.add_row("\n[bold yellow]💽 Disk Usage[/bold yellow]", "")
    disk_table.add_row("", "")
    disk_table.add_row("Total:", format_bytes(disk.total))
    disk_table.add_row("Used:", f"{format_bytes(disk.used)} ([bold magenta]{disk.percent:.1f}%[/bold magenta])   ")
    disk_table.add_row("Free:", format_bytes(disk.free))

    # --- Network ---
    net_io = psutil.net_io_counters()
    net_table = Table(box=None, show_header=False, pad_edge=False)
    net_table.add_row("\n[bold blue]🌐 Network[/bold blue]", "")
    net_table.add_row("", "")
    net_table.add_row("Sent:", format_bytes(net_io.bytes_sent))
    net_table.add_row("Recv:", format_bytes(net_io.bytes_recv))

    # --- Uptime ---
    uptime_table = Table(box=None, show_header=False, pad_edge=False)
    uptime_table.add_row("\n[bold white]⏱️  Uptime[/bold white]", "")
    uptime_table.add_row("", "")
    uptime_table.add_row("Time:", get_uptime())

    # --- Dashboard Table ---
    dashboard = Table.grid(expand=False)
    dashboard.add_row(cpu_table, ram_table)
    dashboard.add_row(disk_table, net_table)
    dashboard.add_row(uptime_table)

    panel = Panel(
        dashboard,
        title="System Monitor",
        border_style="cyan",
        padding=(1, 2),
        expand=False,
    )
    text = Text("Press ^C to exit...")
    return Group(panel, text)


def main(interval: float = 1):
    """
    Show a real time dashboard with CPU, RAM, disk usage, network and uptime information, updating every N seconds.
    """

    try:
        interval = float(interval)
    except ValueError:
        interval = 1

    try:
        with Live(make_panel(), refresh_per_second=2/interval, console=console, transient=False) as live:
            while True:
                live.update(make_panel())
                time.sleep(interval)
    except KeyboardInterrupt:
        return