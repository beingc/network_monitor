# coding=utf8
import time
from psutil import net_io_counters
import tkinter as tk


def get_speed_unit(speed: int):
    if speed < 1000:
        return f"{speed}B/s"
    elif speed < 1000000:
        return f"{speed / 1024:.2f}KB/s"
    elif speed < 1000000000:
        return f"{speed / 1024 / 1024:.2f}MB/s"


def get_net_speed():
    sent_before = net_io_counters().bytes_sent
    recv_before = net_io_counters().bytes_recv
    time.sleep(1)
    sent_now = net_io_counters().bytes_sent
    recv_now = net_io_counters().bytes_recv
    upload_speed = (sent_now - sent_before)
    download_speed = (recv_now - recv_before)

    # print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), end="")
    # print(f"↑{get_speed_unit(upload_speed)} ↓{get_speed_unit(download_speed)}")
    return f"↑{get_speed_unit(upload_speed)} ↓{get_speed_unit(download_speed)}"


def update_speed():
    current_speed = get_net_speed()
    label.config(text=current_speed)
    root.after(1000, update_speed)


if __name__ == '__main__':
    root = tk.Tk()
    label = tk.Label(root)
    label.pack()
    update_speed()
    root.mainloop()
