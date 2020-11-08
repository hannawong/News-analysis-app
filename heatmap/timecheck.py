import datetime
def string2timestamp(strValue):
    import time
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        print(e)
        return 0


# 1440751417.283 --> '2015-08-28'
def timestamp2date(timeStamp):
    return datetime.datetime.fromtimestamp(timeStamp).date()

def timestamp2date_utc(timeStamp):
    return datetime.datetime.utcfromtimestamp(timeStamp).date()


if __name__ == '__main__':
    # now's starttime and endtime
    ts1 = string2timestamp('2020-10-13 0:43:37')
    ts2 = string2timestamp('2020-10-29 23:43:37')
    print('2020-10-13 0:43:37' ,ts1, timestamp2date_utc(ts1) )
    print('2020-10-29 23:43:37',ts2, timestamp2date_utc(ts2) )
    import sys
    print("Python Version {}".format(str(sys.version).replace('\n', '')))


    import django
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")
    django.setup() 

    from django.utils import timezone
    now = timezone.now()
    new = timezone.localtime(now)
    print(now, new)

