import os
from functools import partial

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QApplication

import controllers.runController as Controller

import time

main_window = None


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None


class Thread(QObject):
    def __init__(self, _main):
        super().__init__()
        self._main = _main


class WorkerCrawler(Worker):
    finished = pyqtSignal()
    start_image_matching = pyqtSignal()
    started = pyqtSignal(int)
    status_search = pyqtSignal(str)
    status_download = pyqtSignal(str)
    task_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def connect_signals(self):
        self.started.connect(main_window.start_timer)
        self.task_changed.connect(main_window.change_task)
        self.status_download.connect(main_window.explore_stores)
        self.status_search.connect(main_window.search_for_stores)

    @pyqtSlot(str)
    def execute(self):
        self.connect_signals()
        counter = 3
        time.sleep(1)
        for i in range(4):
            time.sleep(1)
            self.started.emit(counter)
            counter -= 1
        Controller.search_stores(self.status_search)
        self.task_changed.emit(True)
        Controller.download_products(self.start_image_matching, self.status_download)
        self.finished.emit()
        self.thread.quit()


class WorkerImageMatcher(Worker):
    finished = pyqtSignal()
    status_changed = pyqtSignal(str)
    up_to_date = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def connect_signals(self):
        self.status_changed.connect(main_window.explore_stores)
        self.finished.connect(main_window.run_finished)

    @pyqtSlot(str)
    def execute_parallel(self):
        self.connect_signals()
        Controller.compare_images(self.status_changed, int(main_window.num_of_stores))
        self.finished.emit()
        self.thread.quit()


class ThreadController(Thread):
    def __init__(self, _main):
        global main_window
        super().__init__(_main)
        self.threads = {}
        main_window = _main

        self.counter_im = 0
        self.all_modules_finished = 0

        # Workers
        self.worker_crawler = WorkerCrawler()
        self.worker_im = WorkerImageMatcher()
        self.start_thread()

    def _threaded_call(self, worker, fn, *args, signals=None, slots=None):
        thread = QThread()
        thread.setObjectName('thread_' + worker.__class__.__name__)
        # store because garbage collection
        self.threads[worker] = thread
        # give worker thread so it can be quit()
        worker.thread = thread
        # objects stay on threads after thread.quit()
        # need to move back to main thread to recycle the same Worker.
        # Error is thrown about Worker having thread (0x0) if you don't do this
        worker.moveToThread(QThread.currentThread())
        # move to newly created thread
        worker.moveToThread(thread)
        worker.moveToThread(thread)
        # Can now apply cross-thread signals/slots
        if signals:
            for signal, slot in signals.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)
        if slots:
            for slot, signal in slots.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)
        thread.started.connect(partial(fn, *args))  # fn needs to be slot
        thread.start()

    @pyqtSlot()
    def _receive_finish_signal(self):
        print("thread finish notification")
        self.all_modules_finished += 1
        if self.all_modules_finished % 2 == 0:
            os.remove("resources/app_files/downloaded_stores_multi_threading.txt")
            self.start_thread()

    @pyqtSlot(bool)
    def start_thread(self):

        print("Active threads:")
        for worker, t in self.threads.items():
            print(str(type(worker)) + ": " + str(t.isRunning()))

        signals = {self.worker_crawler.start_image_matching: self.start_image_matching_thread,
                   self.worker_crawler.finished: self._receive_finish_signal}
        self._threaded_call(self.worker_crawler, self.worker_crawler.execute, signals=signals)

    @pyqtSlot()
    def start_image_matching_thread(self):
        print("starting image matching")
        signals = {self.worker_im.finished: self._receive_finish_signal}
        self._threaded_call(self.worker_im, self.worker_im.execute_parallel, signals=signals)

