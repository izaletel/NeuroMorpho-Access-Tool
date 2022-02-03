import threading
from tkinter import INSERT, END


class GUIThread(threading.Thread):
    def __init__(self, progressbar='', progress_var='', textbox=''):

        self.progressbar, self.progress_var, self.textbox = progressbar, progress_var, textbox

        threading.Thread.__init__(self)

    def print_to_textbox(self, text):
        try:
            text = text + '\n'
            print(text)
            self.textbox.insert(INSERT, text)
            self.textbox.see(END)
            self.textbox.update_idletasks()
        except Exception as e:
            print(e)

    def set_progress(self, value):
        self.progress_var.set(value)
        self.progressbar.update_idletasks()
