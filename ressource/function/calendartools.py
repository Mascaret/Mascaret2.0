import calendar
from datetime import date, timedelta


def build_list_of_days(first_day, last_day):
    # Return a list of all the days in a range of months, formated as a list of
    # the day number, the month number, the year & a letter (w for weekdays, f
    # for saturdays and sundays)

    # We convert the day string in date objects so we can work on them
    first_day = get_date_from_ISO(first_day)
    # first_day = first_day.split("-")
    # for i in range(len(first_day)): first_day[i] = int(first_day[i])
    # first_day = date(first_day[0],first_day[1],first_day[2])

    last_day = get_date_from_ISO(last_day)
    # last_day = last_day.split("-")
    # for i in range(len(last_day)): last_day[i] = int(last_day[i])
    # last_day= date(last_day[0],last_day[1],last_day[2])

    list_of_days = []

    day = first_day
    while day < last_day:
        list_of_days.append(str(day))
        day = day + timedelta(days = 1)
    return list_of_days

def get_date_from_ISO(ISO):
# return a date object from an iso
    day = ISO.split("-")
    for i in range(len(day)): day[i] = int(day[i])
    return date(day[0],day[1],day[2])
