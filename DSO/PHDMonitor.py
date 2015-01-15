# Michael A. Phillips' PHD2 Star Lost Monitor
# Added to by andy.galasso@gmail.com 2014.11.14 - JSON
#
#!/usr/bin/env python

import datetime, socket, sys, json

host = '127.0.0.1'
port = 4400

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    s.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()

print 'Connected to PHD'
print
print
print "Looking for PHD2 'Star Lost' events on your PHD2..."
print
for l in s.makefile() :
    m = json.loads(l)
    if 'Event' in m and m['Event'] == 'StarLost' :
        print 'Star Lost at time= ' + str(datetime.datetime.fromtimestamp(m['Timestamp']))
        
#Extended info
import datetime
from collections import deque

threshold = 4
queue = deque()
for l in s.makefile() :
    # fill the queue
    record = json.loads(l)
    try:
        if record['Event'] == 'StarLost':
            timestamp = datetime.datetime.fromtimestamp(record['Timestamp'])
            print('Star Lost at time {}.'.format(timestamp.isoformat()))
            queue.append((timestamp, record))
    except KeyError:
        pass # there was no 'Event' in the record
    # clear the queue from old records
    try:
        while queue[0][0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
            queue.popleft()
    except IndexError:
        pass # there are no records in the queue.
    # analyze the queue
    if len(queue) > threshold:
        print('There were more than {} events over the last minute!'.format(threshold))
