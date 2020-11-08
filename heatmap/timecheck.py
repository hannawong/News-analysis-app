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

<<<<<<< HEAD
def timestamp2date_utc(timeStamp):
    return datetime.datetime.utcfromtimestamp(timeStamp).date()

=======
>>>>>>> fe9186525d25bcd129fa621c4423d31f2a6b6d20

if __name__ == '__main__':
    # now's starttime and endtime
    ts1 = string2timestamp('2020-10-13 0:43:37')
    ts2 = string2timestamp('2020-10-29 23:43:37')
<<<<<<< HEAD
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

=======
    print('2020-10-13 0:43:37' ,ts1, timestamp2date(ts1) )
    print('2020-10-29 23:43:37',ts2, timestamp2date(ts2) )
    import sys
    print("Python Version {}".format(str(sys.version).replace('\n', '')))
    print(timestamp2date(1602621018), timestamp2date(1602521018))
# 1602621018 1602521018  转化结果是一样的  所以问题是之后都-1了？

# in lynn's pycharm
# 2020-10-13 0:43:37 1602521017.0 2020-10-13
# 2020-10-29 23:43:37 1603986217.0 2020-10-29
# Python Version 3.6.3 |Anaconda, Inc.| (default, Oct 15 2017, 03:27:45) [MSC v.1900 64 bit (AMD64)]
# in fwq the same?
# 2020-10-13 0:43:37 1602521017.0 2020-10-13
# 2020-10-29 23:43:37 1603986217.0 2020-10-29
# Python Version 3.8.5 (default, Jul 28 2020, 12:59:40) [GCC 9.3.0]
>>>>>>> fe9186525d25bcd129fa621c4423d31f2a6b6d20