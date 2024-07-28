import tkinter as tk
from tkinter import Menu
import psutil
import threading
import time


class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry('150x40')

        # 设置窗口透明度为80%
        self.root.attributes('-alpha', 0.8)
        self.root.configure(bg='white')

        # 初始化标签显示网络速度和CPU/内存使用情况
        self.label_net = tk.Label(self.root, text="Initializing...", fg='black', bg='white', font=('Calibri', 10))
        self.label_net.pack(pady=2)

        self.label_cpu_mem = tk.Label(self.root, text="", fg='black', bg='white', font=('Calibri', 10))
        self.label_cpu_mem.pack(pady=2)

        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.show_cpu_mem = False
        self.always_on_top = True
        self.root.attributes('-topmost', self.always_on_top)

        self.create_context_menu()
        self.start_network_monitor()

        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Button-3>", self.show_context_menu)

    def create_context_menu(self):
        """创建右键菜单"""
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Show CPU and Memory Usage", command=self.show_cpu_memory_usage)
        self.menu.add_command(label="Always on Top", command=self.toggle_always_on_top)
        self.menu.add_command(label="Set Transparency", command=self.set_transparency)
        self.menu.add_command(label="Exit", command=self.exit_app)

    def set_transparency(self):
        """设置窗口透明度"""

        def on_scale(val):
            self.root.attributes('-alpha', float(val))

        win = tk.Toplevel(self.root)
        win.title("Set Transparency")
        win.geometry("200x100")
        win.resizable(False, False)

        tk.Label(win, text="Adjust Transparency:").pack(pady=5)
        scale = tk.Scale(win, from_=0.1, to=1.0, orient='horizontal', resolution=0.01, command=on_scale)
        scale.set(0.8)
        scale.pack(pady=5)

    def start_drag(self, event):
        """开始拖动窗口"""
        self.is_dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        """拖动窗口"""
        if self.is_dragging:
            x = self.root.winfo_pointerx() - self.offset_x
            y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry(f'+{x}+{y}')

    def stop_drag(self, event):
        """停止拖动窗口"""
        self.is_dragging = False

    def show_context_menu(self, event):
        """显示右键菜单"""
        self.menu.post(event.x_root, event.y_root)

    def show_cpu_memory_usage(self):
        """切换是否显示CPU和内存使用情况"""
        self.show_cpu_mem = not self.show_cpu_mem
        if not self.show_cpu_mem:
            self.label_cpu_mem.config(text="")

    def toggle_always_on_top(self):
        """切换窗口是否总在最前"""
        self.always_on_top = not self.always_on_top
        self.root.attributes('-topmost', self.always_on_top)

    def exit_app(self):
        """退出应用"""
        self.root.quit()

    def format_speed(self, speed):
        """格式化网络速度"""
        if speed < 1024:
            return f"{speed} B/s"
        elif speed < 1024 * 1024:
            return f"{speed / 1024:.2f} KB/s"
        else:
            return f"{speed / (1024 * 1024):.2f} MB/s"

    def update_network_speed(self):
        """更新网络速度"""
        old_io_counters = psutil.net_io_counters()
        while True:
            time.sleep(1)
            new_io_counters = psutil.net_io_counters()
            download_speed = new_io_counters.bytes_recv - old_io_counters.bytes_recv
            upload_speed = new_io_counters.bytes_sent - old_io_counters.bytes_sent
            self.label_net.config(text=f"↑{self.format_speed(upload_speed)} ↓{self.format_speed(download_speed)}")
            old_io_counters = new_io_counters

    def update_cpu_memory_usage(self):
        """更新CPU和内存使用情况"""
        while True:
            time.sleep(1)
            if self.show_cpu_mem:
                cpu_usage = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                self.label_cpu_mem.config(text=f"CPU: {cpu_usage}% Mem: {memory.percent}%")

    def start_network_monitor(self):
        """启动网络监控"""
        threading.Thread(target=self.update_network_speed, daemon=True).start()
        threading.Thread(target=self.update_cpu_memory_usage, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    root.mainloop()
