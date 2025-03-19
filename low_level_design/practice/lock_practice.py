import threading

class Lock:
    def __init__(self):
        self.hm = {}
    def add_to_hm(self, val):
        lock = threading.Lock()
        lock.acquire()
        self.hm[val] = True
        lock.release()

l = Lock()
l.add_to_hm(1)
l.add_to_hm(2)
print(l.hm)