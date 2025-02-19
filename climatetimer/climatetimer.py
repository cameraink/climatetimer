# climatetimer/climatetimer.py
import logging
import warnings
from datetime import datetime, timedelta, timezone
from math import floor
from typing import Tuple

from .constants import (
    REFERENCES,
    SECOND_DURATION,
    MINUTE_DURATION,
    QUARTER_DURATION,
    HOUR_DURATION,
    DAY_DURATION,
    WEEK_DURATION,
)

# Configure logging (if you wish to keep logging, in addition to warnings)
logger = logging.getLogger(__name__)

# Supported block types and their durations (in seconds)
TIME_BLOCKS = {
    "second": SECOND_DURATION,
    "minute": MINUTE_DURATION,
    "quarter": QUARTER_DURATION,
    "hour": HOUR_DURATION,
    "day": DAY_DURATION,
    "week": WEEK_DURATION,
}


class ClimateTimer:
    """
    Computes time block IDs (blockid) and time periods (period) for different time units
    since a selected climate agreement (Paris Agreement or Kyoto Protocol).

    The reference timestamp is passed as a positional argument:
        - "paris": April 22, 2016 (UTC)
        - "kyoto": February 16, 2005 (UTC)

    Methods:
        - blockid(date, *, block_type) -> int
        - period(block_id, *, block_type) -> Tuple[datetime, datetime]
    """

    def __init__(self, reference: str):
        """
        Initialize ClimateTimer with a selected reference timestamp.

        Args:
            reference (str): "paris" or "kyoto"

        Raises:
            ValueError: If an invalid reference is provided.
        """
        if reference not in REFERENCES:
            raise ValueError(f"Invalid reference '{reference}'. Choose from {list(REFERENCES.keys())}.")
        self.reference = REFERENCES[reference]

    def _validate_datetime(self, dt: datetime) -> datetime:
        """
        Ensure dt is a timezone-aware datetime.

        Args:
            dt (datetime): Datetime to validate.

        Returns:
            datetime: A timezone-aware datetime.

        Raises:
            TypeError: If dt is not a datetime object.
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"Expected datetime object, got {type(dt).__name__}.")
        if dt.tzinfo is None:
            warnings.warn("Naive datetime provided; assuming UTC.", UserWarning)
            return dt.replace(tzinfo=timezone.utc)
        return dt

    def _validate_block_type(self, block_type: str):
        """
        Validate that block_type is supported.

        Args:
            block_type (str): Block type to validate.

        Raises:
            ValueError: If block_type is not one of the supported types.
        """
        if block_type not in TIME_BLOCKS:
            raise ValueError(f"Invalid block type '{block_type}'. Choose from {list(TIME_BLOCKS.keys())}.")

    def _validate_block_id(self, block_id: int) -> int:
        """
        Validate that block_id is a positive integer.

        Args:
            block_id (int): The block ID.

        Returns:
            int: The validated block ID.

        Raises:
            ValueError: If block_id is not a positive integer.
        """
        if not isinstance(block_id, int) or block_id < 1:
            raise ValueError(f"Invalid block_id {block_id}. Must be a positive integer.")
        return block_id

    def blockid(self, date: datetime, *, block_type: str) -> int:
        """
        Compute the time block ID for the given datetime and block type.

        Args:
            date (datetime): The datetime for computation.
            block_type (str): The block type ("second", "minute", "quarter", "hour", "day", "week").

        Returns:
            int: The computed block ID.
        """
        self._validate_block_type(block_type)
        date = self._validate_datetime(date)
        delta = date - self.reference
        return floor(delta.total_seconds() / TIME_BLOCKS[block_type]) + 1

    def period(self, block_id: int, *, block_type: str) -> Tuple[datetime, datetime]:
        """
        Get the start and end datetimes for the given block ID and block type.

        Args:
            block_id (int): The time block ID.
            block_type (str): The block type ("second", "minute", "quarter", "hour", "day", "week").

        Returns:
            Tuple[datetime, datetime]: The start and end of the block period.
        """
        self._validate_block_type(block_type)
        block_id = self._validate_block_id(block_id)
        start = self.reference + timedelta(seconds=(block_id - 1) * TIME_BLOCKS[block_type])
        return start, start + timedelta(seconds=TIME_BLOCKS[block_type])
