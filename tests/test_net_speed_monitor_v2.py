from unittest import TestCase
from src.net_speed_monitor_v2 import SpeedMonitor


class TestSpeedMonitor(TestCase):
    def test_format_speed_unit(self):
        speed_monitor = SpeedMonitor()
        self.assertEqual(speed_monitor.format_speed_unit(512), "512B/s")
        self.assertEqual(speed_monitor.format_speed_unit(1536), "1.50KB/s")
        self.assertEqual(speed_monitor.format_speed_unit(1048576), "1.00MB/s")
        self.assertEqual(speed_monitor.format_speed_unit(1073741824), "1.00GB/s")
