from scheduler_server import handler, configs
from datetime import datetime, timezone

def test_dummy():
    t0 = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 1, 2, 0, 0, 10, tzinfo=timezone.utc)
    assert "import time" in handler.dummy_policy(t0, t1, {}) 

def test_basic():
    t0 = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 1, 2, 0, 0, 10, tzinfo=timezone.utc)
    cmds = handler.basic_policy(t0, t1, configs.get_default_config('basic'))
    assert len(cmds) == 5349
