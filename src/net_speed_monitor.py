# coding=utf8
import time
from psutil import net_io_counters
import tkinter as tk
import threading

KB = 1024
MB = KB * 1024
GB = MB * 1024


def format_speed_unit(speed: int):
    if speed < KB:
        return f"{speed}B/s"
    elif speed < MB:
        return f"{speed / KB:.2f}KB/s"
    elif speed < GB:
        return f"{speed / MB:.2f}MB/s"
    else:
        return f"{speed / GB:.2f}GB/s"


current_net_speed = f"↑{format_speed_unit(0)} ↓{format_speed_unit(0)}"


def get_net_speed():
    global current_net_speed
    while True:
        sent_before = net_io_counters().bytes_sent
        recv_before = net_io_counters().bytes_recv
        time.sleep(1)
        sent_now = net_io_counters().bytes_sent
        recv_now = net_io_counters().bytes_recv
        upload_speed = (sent_now - sent_before)
        download_speed = (recv_now - recv_before)
        current_net_speed = f"↑{format_speed_unit(upload_speed)} ↓{format_speed_unit(download_speed)}"


def update_speed():
    global current_net_speed
    label.config(text=current_net_speed)
    root.after(1000, update_speed)


if __name__ == '__main__':
    thread_a = threading.Thread(target=get_net_speed)
    thread_a.start()

    root = tk.Tk()
    label = tk.Label(root)
    label.pack()
    update_speed()
    root.mainloop()
