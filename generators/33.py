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
        self.exit_waiting = {}

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

        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def wait_for_exit(self, task, wait_tid):
        if wait_tid in self.taskmap:
            self.exit_waiting.setdefault(wait_tid, []).append(task)
            return True
        else:
            return False

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

class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.wait_for_exit(self.task, self.tid)
        self.task.sendval = result
        if not result:
            self.sched.schedule(self.task)

def handle_client(client, addr):
    print(f'Connection from: {addr}')
    while True:
        data = client.recv(65536)
        if not data:
            break
        client.send(data)
    client.close()
    print(f'Client closed: {addr}')
    yield

def server(port):
    print('Server starting')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', port))
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        yield NewTask(client, addr)

s = Scheduler()
s.new(server()) # But it is the blocking operation
s.mainloop()
