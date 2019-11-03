from queue import Queue
import time

class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def close(self):
        self.target.close()

    def run(self):
        result = self.target.send(self.sendval)
        self.sendval = None
        return result

class SystemCall:
    def handle(self):
        pass

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

    def exit(self, task):
        print(f'Task {task} had terminated')
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
                time.sleep(0.5)
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)

class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)

class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid)
        if task:
            task.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)

def foo():
    tid = yield GetTid()
    for i in range(1, 30):
        print(f'[{tid}]: foo()')
        yield

def main():
    child = yield NewTask(foo())
    tid = yield GetTid()
    for i in range(1, 3):
        print(f'[{tid}]: main()')
        yield
    result = yield KillTask(child)
    print(f'Main done: {result}')

s = Scheduler()
s.new(main())
s.mainloop()
