# coding=utf8
import time
from psutil import net_io_counters
import tkinter as tk
import threading
import queue

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


def get_net_speed(queue):
    while True:
        sent_before = net_io_counters().bytes_sent
        recv_before = net_io_counters().bytes_recv
        time.sleep(1)
        sent_now = net_io_counters().bytes_sent
        recv_now = net_io_counters().bytes_recv
        upload_speed = (sent_now - sent_before)
        download_speed = (recv_now - recv_before)
        speed_data = f"↑{format_speed_unit(upload_speed)} ↓{format_speed_unit(download_speed)}"
        queue.put(speed_data)


def update_speed(label, queue):
    speed_data = queue.get()
    label.config(text=speed_data)
    label.after(1000, lambda: update_speed(label, queue))


if __name__ == '__main__':
    speed_queue = queue.Queue()
    thread_a = threading.Thread(target=get_net_speed, args=(speed_queue,))
    thread_a.daemon = True
    thread_a.start()

    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("+1400+100")

    label = tk.Label(root)
    label.pack()
    update_speed(label, speed_queue)
    root.mainloop()
