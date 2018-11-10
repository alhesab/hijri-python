from hijriconverter import ummalqura
from typing import Tuple


def check_hijri_calendar(calendar: str) -> str:
    """Check type and value of hijri calendar."""
    calendars = ['lunar', 'solar']
    if not isinstance(calendar, str):
        raise TypeError('calendar must be a string')
    if calendar.lower() not in calendars:
        raise ValueError('calendar must be \'{}\' or \'{}\''.format(
                *calendars))
    return calendar.lower()


def check_date(year: int, month: int, day: int,
               calendar: str) -> Tuple[int, int, int]:
    """Check date values and if date is within conversion range."""
    # check year
    if not isinstance(year, int):
        raise TypeError('year must be an integer')
    if year < 1 or len(str(year)) != 4:
        raise ValueError('year must be in yyyy format')
    # check month
    if not isinstance(month, int):
        raise TypeError('month must be an integer')
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12')
    # check range
    calendar_range = ummalqura.ranges[calendar]
    if not calendar_range[0] <= (year, month, day) <= calendar_range[1]:
        raise ValueError('date is out of range for conversion')
    # check day
    if not isinstance(day, int):
        raise TypeError('day must be an integer')
    if calendar == 'gregorian':
        is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        gregorian_months = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2 and is_leap:
            month_days = 29
        else:
            month_days = gregorian_months[month]
    else:
        month_days = hijri_month_days(year, month, calendar)
    if not 1 <= day <= month_days:
        raise ValueError('day must be in 1..{} for month'.format(month_days))
    return year, month, day


def hijri_month_index(year: int, month: int, calendar: str) -> int:
    """Return index of month modified julian day in ummalqura month_starts."""
    years = year - 1
    months = (years * 12) + month
    index = months - ummalqura.first_month_offset[calendar]
    return index


def hijri_month_days(year: int, month: int, calendar: str) -> int:
    """Return number of days in hijri month."""
    i = hijri_month_index(year, month, calendar)
    month_starts = ummalqura.month_starts[calendar]
    days = month_starts[i] - month_starts[i - 1]
    return days


def hijri_to_julian(year: int, month: int, day: int, calendar: str) -> int:
    """Convert hijri date to julian day."""
    i = hijri_month_index(year, month, calendar)
    month_starts = ummalqura.month_starts[calendar]
    mjd = day + month_starts[i - 1] - 1
    jd = modified_julian_to_julian(mjd)
    return jd


def gregorian_to_julian(year: int, month: int, day: int) -> int:
    """Convert gregorian date to julian day."""
    i = int((month - 14) / 12)
    jd = int((1461 * (year + 4800 + i)) / 4)
    jd += int((367 * (month - 2 - (12 * i))) / 12)
    jd -= int((3 * int((year + 4900 + i) / 100)) / 4)
    jd += day - 32075
    return jd


def julian_to_gregorian(jd: int) -> Tuple[int, int, int]:
    """Convert julian day to gregorian date."""
    i = jd + 68569
    n = int((4 * i) / 146097)
    i -= int(((146097 * n) + 3) / 4)
    ii = int((4000 * (i + 1)) / 1461001)
    i -= int((1461 * ii) / 4) - 31
    j = int((80 * i) / 2447)
    day = i - int((2447 * j) / 80)
    i = int(j / 11)
    month = j + 2 - (12 * i)
    year = 100 * (n - 49) + ii + i
    return year, month, day


def julian_to_modified_julian(jd: int) -> int:
    """Convert julian day to modified julian day number."""
    mjd0 = 2400000
    return jd - mjd0


def modified_julian_to_julian(mjd: int) -> int:
    """Convert modified julian day number to julian day."""
    mjd0 = 2400000
    return mjd + mjd0

