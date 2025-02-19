# ClimateTimer

**ClimateTimer** is a pure-Python library that computes **time block IDs** and **time periods** based on elapsed time units (seconds, minutes, quarters, hours, days, weeks, etc.) since major climate agreements.

It supports two reference points:
- **Paris Agreement** (April 22, 2016, UTC)
- **Kyoto Protocol** (February 16, 2005, UTC)

This package is designed for Python 3, is OS independent, and is licensed under the MIT License.

[![PyPI version](https://img.shields.io/pypi/v/climatetimer.svg)](https://pypi.org/project/climatetimer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/climatetimer.svg)](https://pypi.org/project/climatetimer/)

## Features

- **Flexible Reference Selection:** Choose between the Paris Agreement and the Kyoto Protocol as your starting point.
- **Time Block Calculations:** Compute block IDs and corresponding time periods for various units:
  - Seconds
  - Minutes
  - Quarters (15-minute intervals)
  - Hours
  - Days
  - Weeks
- **Simple API:** Two main methods:
  - `blockid(date, *, block_type)`: Compute the time block ID for a given datetime.
  - `period(block_id, *, block_type)`: Retrieve the start and end datetimes for a specific time block.
- **Modern Packaging:** Built with a pyproject.toml–only configuration.

## Installation

### Using pip
```bash
pip install climatetimer
```

### From Source
Clone the repository and install:
```
git clone https://github.com/cameraink/climatetimer.git
cd climatetimer
pip install .
```

# Quick Start
```
from climatetimer import ClimateTimer
from datetime import datetime, timezone

# Initialize using the Paris Agreement reference
timer = ClimateTimer("paris")

# Compute the block ID for the current hour
block_id = timer.blockid(datetime.utcnow(), block_type="hour")
print(f"Current hour block ID: {block_id}")

# Retrieve the start and end times for that block
start, end = timer.period(block_id, block_type="hour")
print(f"Block {block_id} starts at {start} and ends at {end}")
```

# Usage
## Initializing ClimateTimer
You must specify the reference as a positional argument:
```
# For Paris Agreement
timer_paris = ClimateTimer("paris")
# For Kyoto Protocol
timer_kyoto = ClimateTimer("kyoto")
```

## Computing a Block ID
Pass a timezone-aware datetime and specify the block type:
```
block_id = timer_paris.blockid(datetime(2023, 5, 10, 15, 30, tzinfo=timezone.utc), block_type="hour")
```

## Retrieving a Time Block Period
```
start, end = timer_paris.period(block_id, block_type="hour")
```
