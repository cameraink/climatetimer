[![PyPI version](https://img.shields.io/pypi/v/climatetimer.svg)](https://pypi.org/project/climatetimer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/climatetimer.svg)](https://pypi.org/project/climatetimer/)

# ClimateTimer

**ClimateTimer** is a pure-Python library that computes **time block IDs** and **time periods** based on elapsed time units (seconds, minutes, quarters, hours, days, weeks, etc.) since major climate agreements.

It supports two reference points:
- **Paris Agreement** (April 22, 2016, UTC)
- **Kyoto Protocol** (February 16, 2005, UTC)

This package is designed for Python 3, is OS independent, and is licensed under the MIT License.

## Release notes

v0.3
- new method `blockids` (with 's') that returns a list of blockId's between two dates.

## Features

### Flexible Time Reference Selection
Choose between the Paris Agreement and the Kyoto Protocol as your starting point.

### Time Block Calculations
Compute block IDs and corresponding time periods for various units:
  - Seconds
  - Minutes
  - Quarters (15-minute intervals)
  - Hours
  - Days
  - Weeks

### Simple and intuitive API

  - `blockid(date, blocktype="quarter")`: Compute the time block ID.  
    - **date:** A timezone-aware datetime (positional).  
    - **blocktype:** The type of block (e.g., "second", "minute", "quarter", "hour", "day", "week"). Defaults to `"quarter"`.

  - `period(block_id, blocktype="quarter")`: Retrieve the start and end datetimes for a given block.

### Reference Information
  The `info()` method returns a plain-text description of the instantiated reference event.

### Modern Packaging
Built with a pyproject.toml–only configuration.

## Installation

### Using pip
```bash
pip install climatetimer
```

### From Source
Clone the repository and install:
```bash
git clone https://github.com/cameraink/climatetimer.git
cd climatetimer
pip install .
```

# Quick Start
```python
from climatetimer import ClimateTimer
from datetime import datetime, timezone

# Initialize using the Paris Agreement reference
timer = ClimateTimer("paris")

# Compute the block ID for the current hour (date is positional; blocktype defaults to "quarter")
block_id = timer.blockid(datetime.utcnow(), blocktype="hour")
print(f"Current hour block ID: {block_id}")

# Retrieve the start and end times for that block
start, end = timer.period(block_id, blocktype="hour")
print(f"Block {block_id} starts at {start} and ends at {end}")

# Get information about the reference event for this instance
print("Reference Info:", timer.info())
```

# Usage
## Initializing ClimateTimer
You must specify the reference as a positional argument:
```python
# For Paris Agreement
timer_paris = ClimateTimer("paris")

# For Kyoto Protocol
timer_kyoto = ClimateTimer("kyoto")

```

## Computing a Block ID
Pass a timezone-aware datetime and specify the block type:
```python
block_id = timer_paris.blockid(datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), blocktype="hour")
```

## Retrieving a Time Block Period
```python
info = timer_paris.info()
print("Reference Info:", info)
```

## Computing a list of Block IDs
Pass a timezone-aware start time and end time and specify the block type:
```python
from datetime import datetime, timezone
from climatetimer import ClimateTimer

# Create an instance of ClimateTimer using the "paris" reference
timer = ClimateTimer("paris")

# Define the start and end datetimes (make sure they're timezone-aware)
start_date = datetime(2025, 3, 1, tzinfo=timezone.utc)
end_date = datetime(2025, 3, 27, tzinfo=timezone.utc)

# Compute the list of block IDs for the specified date range and block type
block_ids = timer.blockids(start_date, end_date, blocktype="quarter")

# Output the list of block IDs
print("Block IDs:", block_ids)
```

Note that `blockids` raise an error if the condition start_date > end_date is not satisfied.