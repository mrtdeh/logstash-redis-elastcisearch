#!/usr/bin/python app.py

import pyinotify
import re
import os
import redis
import json
import time

print("start app")

r = redis.StrictRedis(host='redis', port=6379, db=0)
regex = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'
fields = ['ip','ui','usr','@timestamp','method','rline','ver','status','size']

wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY



class EventHandler (pyinotify.ProcessEvent):

    def __init__(self, file_path, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = 0
        logpats = r'I2G\(JV\)'
        self._logpat = re.compile(logpats)
        self.fetch_lines()
    
    def process_IN_MODIFY(self, event):
        self.fetch_lines(msg="Apped")

    def send_to_redis(self,data):
        # simple function to convert file rows to json records and send its to redis
        x = len(data)
        def toJson(inp):
            m = re.match(regex,inp)
            if m:
                data1 = m.groups(0)
                data2 = dict(zip(fields,data1))
                j = json.dumps(data2)
                return j
        for i in range(0,x-1):
            r.lpush("logstash",toJson(data[i]))
               

    def fetch_lines(self,msg=""):
        research=True
        # this while use for file check exist or not,
        # if not exist try again for checking after 5 seconds while file created.
        while research:
            # if this try has a error, mean file not exist and go to on FileNotFoundError
            try:
                if self._last_position > os.path.getsize(self.file_path):
                    self._last_position = 0
                research=False
                print("file Path : ",self.file_path)
            # if file not exist try again after 5 seconds
            except FileNotFoundError:
                research=True
                print("File not found, research after 5 seconds")
                time.sleep(5)
            # when file exist and do normaly
            else:
                with open(self.file_path) as f:
                    f.seek(self._last_position)
                    loglines = f.readlines()
                    self._last_position = f.tell()
                    if(len(loglines) > 0):
                        
                        print ("fetch_lines : ",msg)
                        print(loglines)
                        self.send_to_redis(loglines)
                        
        


path = os.getenv("LOGSOURCE")
if(not path): path = './example_accesss.log'

handler = EventHandler(path)
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch(handler.file_path, mask)        
notifier.loop()


