def grep(pattern):
    while True:
        line = (yield)
        if pattern in line:
            print(line)

g = grep("python")
g.send(None)
g.send("java is cool")
g.send("python is cool")
