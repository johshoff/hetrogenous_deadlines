#!/usr/bin/python

'''Generate calendar files from Due Date page on the Hetrogenous Parallel Programming course on coursera.

The `data` string is simply the raw paste chrome gave me when copying the table.

Author: Johannes Hoff
'''

from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

data='''Quiz: Week #1
Monday, January 19
Monday, February 2
Lab Tour with Device Query Code
Wednesday, January 28
Wednesday, February 11
Lab: Vector Addition
Wednesday, January 28
Wednesday, February 11
 Quiz: Week #2
 Monday, January 26
Monday, February 9
Lab: Basic Matrix-Matrix Multiplication
Wednesday, February 4
Friday, February 20
Lab: Tiled Matrix-Matrix Multiplication
Wednesday, February 4
Friday, February 20
Quiz: Week #3
 Monday, February 2
Monday, February 16
Lab: Image Convolution
Wednesday, February 11
Wednesday, February 25
Quiz: Week #4
Monday, February 9
Monday, February 23
Lab: List Reduction
Wednesday, February 18
Wednesday, March 4
Quiz: Week #5
Monday, February 16
Monday, March 2
Lab: List Scan
Wednesday, February 25
Wednesday, March 11
Quiz: Week #6
Monday, February 23
Monday, March 9
Lab: Histogram
Wednesday, March 4
Wednesday, March 18
Quiz: Week #7
Monday, March 2
Monday, March 16
Lab: Vector Addition with Streams (Extra Credit)
Wednesday, March 11
Wednesday, March 25
Quiz: Week #8
Monday, March 9
Monday, March 23
Lab: OpenCL Vector Addition (Extra Credit)
Wednesday, March 18
Wednesday, April 1 '''

def datify(datestr):
    basic = datetime.strptime(datestr.split(',')[1].strip(), '%B %d')
    return datetime(2015, basic.month, basic.day, 17, 00, tzinfo=pytz.timezone('US/Central'))

def make_event(name, deadline):
    hour = timedelta(0, 60 * 60)
    nowish = datetime(2015, 2, 23)

    event = Event()
    event.add('summary', name)
    event.add('dtstart', deadline - hour)
    event.add('dtend',   deadline)
    event.add('dtstamp', nowish)
    return event

def make_calendar(summary, event_names, deadlines):
    calendar = Calendar()
    calendar['summary'] = summary

    for name, deadline in zip(event_names, deadlines):
        calendar.add_component(make_event(name, deadline))

    return calendar

def write_calendar(calendar, outfile):
    import os
    with open(outfile, 'wb') as out:
        out.write(calendar.to_ical())

names, soft, hard = (map(str.strip, data.split('\n')[i::3]) for i in xrange(3))
soft_dates, hard_dates = (map(datify, list) for list in [soft, hard])


write_calendar(make_calendar('Soft due dates Heterogeneous Parallel Programming', names, soft_dates), 'output/soft.ics')
write_calendar(make_calendar('Hard due dates Heterogeneous Parallel Programming', names, hard_dates), 'output/hard.ics')

