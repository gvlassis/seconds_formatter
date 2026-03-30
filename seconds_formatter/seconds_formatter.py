import test_functions


MICROSECONDS_IN_MILLISECONDS = 1000

MILLISECONDS_IN_SECONDS = 1000
MICROSECONDS_IN_SECONDS = MICROSECONDS_IN_MILLISECONDS * MILLISECONDS_IN_SECONDS

SECONDS_IN_MINUTES = 60
MILLISECONDS_IN_MINUTES = MILLISECONDS_IN_SECONDS * SECONDS_IN_MINUTES
MICROSECONDS_IN_MINUTES = MICROSECONDS_IN_MILLISECONDS * MILLISECONDS_IN_MINUTES

MINUTES_IN_HOURS = 60
SECONDS_IN_HOURS = SECONDS_IN_MINUTES * MINUTES_IN_HOURS
MILLISECONDS_IN_HOURS = MILLISECONDS_IN_SECONDS * SECONDS_IN_HOURS
MICROSECONDS_IN_HOURS = MICROSECONDS_IN_MILLISECONDS * MILLISECONDS_IN_HOURS

HOURS_IN_DAYS = 24
MINUTES_IN_DAYS = MINUTES_IN_HOURS * HOURS_IN_DAYS
SECONDS_IN_DAYS = SECONDS_IN_MINUTES * MINUTES_IN_DAYS
MILLISECONDS_IN_DAYS = MILLISECONDS_IN_SECONDS * SECONDS_IN_DAYS
MICROSECONDS_IN_DAYS = MICROSECONDS_IN_MILLISECONDS * MILLISECONDS_IN_DAYS


def microseconds(seconds=0):
    return round(seconds * MICROSECONDS_IN_SECONDS)

def milliseconds(seconds=0):
    return round(seconds * MILLISECONDS_IN_SECONDS)

def minutes(seconds=0):
    return round(seconds / SECONDS_IN_MINUTES)

def hours(seconds=0):
    return round(seconds / SECONDS_IN_HOURS)

def days(seconds=0):
    return round(seconds / SECONDS_IN_DAYS)


def milliseconds_microseconds(seconds=0):
    microseconds_ = microseconds(seconds)
    
    milliseconds_ = microseconds_ // MICROSECONDS_IN_MILLISECONDS
    microseconds_ = microseconds_ % MICROSECONDS_IN_MILLISECONDS

    return milliseconds_, microseconds_

def seconds_milliseconds_microseconds(seconds=0):
    microseconds_ = microseconds(seconds)

    seconds_ = microseconds_ // MICROSECONDS_IN_SECONDS
    microseconds_ = microseconds_ % MICROSECONDS_IN_SECONDS
    
    seconds = microseconds_ / MICROSECONDS_IN_SECONDS
    milliseconds_, microseconds_ = milliseconds_microseconds(seconds)

    return seconds_, milliseconds_, microseconds_

def minutes_seconds_milliseconds_microseconds(seconds=0):
    microseconds_ = microseconds(seconds)

    minutes_ = microseconds_ // MICROSECONDS_IN_MINUTES
    microseconds_ = microseconds_ % MICROSECONDS_IN_MINUTES
    
    seconds = microseconds_ / MICROSECONDS_IN_SECONDS
    seconds_, milliseconds_, microseconds_ = seconds_milliseconds_microseconds(seconds)

    return minutes_, seconds_, milliseconds_, microseconds_

def hours_minutes_seconds_milliseconds_microseconds(seconds=0):
    microseconds_ = microseconds(seconds)

    hours_ = microseconds_ // MICROSECONDS_IN_HOURS
    microseconds_ = microseconds_ % MICROSECONDS_IN_HOURS
    
    seconds = microseconds_ / MICROSECONDS_IN_SECONDS
    minutes_, seconds_, milliseconds_, microseconds_ = minutes_seconds_milliseconds_microseconds(seconds)
    
    return hours_, minutes_, seconds_, milliseconds_, microseconds_

def days_hours_minutes_seconds_milliseconds_microseconds(seconds=0):
    microseconds_ = microseconds(seconds)

    days_ = microseconds_ // MICROSECONDS_IN_DAYS
    microseconds_ = microseconds_ % MICROSECONDS_IN_DAYS
    
    seconds = microseconds_ / MICROSECONDS_IN_SECONDS
    hours_, minutes_, seconds_, milliseconds_, microseconds_ = hours_minutes_seconds_milliseconds_microseconds(seconds)

    return days_, hours_, minutes_, seconds_, milliseconds_, microseconds_


