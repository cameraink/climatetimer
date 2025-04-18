import pytest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo  # For handling IANA time zones such as New York
from climatetimer.climatetimer import ClimateTimer


@pytest.fixture
def timer_paris():
    """Return a ClimateTimer instance configured with 'paris'."""
    return ClimateTimer("paris")


@pytest.fixture
def timer_kyoto():
    """Return a ClimateTimer instance configured with 'kyoto'."""
    return ClimateTimer("kyoto")


def test_initialization():
    """
    Test that initializing a ClimateTimer with a valid reference ('paris')
    produces a timer with a non-None reference attribute.
    """
    timer = ClimateTimer("paris")
    assert timer.reference is not None


def test_initialization_uppercase():
    """
    Test that the ClimateTimer initialization is case-insensitive by
    checking that 'Paris' (with an uppercase 'P') is valid.
    """
    timer = ClimateTimer("Paris")
    assert timer.reference is not None


@pytest.mark.parametrize("invalid_reference", ["invalid", "earth", "2020"])
def test_invalid_reference(invalid_reference):
    """
    Test that using an invalid reference string to initialize ClimateTimer
    raises a ValueError.

    Args:
        invalid_reference (str): A reference name that is not accepted.
    """
    with pytest.raises(ValueError):
        ClimateTimer(invalid_reference)


@pytest.mark.parametrize(
    "dt, blocktype",
    [
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "second"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "minute"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "quarter"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "15m"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "hour"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "day"),
        (datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), "week"),
    ],
)
def test_blockid_valid(timer_paris, dt, blocktype):
    """
    Test that blockid returns a positive integer when provided
    with a valid datetime and block type.

    Args:
        dt (datetime): The datetime for which to compute the block ID.
        blocktype (str): The type of the time block (e.g., 'minute', 'hour').
    """
    block_id = timer_paris.blockid(dt, blocktype=blocktype)
    assert isinstance(block_id, int)
    assert block_id > 0


@pytest.mark.parametrize("invalid_blocktype", ["year", "decade", "invalid"])
def test_blockid_invalid_blocktype(timer_paris, invalid_blocktype):
    """
    Test that providing an unsupported block type to blockid raises a ValueError.

    Args:
        invalid_blocktype (str): An invalid or unsupported block type.
    """
    dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        timer_paris.blockid(dt, blocktype=invalid_blocktype)


@pytest.mark.parametrize(
    "block_id, blocktype",
    [
        (1, "second"),
        (1000, "minute"),
        (50000, "quarter"),
        (50000, "15m"),
        (100000, "hour"),
        (3000, "day"),
        (500, "week"),
    ],
)
def test_period_valid(timer_paris, block_id, blocktype):
    """
    Test that the period method returns a tuple of two datetime objects
    representing the start and end of the time period.

    Args:
        block_id (int): The block identifier for the requested period.
        blocktype (str): The time block type.
    """
    start, end = timer_paris.period(block_id, blocktype=blocktype)
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert start < end


@pytest.mark.parametrize("invalid_block_id", [-1, 0, "string", None])
def test_period_invalid_block_id(timer_paris, invalid_block_id):
    """
    Test that providing an invalid block_id to period raises a ValueError.

    Args:
        invalid_block_id: An invalid block id value (e.g., negative, zero, wrong type).
    """
    with pytest.raises(ValueError):
        timer_paris.period(invalid_block_id, blocktype="hour")


@pytest.mark.parametrize("invalid_blocktype", ["year", "invalid", "millennium"])
def test_period_invalid_blocktype(timer_paris, invalid_blocktype):
    """
    Test that providing an invalid block type to period raises a ValueError.

    Args:
        invalid_blocktype (str): A block type that is not supported.
    """
    with pytest.raises(ValueError):
        timer_paris.period(1000, blocktype=invalid_blocktype)


def test_blockid_negative_paris(timer_paris):
    """
    Test that blockid returns a negative value when a datetime preceding the Paris Agreement
    reference date (April 22, 2016) is provided.
    """
    dt = datetime(2015, 4, 22, 0, 0, tzinfo=timezone.utc)
    assert timer_paris.blockid(dt, blocktype="day") < 0


def test_blockid_negative_kyoto(timer_kyoto):
    """
    Test that blockid returns a negative value when a datetime preceding the Kyoto Protocol
    reference date (February 16, 2005) is provided.
    """
    dt = datetime(2004, 2, 15, 0, 0, tzinfo=timezone.utc)
    assert timer_kyoto.blockid(dt, blocktype="day") < 0


def test_blockid_naive_datetime(timer_paris):
    """
    Test that providing a naive datetime (lacking timezone info) to blockid
    issues a UserWarning yet still returns a valid integer block ID.
    """
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
    """
    Test that providing an invalid datetime type (e.g., string, integer, or None)
    to blockid results in a TypeError.

    Args:
        dt: The invalid datetime value.
    """
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
    """
    Test that providing a block_id of an incorrect type (such as string or None)
    to period raises a ValueError.

    Args:
        block_id: The block id of the wrong type.
    """
    with pytest.raises(ValueError):
        timer_paris.period(block_id, blocktype="hour")


