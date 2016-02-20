from datetime import datetime, timedelta

def round_time(date_time=None, round_to=60):
    """
    Round a datetime object to any time lapse in seconds

        date_time: datetime.datetime object, default now.
        round_to:  Closest number of seconds to round to,
                   default 1 minute.
    """
    if date_time == None:
        date_time = datetime.now()
    seconds = (date_time - date_time.min).seconds
    #rounding = (seconds+round_to/2) // round_to * round_to  # default
    #rounding = (seconds + round_to) // round_to * round_to  # round up
    rounding = seconds // round_to * round_to               # round down
    return date_time + timedelta(0, rounding-seconds, -date_time.microsecond)

def date_time_bins(start_date_time, number_bins, bin_width=60):
    date_time = round_time(start_date_time, bin_width)
    time_delta = timedelta(seconds=bin_width)
    date_time_bins = [
        date_time - timedelta(seconds=(bin_width * i))
        for i in xrange(number_bins)
        ]
    return date_time_bins

if __name__ == '__main__':

    date_time = datetime.now()

    x = date_time_bins(date_time, 100, 60)
    y = date_time_bins(date_time, 100, -60)

    print date_time, round_time(date_time)

    for i in xrange(60):
        print x[i], y[i]

    u = datetime.now()
    v = datetime.now() - timedelta(minutes=0, seconds=10, microseconds=0)

    print
    print "Testing..."
    print
    print u, v

    u = round_time(u)
    v = round_time(v)

    print
    print u, v
    print
    print u == v

