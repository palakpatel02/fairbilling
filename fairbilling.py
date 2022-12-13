from datetime import datetime
from datetime import timedelta
from sys import argv

data = {}
eventtext = ['start', 'end']
validdata = []
def inputlinevalidated(line_content):
    try:
        if len(line_content) == 3 and isTimeFormat(line_content[0]) and line_content[1].isalnum() and eventtext.count(line_content[2].lower()) > 0:
            return 1
        else:
            return 0
    except:
        return 0
        
def isTimeFormat(inputtime):
    try:
        datetime.strptime(inputtime, '%H:%M:%S')
        return True
    except ValueError:
        return False
        
def load_file_data(file_path):
	lines = open(file_path, 'r').readlines()
	# lines = ['14:02:03 ALICE99 Start\n', '14:02:05 CHARLIE End\n', '14:02:34 ALICE99 End\n', '14:02:58 ALICE99 Start\n', '14:03:02 CHARLIE Start\n', '14:03:33 ALICE99 Start\n', '14:03:35 ALICE99 End\n', '14:03:37 CHARLIE End\n', '14:04:05 ALICE99 End\n', '14:04:23 ALICE99 End\n', '14:04:41 CHARLIE Start\n', '14:02:03 ALICE99 Started Python\n','14:04:42 JJJJJJJ End\n','14:04:42 Start\n','14:04:42 sss4544 Start\n','14:04:42 CHARLIE wrew\n','14:04:42 CH@RLI3 Start\n','14:04:42 ******* Start\n','99:04:42 CHARLIE Start\n']
	return [line.strip() for line in lines]

#reading input file name
arg1, arg2 = argv
file_data = load_file_data(arg2)

#valiadating each line and identifying keys(user) to loop through
for line in file_data:
    line_content = line.split(" ")
    if (inputlinevalidated(line_content) == 0):
        continue
    validdata.append(line)
    time, name, event = line_content[0], line_content[1], line_content[2]
    old_val = data.get(name, [])
    old_val.append({"time": time, "event": event})
    data[name] = old_val

#sorting the list
validdata.sort()

#getting overall start and end time from the list
sessionstart = datetime.strptime(validdata[0].split(' ')[0], '%H:%M:%S')
sessionend = datetime.strptime(validdata[-1].split(' ')[0], '%H:%M:%S')

#looping through each user
for key in data:
    startarr = []
    endarr = []
    sessioncount = 0
    totaltime = 0
    #creating event wise array
    for entry in data[key]:
        if entry['event'].lower() == 'start':
            startarr.append(entry['time'])
        elif entry['event'].lower() == 'end':
            endarr.append(entry['time'])
            
    i = 0
    j = 0
    while i < len(startarr) or j < len(endarr):
        if (len(startarr) > i and len(endarr) > j):
            start = datetime.strptime(startarr[i], '%H:%M:%S')
            end = datetime.strptime(endarr[j], '%H:%M:%S')
            if (end > start):
                sessioncount = sessioncount + 1
                totaltime = totaltime + (end - start).total_seconds()
                i = i + 1
                j = j + 1
            elif (end < start):
                sessioncount = sessioncount + 1
                start = sessionstart
                totaltime = totaltime + (end - start).total_seconds()
                j = j + 1
        elif (i == len(startarr) and len(endarr) > j):
            sessioncount = sessioncount + 1
            start = sessionstart
            end = datetime.strptime(endarr[j], '%H:%M:%S')
            totaltime = totaltime + (end - start).total_seconds()
            j = j + 1
        elif (len(startarr) > i and len(endarr) == j):
            sessioncount = sessioncount + 1
            start = datetime.strptime(startarr[i], '%H:%M:%S')
            end = sessionend
            totaltime = totaltime + (end - start).total_seconds()
            i = i + 1
        
    print(key,sessioncount,totaltime)

