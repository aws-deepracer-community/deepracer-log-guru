import tkinter as tk
import tkinter.messagebox

from src.ui.dialog import Dialog
from src.ui.please_wait_OLD import PleaseWaitDialog
from src.log.log import get_possible_new_model_log_files, import_new_logs
from src.ui.please_wait import PleaseWait

class NewFilesDialog(Dialog):

    def __init__(self, parent, please_wait :PleaseWait):
        self.new_log_files = get_possible_new_model_log_files()
        self.please_wait = please_wait

        super().__init__(parent, "Import New Log Files")

    def body(self, master):

        if self.new_log_files:
            tk.Label(master, text="The following new log files were found:").pack(anchor=tk.W, pady=10)

            for f in self.new_log_files:
                tk.Label(master, text="        " + f).pack(anchor=tk.W, pady=2)

            tk.Label(master, text="Click OK to import them now").pack(anchor=tk.W, pady=10)
        else:
            tk.Label(master, text="No new log files were found").pack()

    def apply(self):
        try:
            import_new_logs(self.new_log_files, self.please_wait)
        except:
            self.please_wait.stop()
            tk.messagebox.showerror("Fetch File", "Unable to import all files")
        else:
            self.please_wait.stop(0.2)
            tk.messagebox.showinfo("Fetch File", "Import succeeded")
            pass

