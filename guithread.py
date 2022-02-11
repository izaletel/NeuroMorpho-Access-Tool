from PySide6.QtCore import QRunnable, QObject, Signal


class WorkerSignals(QObject):

    finished = Signal()
    error = Signal(tuple)
    text = Signal(str)
    progress = Signal(float)


class GUIThread(QRunnable):
    def __init__(self):

        self.signals = WorkerSignals()
        QRunnable .__init__(self)

    def print_to_textbox(self, text):
        try:
            self.signals.text.emit(str(text))
        except Exception as e:
            print(e)

    def set_progress(self, value):
        self.signals.progress.emit(value)
