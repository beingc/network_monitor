import threading
import queue
import time
import tkinter as tk
from psutil import net_io_counters


class SpeedMonitor:
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024

    def __init__(self):
        self.speed_queue = queue.Queue()
        self.thread_a = threading.Thread(target=self.get_net_speed)
        self.thread_a.daemon = True
        self.thread_a.start()

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+1400+100")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.update_speed()

    def format_speed_unit(self, speed: int):
        if speed < self.KB:
            return f"{speed}B/s"
        elif speed < self.MB:
            return f"{speed / self.KB:.2f}KB/s"
        elif speed < self.GB:
            return f"{speed / self.MB:.2f}MB/s"
        else:
            return f"{speed / self.GB:.2f}GB/s"

    def get_net_speed(self):
        while True:
            sent_before = net_io_counters().bytes_sent
            recv_before = net_io_counters().bytes_recv
            time.sleep(1)
            sent_now = net_io_counters().bytes_sent
            recv_now = net_io_counters().bytes_recv
            upload_speed = (sent_now - sent_before)
            download_speed = (recv_now - recv_before)
            speed_data = f"↑{self.format_speed_unit(upload_speed)} ↓{self.format_speed_unit(download_speed)}"
            self.speed_queue.put(speed_data)

    def update_speed(self):
        speed_data = self.speed_queue.get()
        self.label.config(text=speed_data)
        self.label.after(1000, self.update_speed)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    speed_monitor = SpeedMonitor()
    speed_monitor.run()
