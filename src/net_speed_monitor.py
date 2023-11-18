# coding=utf8
import time
from psutil import net_io_counters


def get_net_speed():
    sent_before = net_io_counters().bytes_sent
    recv_before = net_io_counters().bytes_recv
    time.sleep(1)
    sent_now = net_io_counters().bytes_sent
    recv_now = net_io_counters().bytes_recv
    upload_speed = (sent_now - sent_before)
    download_speed = (recv_now - recv_before)

    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), end="")
    print(f"↑{get_speed_unit(upload_speed)} ↓{get_speed_unit(download_speed)}")


def get_speed_unit(speed: int):
    if speed < 1000:
        return f"{speed}B/s"
    elif speed < 1000000:
        return f"{speed / 1024:.2f}KB/s"
    elif speed < 1000000000:
        return f"{speed / 1024 / 1024:.2f}MB/s"


if __name__ == '__main__':
    while True:
        get_net_speed()