def test_info_method(timer_paris, timer_kyoto):
    """
    Test that the info method returns a string containing the correct protocol
    reference for each timer instance (i.e., 'Paris Agreement' for Paris and
    'Kyoto Protocol' for Kyoto).
    """
    info_paris = timer_paris.info()
    assert isinstance(info_paris, str)
    assert "Paris Agreement" in info_paris

    info_kyoto = timer_kyoto.info()
    assert isinstance(info_kyoto, str)
    assert "Kyoto Protocol" in info_kyoto


def test_blockids_valid(timer_paris):
    """
    Test that blockids returns a list of block IDs for a valid date range.

    The test verifies the length of the returned list matches the expected number of blocks.
    """
    start_date = datetime(2025, 3, 1, tzinfo=timezone.utc)
    end_date = datetime(2025, 3, 5, tzinfo=timezone.utc)
    blockids_list = timer_paris.blockids(start_date, end_date, blocktype="day")
    expected_length = 5
    assert isinstance(blockids_list, list)
    assert len(blockids_list) == expected_length


def test_blockids_invalid_date_range(timer_paris):
    """
    Test that blockids raises a ValueError if the start date is later than the end date.
    """
    start_date = datetime(2025, 3, 5, tzinfo=timezone.utc)
    end_date = datetime(2025, 3, 1, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        timer_paris.blockids(start_date, end_date, blocktype="day")


def test_blockids_naive_datetime(timer_paris):
    """
    Test that blockids issues a warning when a naive datetime (without timezone info)
    is provided as the start date, while still returning a list of block IDs.
    """
    start_date = datetime(2025, 3, 1)  # naive datetime
    end_date = datetime(2025, 3, 5, tzinfo=timezone.utc)
    with pytest.warns(UserWarning):
        blockids_list = timer_paris.blockids(start_date, end_date, blocktype="day")
    assert isinstance(blockids_list, list)


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        ("2025-03-01", datetime(2025, 3, 5, tzinfo=timezone.utc)),
        (datetime(2025, 3, 1, tzinfo=timezone.utc), "2025-03-05"),
    ],
)
def test_blockids_invalid_datetime(timer_paris, start_date, end_date):
    """
    Test that blockids raises a TypeError when either the start_date or end_date
    is provided in an invalid format (non-datetime).

    Args:
        start_date: The starting date, which may be invalid.
        end_date: The ending date, which may be invalid.
    """
    with pytest.raises(TypeError):
        timer_paris.blockids(start_date, end_date, blocktype="day")


def test_blockids_invalid_blocktype(timer_paris):
    """
    Test that blockids raises a ValueError when an invalid block type is provided.
    """
    start_date = datetime(2025, 3, 1, tzinfo=timezone.utc)
    end_date = datetime(2025, 3, 5, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        timer_paris.blockids(start_date, end_date, blocktype="year")


def test_blockids_single_block_if_range_short(timer_paris):
    """
    Test that when a short date range falls completely within a single time block,
    blockids returns a list with exactly one block ID.

    Uses the 'second' block type with a range narrower than one second.
    """
    start_date = timer_paris.reference + timedelta(seconds=10)
    end_date = timer_paris.reference + timedelta(seconds=10, microseconds=500000)
    blockids_list = timer_paris.blockids(start_date, end_date, blocktype="second")
    assert len(blockids_list) == 1


def test_blockids_overlap_reference_includes_zero(timer_paris):
    """
    Test that blockids handles a date range that overlaps the timer's reference point.

    For a 'second' block type, verifies that the block ID corresponding to just before
    the reference (expected to be 0) is included and that the total number of blocks is correct.
    """
    start_date = timer_paris.reference - timedelta(seconds=1)
    end_date = timer_paris.reference + timedelta(seconds=1)
    blockids_list = timer_paris.blockids(start_date, end_date, blocktype="second")
    assert 0 in blockids_list
    expected_length = 3
    assert len(blockids_list) == expected_length


@pytest.mark.parametrize(
    "dt_utc, dt_ny",
    [
        (
            datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 1, 12, 0, tzinfo=ZoneInfo("America/New_York")),
        ),
    ],
)
def test_timezone_handling(timer_paris, dt_utc, dt_ny):
    """
    Test that the ClimateTimer calculates distinct block IDs for the same local time
    specified in different time zones.

    In this test, the datetime for 12:00 UTC and 12:00 in the New York time zone are used.
    Although they share the same wall-clock time, they represent different moments in time.
    The test asserts that their computed block IDs (using the 'hour' block type) are different.
    """
    block_id_utc = timer_paris.blockid(dt_utc, blocktype="hour")
    block_id_ny = timer_paris.blockid(dt_ny, blocktype="hour")
    assert block_id_utc != block_id_ny

    block_id_utc = timer_paris.blockid(dt_utc, blocktype="15m")
    block_id_ny = timer_paris.blockid(dt_ny, blocktype="15m")
    assert block_id_utc != block_id_ny
