from scheduler_server import handler
from datetime import datetime, timezone

def test_dummy():
    t0 = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2023, 11, 2, 0, 0, 0, tzinfo=timezone.utc)
    assert "import time" in handler.dummy_handler(t0, t1, {}) 
