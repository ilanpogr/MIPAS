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
        self.b = rwlock.RWLockFairD()
        self.a_reader_lock = self.a.gen_rlock()
        self.a_writer_lock = self.a.gen_wlock()

        self.b_reader_lock = self.b.gen_rlock()
        self.b_writer_lock = self.b.gen_wlock()

    def read(self, file, line_index):
        with self.a_reader_lock:
            f = open(file)
            lines = f.readlines()
            if line_index >= len(lines):
                return None
            else:
                return lines[line_index]

    def write(self, file, content):
        with self.a_writer_lock:
            with open(file, 'a') as f:
                f.write(content + '\n')

    def read_results(self, file):
        with self.b_reader_lock:
            f = open(file)
            return f.readlines()

    def save_results(self, file, tmp_file):
        with self.b_writer_lock:
            os.remove(file)
            os.rename(tmp_file, file)