def dd_hh_mm_ss(seconds=0):
    seconds = round(seconds)
    
    days_, hours_, minutes_, seconds_, milliseconds_, microseconds = days_hours_minutes_seconds_milliseconds_microseconds(seconds)
    assert milliseconds_ == microseconds == 0
    
    return f"{days_:02}:{hours_:02}:{minutes_:02}:{seconds_:02}"


def adaptive(seconds=0):
    days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)

    if days_ > 0:
        # Round to the nearest hour
        hours_ = hours(seconds)
        seconds = hours_ * SECONDS_IN_HOURS
        days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)

        assert minutes_ == seconds_ == milliseconds_ == microseconds_ == 0
        return f"{days_}d{hours_}h" if hours_ else f"{days_}d"

    elif hours_ > 0: # days_ == 0
        # Round to the nearest minute
        minutes_ = minutes(seconds)
        seconds = minutes_ * SECONDS_IN_MINUTES
        days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)

        assert seconds_ == milliseconds_ == microseconds_ == 0

        if days_ == 1:
            assert hours_ == minutes_ == 0
            return "1d"

        else:
            return f"{hours_}h{minutes_}m" if minutes_ else f"{hours_}h"

    elif minutes_ > 0: # days_ == hours_ == 0
        # Round to the nearest second
        seconds = round(seconds)
        days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)

        assert milliseconds_ == microseconds_ == 0

        if hours_ == 1:
            assert minutes_ == seconds_ == 0
            return "1h"

        else:
            return f"{minutes_}m{seconds_}s" if seconds_ else f"{minutes_}m"

    elif seconds_ > 0: # days_ == hours_ == minutes_ == 0
        digits = len(str(seconds_))

        if digits == 2:
            # Round to the nearest millisecond hundredth
            hundred_milliseconds_in_seconds = MILLISECONDS_IN_SECONDS//100
            hundred_milliseconds_ = round(seconds * hundred_milliseconds_in_seconds)
            seconds =  hundred_milliseconds_ / hundred_milliseconds_in_seconds
            days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)
            padded = f"{milliseconds_:03}"

            assert int(padded[1]) ==  int(padded[2]) == microseconds_ == 0

            if minutes_ == 1:
                assert seconds_ == milliseconds_ == 0
                return "1m"

            else:
                return f"{seconds_}.{padded[0]}s" if int(padded[0]) else f"{seconds_}s"

        else: # digits == 1
            # Round to the nearest millisecond tenth
            ten_milliseconds_in_seconds = MILLISECONDS_IN_SECONDS//10
            ten_milliseconds_ = round(seconds * ten_milliseconds_in_seconds)
            seconds =  ten_milliseconds_ / ten_milliseconds_in_seconds
            days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)
            padded = f"{milliseconds_:03}"

            assert int(padded[2]) == microseconds_ == 0

            if seconds_ == 10:
                assert milliseconds_ == 0
                return "10s"

            else:
                return f"{seconds_}.{padded[0]}{padded[1]}s" if int(padded[0]) or int(padded[1]) else f"{seconds_}s"

    elif milliseconds_ > 0: # days_ == hours_ == minutes_ == seconds_ == 0
        digits = len(str(milliseconds_))

        if digits == 3:
            # Round to the nearest millisecond
            milliseconds_ = milliseconds(seconds)
            seconds = milliseconds_ / MILLISECONDS_IN_SECONDS
            days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)

            assert microseconds_ == 0

            if seconds_ == 1:
                assert milliseconds_ == 0
                return "1s"

            else:
                return f"{milliseconds_}ms"

        elif digits == 2:
            # Round to the nearest microsecond hundredth
            hundred_microseconds_in_seconds = MICROSECONDS_IN_SECONDS//100
            hundred_microseconds_ = round(seconds * hundred_microseconds_in_seconds)
            seconds =  hundred_microseconds_ / hundred_microseconds_in_seconds
            days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)
            padded = f"{microseconds_:03}"

            assert int(padded[1]) ==  int(padded[2]) == 0

            if milliseconds_ == 100:
                assert microseconds_ == 0
                return "100ms"

            else:
                return f"{milliseconds_}.{padded[0]}ms" if int(padded[0]) else f"{milliseconds_}ms"

        else: # digits == 1
            # Round to the nearest microsecond tenth
            ten_microseconds_in_seconds = MICROSECONDS_IN_SECONDS//10
            ten_microseconds_ = round(seconds * ten_microseconds_in_seconds)
            seconds =  ten_microseconds_ / ten_microseconds_in_seconds
            days_, hours_, minutes_, seconds_, milliseconds_, microseconds_ = days_hours_minutes_seconds_milliseconds_microseconds(seconds)
            padded = f"{microseconds_:03}"

            assert int(padded[2]) == 0

            if milliseconds_ == 10:
                assert microseconds_ == 0
                return "10ms"

            else:
                return f"{milliseconds_}.{padded[0]}{padded[1]}ms" if int(padded[0]) or int(padded[1]) else f"{milliseconds_}ms"

    else: # days_ == hours_ == minutes_ == seconds_ == milliseconds_ == 0
        return f"{microseconds_}μs"


