import time

def follow(file):
    '''Linux tail like function'''
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

logfile = open("/tmp/log")

for line in follow(logfile):
    print(line)
