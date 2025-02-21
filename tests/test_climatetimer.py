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


def test_initialization():
    timer = ClimateTimer("paris")
    assert timer.reference is not None


@pytest.mark.parametrize("invalid_reference", ["invalid", "earth", "2020"])
def test_invalid_reference(invalid_reference):
    with pytest.raises(ValueError):
        ClimateTimer(invalid_reference)


@pytest.mark.parametrize(
    "dt, blocktype",
    [
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "second"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "minute"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "quarter"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "hour"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "day"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "week"),
    ],
)
def test_blockid_valid(timer_paris, dt, blocktype):
    block_id = timer_paris.blockid(dt, blocktype=blocktype)
    assert isinstance(block_id, int)
    assert block_id > 0


@pytest.mark.parametrize("invalid_blocktype", ["year", "decade", "invalid"])
def test_blockid_invalid_blocktype(timer_paris, invalid_blocktype):
    dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        timer_paris.blockid(dt, blocktype=invalid_blocktype)


@pytest.mark.parametrize(
    "block_id, blocktype",
    [
        (1, "second"),
        (1000, "minute"),
        (50000, "quarter"),
        (100000, "hour"),
        (3000, "day"),
        (500, "week"),
    ],
)
def test_period_valid(timer_paris, block_id, blocktype):
    start, end = timer_paris.period(block_id, blocktype=blocktype)
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert start < end


@pytest.mark.parametrize("invalid_block_id", [-1, 0, "string", None])
def test_period_invalid_block_id(timer_paris, invalid_block_id):
    with pytest.raises(ValueError):
        timer_paris.period(invalid_block_id, blocktype="hour")


@pytest.mark.parametrize("invalid_blocktype", ["year", "invalid", "millennium"])
def test_period_invalid_blocktype(timer_paris, invalid_blocktype):
    with pytest.raises(ValueError):
        timer_paris.period(1000, blocktype=invalid_blocktype)


def test_blockid_negative_paris(timer_paris):
    # Date before Paris Agreement (2016-04-22)
    dt = datetime(2015, 4, 22, 0, 0, tzinfo=timezone.utc)
    assert timer_paris.blockid(dt, blocktype="day") < 0


def test_blockid_negative_kyoto(timer_kyoto):
    # Date before Kyoto Protocol (2005-02-16)
    dt = datetime(2004, 2, 15, 0, 0, tzinfo=timezone.utc)
    assert timer_kyoto.blockid(dt, blocktype="day") < 0


def test_blockid_naive_datetime(timer_paris):
    dt = datetime(2023, 5, 10, 15, 30)  # naive datetime
    with pytest.warns(UserWarning):
        block_id = timer_paris.blockid(dt, blocktype="hour")
    assert isinstance(block_id, int)


@pytest.mark.parametrize(
    "dt",
    [
        "2023-05-10T15:30:00",
        1683816600,
        None,
    ],
)
def test_blockid_invalid_datetime(timer_paris, dt):
    with pytest.raises(TypeError):
        timer_paris.blockid(dt, blocktype="hour")


@pytest.mark.parametrize(
    "block_id",
    [
        "1000",
        None,
    ],
)
def test_period_invalid_block_id_type(timer_paris, block_id):
    with pytest.raises(ValueError):
        timer_paris.period(block_id, blocktype="hour")


def test_info_method(timer_paris, timer_kyoto):
    info_paris = timer_paris.info()
    assert isinstance(info_paris, str)
    assert "Paris Agreement" in info_paris

    info_kyoto = timer_kyoto.info()
    assert isinstance(info_kyoto, str)
    assert "Kyoto Protocol" in info_kyoto
