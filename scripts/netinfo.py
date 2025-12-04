import psutil
import time
import socket
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def make_table(prev_counters=None, interval=1.0):
    """
    Build a Rich table with network interface data.
    If prev_counters is provided, shows throughput (bytes/sec).
    """

    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    counters = psutil.net_io_counters(pernic=True)

    table = Table(box=None, show_header=True, header_style="bold cyan")
    table.add_column("Interface", style="bold white")
    table.add_column("Status", justify="center")
    table.add_column("IPv4", style="cyan")
    table.add_column("IPv6", style="dim")
    table.add_column("Sent", justify="right")
    table.add_column("Recv", justify="right")
    table.add_column("↑ Speed", justify="right")
    table.add_column("↓ Speed", justify="right")

    for iface, iface_addrs in addrs.items():
        stat = stats.get(iface)
        if not stat:
            continue

        ipv4 = next((a.address for a in iface_addrs if a.family == socket.AF_INET), "-")
        ipv6 = next((a.address for a in iface_addrs if a.family == socket.AF_INET6), "-")

        iface_counters = counters.get(iface)
        if not iface_counters:
            continue

        sent_mb = iface_counters.bytes_sent / (1024**2)
        recv_mb = iface_counters.bytes_recv / (1024**2)

        # Calculate speed difference since last check
        if prev_counters and iface in prev_counters:
            prev = prev_counters[iface]
            sent_speed = (iface_counters.bytes_sent - prev.bytes_sent) / interval
            recv_speed = (iface_counters.bytes_recv - prev.bytes_recv) / interval
        else:
            sent_speed = recv_speed = 0.0

        # Format speed (auto units)
        def fmt_speed(bps):
            if bps > 1024**2:
                return f"{bps / 1024**2:5.1f} MB/s"
            elif bps > 1024:
                return f"{bps / 1024:5.1f} KB/s"
            else:
                return f"{bps:5.0f} B/s"

        status = "[green]UP[/green]" if stat.isup else "[red]DOWN[/red]"
        speed_up = f"{fmt_speed(sent_speed)}"
        speed_dw = f"{fmt_speed(recv_speed)}"

        table.add_row(
            iface,
            status,
            ipv4,
            ipv6,
            f"{sent_mb:8.1f} MB",
            f"{recv_mb:8.1f} MB",
            speed_up,
            speed_dw,
        )

    panel = Panel(
        table,
        title="Network Interfaces",
        border_style="cyan",
        padding=(0, 1),
        expand=False,
    )
    text = Text("Press ^C to exit...")
    return Group(panel, text), counters


def main(interval: float = 2):
    """
    Show network interface information, updating every N seconds.
    """

    try:
        interval = float(interval)
    except ValueError:
        interval = 2

    if interval <= 0:
        interval = 2

    prev_counters = None

    try:
        with Live(console=console, transient=False, refresh_per_second=2/interval) as live:
            while True:
                panel, prev_counters = make_table(prev_counters, interval)
                live.update(panel)
                time.sleep(interval)
    except KeyboardInterrupt:
        return