from scheduler_server import handler, configs
from datetime import datetime, timezone

def test_dummy():
    t0 = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 11, 2, 0, 0, 0, tzinfo=timezone.utc)
    assert "import time" in handler.dummy_handler(t0, t1, {}) 

def test_basic():
    t0 = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 11, 2, 0, 0, 0, tzinfo=timezone.utc)
    cmds = handler.get_handler('basic')(t0, t1, configs.get_config('basic'))

def test_flex():
    t0 = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 11, 2, 0, 0, 0, tzinfo=timezone.utc)
    cmds = handler.get_handler('flex')(t0, t1, configs.get_config('flex'))

def test_satp1():
    t0 = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 11, 2, 0, 0, 0, tzinfo=timezone.utc)
    cmds = handler.get_handler('sat')(t0, t1, configs.get_config('satp1'))