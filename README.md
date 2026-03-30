# seconds_formatter

## Description
Convenient Python formatter from and to seconds (everything is rounded to microseconds precision). It supports the dd:hh:mm:ss format, as well as a human-friendly adaptive format. It uses [test_functions](https://github.com/gvlassis/test_functions) for minimal testing.

## Getting Started
1) Install/update(-U) seconds_formatter from GitHub

```bash
pip install -U git+https://github.com/gvlassis/seconds_formatter
```

2) Convert from bigger to smaller units and vice versa via constants and functions respectively

```python
import seconds_formatter

# big -> small
seconds_in_six_hours = 6 * seconds_formatter.SECONDS_IN_HOURS
milliseconds_in_five_days = 5 * seconds_formatter.MILLISECONDS_IN_DAYS

# small -> big
print(seconds_formatter.minutes(95)) # 2 minutes
print(seconds_formatter.hours(7230)) # 2 hours
```

3) Convert seconds to the dd:hh:mm:ss format

```python
seconds_formatter.dd_hh_mm_ss(3*3600+25*60+13) # 00:03:25:13
```

4) Convert seconds to the human-friendly adaptive format

```python
seconds_formatter.adaptive(3*3600+25*60+13) # 3h25m
seconds_formatter.adaptive((4*24+6)*3600) # 4d6h
```

5) Run the tests

```bash
python ./seconds_formatter/seconds_formatter.py
```
