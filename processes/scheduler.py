#!/usr/bin/env python

import time
import schedule

from rq import Queue
from worker import conn

#import metricsproc
import imp
metricsproc = imp.load_source(
    'metricsproc',
    '/home/nfs/lariatdqm/app/dqm-v2/dqm-v2/processes/metricsproc.py'
    )

q = Queue(connection=conn)

#def job():
#    print("I'm working...")

def update_metrics():
    result = q.enqueue(metricsproc.update_metrics)
    return

if __name__ == '__main__':

    #schedule.every(10).minutes.do(job)
    #schedule.every().hour.do(job)
    #schedule.every().day.at("10:30").do(job)
    #schedule.every().monday.do(job)
    #schedule.every().wednesday.at("13:15").do(job)

    schedule.every(1).minutes.do(update_metrics)

    while True:
        schedule.run_pending()
        time.sleep(1)

