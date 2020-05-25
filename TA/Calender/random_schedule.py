
import datetime

num_students = 18
start_time = "04/12/20 5:40pm"
stop_time = "04/12/20 8:30pm"

import numpy as np

def schedule(num_students,start_time,stop_time):
    formatStr =  "%m/%d/%y %H:%M"
    start_time_o = datetime.datetime.strptime(start_time ,formatStr)
    stop_time_o = datetime.datetime.strptime(stop_time , formatStr)
    total_time = stop_time_o- start_time_o
    ordered = np.random.choice(np.arange(0,num_students , 1) , num_students , replace=False)
    perSlot = total_time.seconds/num_students
    scheduleList  = []
    for i,n in enumerate(ordered):
        slot = start_time_o + datetime.timedelta(seconds=i*perSlot)
        slotStr = slot.strftime(formatStr)
        scheduleList.append((n,slotStr))
