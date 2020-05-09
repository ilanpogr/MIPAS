from functools import partial

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QCoreApplication
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
    finished_store_searching = pyqtSignal()
    progress_changed = pyqtSignal(int)
    progress_pd_changed = pyqtSignal(int)
    status_sf_changed = pyqtSignal(str)
    status_pd_changed = pyqtSignal(str)
    task_sf_changed = pyqtSignal(str)
    task_pd_changed = pyqtSignal(str)
    switch_screen = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def execute(self):
        global main_window
        _translate = QCoreApplication.translate
        step = main_window.run_option
        self.progress_changed.connect(main_window.update_progress_bar_sf)
        self.progress_pd_changed.connect(main_window.update_progress_bar_pd)
        self.status_sf_changed.connect(main_window.update_status_sf)
        self.status_pd_changed.connect(main_window.update_status_pd)
        self.task_sf_changed.connect(main_window.update_task_sf)
        self.task_pd_changed.connect(main_window.update_task_pd)
        self.switch_screen.connect(main_window.switch_to_parallel_screen)
        self.finished.connect(main_window.finished_crawler)
        if step == 0:
            Controller.search_stores(self.progress_changed, self.status_sf_changed, self.task_sf_changed)
            step += 1
            self.finished_store_searching.emit()
        self.switch_screen.emit()
        if step == 1:
            Controller.download_products(self.progress_pd_changed, self.status_pd_changed, self.task_pd_changed)
            step += 1
        # NEXT TODO - RUN PRODUCT DOWNLOADER AND THEN CREATE PARALLEL READER WRITER FOR IM
        self.finished.emit()
        self.thread.quit()


class WorkerImageMatcher(Worker):
    finished = pyqtSignal()
    progress_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    task_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def execute(self):
        global main_window
        _translate = QCoreApplication.translate
        self.progress_changed.connect(main_window.update_progress_bar_im)
        self.status_changed.connect(main_window.update_status_im)
        self.task_changed.connect(main_window.update_task_im)
        # NEXT TODO - implement second thread

        self.finished.emit()
        self.thread.quit()


class ThreadController(Thread):
    def __init__(self, _main):
        global main_window
        super().__init__(_main)
        self.threads = {}
        main_window = _main
        self._main.start_btn.clicked.connect(self.start_thread)

        # Workers
        self.worker_crawler = WorkerCrawler()
        self.worker_im = WorkerImageMatcher()

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
        print("done")
        # next_index = main_window.stackedWidget.currentIndex() + 1
        main_window.stackedWidget.setCurrentIndex(0)  # for mockup!!! todo - delete.

    @pyqtSlot(bool)
    def start_thread(self):
        signals = {self.worker_crawler.finished_store_searching: self.finished_looking_for_stores}
        self._threaded_call(self.worker_crawler, self.worker_crawler.execute, signals=signals)

    @pyqtSlot()
    def finished_looking_for_stores(self):
        print("finished downloading products")
        # signals = {self.worker_im.finished: self._receive_finish_signal}
        # self._threaded_call(self.worker_im, self.worker_im.execute, signals=signals)


