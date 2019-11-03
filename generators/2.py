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

def grep(pattern, lines):
    '''Linux grep like function'''
    for line in lines:
        if pattern in line:
            yield line

logfile = open("/tmp/log")
loglines = follow(logfile)
greplines = grep("python", loglines)

for line in greplines:
    print(line)
