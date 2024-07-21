import argparse
from datetime import datetime, timedelta, timezone
from hijridate._version import __version__
from hijridate.convert import Gregorian, Hijri

def unix_date(args):
    now = datetime.today()

    # Format the date into [YYYY, MM, DD]
    now = now.strftime("%Y,%m,%d").split(",")
    now = list(map(int, now))
    now = Gregorian(*now).to_hijri()

    print(datetime.today().strftime(f'{now.day_name()} {now.month_name()} {now.day} %H:%M:%S UTC {now.year}'))

def main():
    parser = argparse.ArgumentParser(
        description=''
        'Print, set, or convert the system date and time in'
        ' Hijri Islamic Calendar'
    )

    args = parser.parse_args()
    unix_date(args)

if __name__ == "__main__":
    main()
