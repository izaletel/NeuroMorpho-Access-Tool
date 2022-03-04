from PySide6.QtCore import QRunnable, QObject, Signal


class WorkerSignals(QObject):

    finished = Signal(tuple)
    error = Signal(tuple)
    text = Signal(str)
    progress = Signal(float)


class GUIThread(QRunnable):
    def __init__(self):
        self.is_paused = False
        self.is_killed = False
        self.signals = WorkerSignals()
        QRunnable .__init__(self)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def kill(self):
        self.is_killed = True

    def print_to_textbox(self, text):
        try:
            self.signals.text.emit(str(text))
        except Exception as e:
            print(e)

    def set_progress(self, value):
        self.signals.progress.emit(value)
