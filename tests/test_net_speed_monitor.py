import pytest
from tkinter import Tk
from src.net_speed_monitor import NetworkMonitorApp


@pytest.fixture
def app():
    root = Tk()
    app = NetworkMonitorApp(root)
    return app


def test_format_speed(app):
    assert app.format_speed(500) == "500 B/s"
    assert app.format_speed(2048) == "2.00 KB/s"
    assert app.format_speed(1048576) == "1.00 MB/s"


def test_toggle_cpu_memory_usage(app):
    initial_state = app.show_cpu_mem
    app.show_cpu_memory_usage()
    assert app.show_cpu_mem != initial_state


def test_toggle_always_on_top(app):
    initial_state = app.always_on_top
    app.toggle_always_on_top()
    assert app.always_on_top != initial_state


def test_exit_app(app):
    app.exit_app()
    assert not app.running
