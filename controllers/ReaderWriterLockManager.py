from readerwriterlock import rwlock
import os

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LockManager(metaclass=Singleton):
    def __init__(self):
        self.a = rwlock.RWLockFairD()
        self.a_reader_lock = self.a.gen_rlock()
        self.a_writer_lock = self.a.gen_wlock()

    def read(self, file, line_index):
        print("STARTED reading file...")
        with self.a_reader_lock:
            f = open(file)
            lines = f.readlines()
            print("NUM OF LINES IN FILE: " + str(len(lines)))
            print("FINISHED reading file...")
            if line_index > len(lines):
                return None
            else:
                return lines[line_index]

    def write(self, file, content):
        with self.a_writer_lock:
            with open(file, 'a') as f:
                f.write(content + '\n')
