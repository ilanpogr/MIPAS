from functools import partial
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from controllers.runController import start_button_clicked

main_window = None


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None


class Thread(QObject):
    def __init__(self, _main):
        super().__init__()
        self._main = _main


class WorkerNewSearch(Worker):
    finished = pyqtSignal()
    progress_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def execute(self):
        global main_window
        self.progress_changed.connect(main_window.update_progress_bar)
        start_button_clicked(self.progress_changed)
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
        self.worker1 = WorkerNewSearch()
        #self.worker2 = WorkerTwo()

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

        # Can now apply cross-thread signals/slots
        #worker.signals.connect(self.slots)
        if signals:
            for signal, slot in signals.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)

        #self.signals.connect(worker.slots)
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
    def _receive_signal(self):
        print("Final Signal received.")

    # @pyqtSlot()
    # def _receive_signal_to_progress(self):
    #     print()

    @pyqtSlot(bool)
    def start_thread(self):
        signals = {self.worker1.finished: self._receive_signal}
                   # self.worker1.progress_changed: self._receive_signal_to_progress}
        self._threaded_call(self.worker1, self.worker1.execute, signals=signals)
