from queue import Queue
import time

class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)

class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.taskid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            result = task.run()
            time.sleep(0.5)
            self.schedule(task)

def foo():
    while True:
        print('foo()')
        yield

def bar():
    while True:
        print('bar()')
        yield

s = Scheduler()
s.new(foo())
s.new(bar())
s.mainloop()