def seconds_in(days_=0, hours_=0, minutes_=0, seconds_=0, milliseconds_=0, microseconds_=0):
    return (
        days_ * SECONDS_IN_DAYS +
        hours_ * SECONDS_IN_HOURS +
        minutes_ * SECONDS_IN_MINUTES +
        seconds_ +
        milliseconds_ / MILLISECONDS_IN_SECONDS +
        microseconds_ / MICROSECONDS_IN_SECONDS
    )

def test_adaptive():
    return test_functions.test_tuples(
        [
            ("120d", adaptive(seconds_in(120))),
            ("120d10h", adaptive(seconds_in(120,10))),
            ("120d23h", adaptive(seconds_in(120,23))),
            ("120d23h", adaptive(seconds_in(120,23,0,35))),
            ("121d", adaptive(seconds_in(120,23,40))),
            ("120d14h", adaptive(seconds_in(120,14,29,59,999,999))),
            ("120d15h", adaptive(seconds_in(120,14,30,0,0,1))),
            ("23h45m", adaptive(seconds_in(0,23,45))),
            ("23h45m", adaptive(seconds_in(0,23,45,23))),
            ("23h46m", adaptive(seconds_in(0,23,45,34))),
            ("23h59m", adaptive(seconds_in(0,23,59,0,999))),
            ("23h59m", adaptive(seconds_in(0,23,59,0,999,999))),
            ("1d", adaptive(seconds_in(0,23,59,59,999,999))),
            ("1d", adaptive(seconds_in(0,23,59,59))),
            ("15h", adaptive(seconds_in(0,15))),
            ("50m10s", adaptive(seconds_in(0,0,50,10))),
            ("50m10s", adaptive(seconds_in(0,0,50,10))),
            ("50m11s", adaptive(seconds_in(0,0,50,10,999))),
            ("50m10s", adaptive(seconds_in(0,0,50,10,499,999))),
            ("50m11s", adaptive(seconds_in(0,0,50,10,500,1))),
            ("59m59s", adaptive(seconds_in(0,0,59,59))),
            ("1h", adaptive(seconds_in(0,0,59,59,900))),
            ("52m", adaptive(seconds_in(0,0,51,59,820))),
            ("41m", adaptive(seconds_in(0,0,41))),
            ("59.9s", adaptive(seconds_in(0,0,0,59,900))),
            ("1m", adaptive(seconds_in(0,0,0,59,990))),
            ("1m", adaptive(seconds_in(0,0,0,59,999))),
            ("27s", adaptive(seconds_in(0,0,0,27))),
            ("27s", adaptive(seconds_in(0,0,0,27,5))),
            ("27s", adaptive(seconds_in(0,0,0,27,0,5))),
            ("28.6s", adaptive(seconds_in(0,0,0,28,599,999))),
            ("28.5s", adaptive(seconds_in(0,0,0,28,540))),
            ("500ms", adaptive(seconds_in(0,0,0,0,500))),
            ("999ms", adaptive(seconds_in(0,0,0,0,999))),
            ("999ms", adaptive(seconds_in(0,0,0,0,999,380))),
            ("1s", adaptive(seconds_in(0,0,0,0,999,660))),
            ("21ms", adaptive(seconds_in(0,0,0,0,21))),
            ("21.5ms", adaptive(seconds_in(0,0,0,0,21,451))),
            ("99ms", adaptive(seconds_in(0,0,0,0,99))),
            ("99.9ms", adaptive(seconds_in(0,0,0,0,99,900))),
            ("100ms", adaptive(seconds_in(0,0,0,0,99,990))),
            ("7ms", adaptive(seconds_in(0,0,0,0,7))),
            ("7.06ms", adaptive(seconds_in(0,0,0,0,7,56))),
            ("7.57ms", adaptive(seconds_in(0,0,0,0,7,566))),
            ("9.91ms", adaptive(seconds_in(0,0,0,0,9,912))),
            ("9.99ms", adaptive(seconds_in(0,0,0,0,9,994))),
            ("10ms", adaptive(seconds_in(0,0,0,0,9,997))),
            ("789μs", adaptive(seconds_in(0,0,0,0,0,789))),
            ("89μs", adaptive(seconds_in(0,0,0,0,0,89))),
            ("0μs", adaptive(seconds_in()))
        ]
    )


if __name__ == "__main__":
    exit(not test_functions.test_functions([test_adaptive]))
