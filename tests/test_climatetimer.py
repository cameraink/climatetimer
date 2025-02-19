# tests/test_climatetimer.py
import pytest
from datetime import datetime, timezone
from climatetimer.climatetimer import ClimateTimer

@pytest.fixture
def timer_paris():
    return ClimateTimer("paris")

@pytest.fixture
def timer_kyoto():
    return ClimateTimer("kyoto")

@pytest.mark.parametrize("reference", ["paris", "kyoto"])
def test_initialization(reference):
    timer = ClimateTimer(reference)
    assert timer.reference is not None

@pytest.mark.parametrize("invalid_reference", ["invalid", "earth", "2020"])
def test_invalid_reference(invalid_reference):
    with pytest.raises(ValueError):
        ClimateTimer(invalid_reference)

@pytest.mark.parametrize("dt, block_type", [
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "second"),
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "minute"),
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "quarter"),
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "hour"),
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "day"),
    (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "week"),
])
def test_blockid_valid(timer_paris, dt, block_type):
    block_id = timer_paris.blockid(dt, block_type=block_type)
    assert isinstance(block_id, int)
    # Since the reference is 2016-04-22 for Paris, a 2023 date should yield a positive block id.
    assert block_id > 0

@pytest.mark.parametrize("invalid_block_type", ["year", "decade", "invalid"])
def test_blockid_invalid_block_type(timer_paris, invalid_block_type):
    dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        timer_paris.blockid(dt, block_type=invalid_block_type)

@pytest.mark.parametrize("block_id, block_type", [
    (1, "second"),
    (1000, "minute"),
    (50000, "quarter"),
    (100000, "hour"),
    (3000, "day"),
    (500, "week"),
])
def test_period_valid(timer_paris, block_id, block_type):
    start, end = timer_paris.period(block_id, block_type=block_type)
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert start < end

@pytest.mark.parametrize("invalid_block_id", [-1, 0, "string", None])
def test_period_invalid_block_id(timer_paris, invalid_block_id):
    with pytest.raises(ValueError):
        timer_paris.period(invalid_block_id, block_type="hour")

@pytest.mark.parametrize("invalid_block_type", ["year", "invalid", "millennium"])
def test_period_invalid_block_type(timer_paris, invalid_block_type):
    with pytest.raises(ValueError):
        timer_paris.period(1000, block_type=invalid_block_type)

def test_blockid_negative_paris(timer_paris):
    # Use a date before the Paris Agreement reference (2016-04-22)
    dt = datetime(2015, 4, 22, 0, 0, tzinfo=timezone.utc)
    assert timer_paris.blockid(dt, block_type="day") < 0

def test_blockid_negative_kyoto(timer_kyoto):
    # Use a date before the Kyoto Protocol reference (2005-02-16)
    dt = datetime(2004, 2, 15, 0, 0, tzinfo=timezone.utc)
    assert timer_kyoto.blockid(dt, block_type="day") < 0

def test_blockid_naive_datetime(timer_paris):
    dt = datetime(2023, 5, 10, 15, 30)  # naive datetime, no tzinfo
    with pytest.warns(UserWarning):
        block_id = timer_paris.blockid(dt, block_type="hour")
    assert isinstance(block_id, int)

@pytest.mark.parametrize("dt", [
    "2023-05-10T15:30:00",  # string instead of datetime
    1683816600,             # int (unix timestamp)
    None,                   # NoneType
])
def test_blockid_invalid_datetime(timer_paris, dt):
    with pytest.raises(TypeError):
        timer_paris.blockid(dt, block_type="hour")

@pytest.mark.parametrize("block_id", [
    "1000",  # string instead of int
    None,    # NoneType
])
def test_period_invalid_block_id_type(timer_paris, block_id):
    with pytest.raises(ValueError):
        timer_paris.period(block_id, block_type="hour")
