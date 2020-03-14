import datetime


def date_Range_list(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    # days = (strptime(end, format) - strptime(start, format)).days
    days = (end - start).days+1
    print(days)
    return [start + datetime.timedelta(i) for i in range(0, days, step)]


if __name__ == '__main__':
    print(date_Range_list("2020-03-01 00:00:00", "2020-03-05 00:00:00", format="%Y-%m-%d %H:%M:%S"))
