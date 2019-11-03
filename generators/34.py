from queue import Queue
import time
import socket
import select

class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None
        self.exc = None

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
        self.read_waiting = {}
        self.write_waiting = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.taskid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def exit(self, task):
        if task.exc:
            print(f'Task {task} had terminated with an exception: {task.exc}')
        else:
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

    def wait_for_read(self, task, fd):
        self.read_waiting[fd] = task

    def wait_for_write(self, task, fd):
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [], timeout)
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))
            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(0)
            yield

    def mainloop(self):
        self.new(self.iotask())

        while self.taskmap:
            task = self.ready.get()

            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            except Exception as e:
                task.exc = e
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

class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.wait_for_read(self.task, fd)

class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.wait_for_write(self.task, fd)

def AsyncAccept(sock):
    yield ReadWait(sock)
    return sock.accept()

def AsyncRecv(sock, maxbytes):
    yield ReadWait(sock)
    return sock.recv(maxbytes)

def AsyncSend(sock, buffer):
    while buffer:
        yield WriteWait(sock)
        length = sock.send(buffer)
        buffer = buffer[length:]

def handle_client(client, addr):
    print(f'Connection from: {addr}')
    raise RuntimeError('client exception')
    while True:
        data = yield from AsyncRecv(client, 65536)
        if not data:
            break
        yield from AsyncSend(client, data)
    client.close()
    print(f'Client closed: {addr}')
    yield

def server(port):
    print('Server starting')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.setblocking(0)
    sock.bind(('127.0.0.1', port))
    sock.listen(5)
    while True:
        client, addr = yield from AsyncAccept(sock)
        #client.setblocking(0)
        yield NewTask(handle_client(client, addr))

s = Scheduler()
s.new(server(55555)) # But it is the blocking operation
s.mainloop()
