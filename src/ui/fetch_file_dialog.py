import traceback
from tkinter import Label, Entry, messagebox, StringVar, Radiobutton, W, LEFT

from src.aws.log_file import fetch_log_file
# from src.log.parse import create_meta_file
from src.ui.dialog import Dialog
from src.ui.please_wait import PleaseWaitDialog
from src.log.log import Log

class FetchFileDialog(Dialog):

    def __init__(self, parent):

        self.stream_name = StringVar()

        # For future expansion, NT = "Normal Training"
        self.radio_button_value = StringVar()
        self.radio_button_value.set("NT")
        
        super().__init__(parent, "Fetch Log File From AWS")

    def body(self, master):

        Label(master, text="Enter the FULL name of the log file stream:").pack(anchor=W)
        stream_name_entry = Entry(master, textvariable=self.stream_name, width=110)
        stream_name_entry.pack(anchor=W)

        return stream_name_entry

    def apply(self):
        please_wait = PleaseWaitDialog(self.parent)
        try:
            stream_full_name = self.stream_name.get()

            if stream_full_name.endswith("\n"):
                stream_full_name = stream_full_name[:-1]

            prefix = stream_full_name.split("/", 1)[0]
            log_file_name = prefix + "_" + self.radio_button_value.get() + ".log"

            if self.radio_button_value.get() == "VR":
                log_group = "/aws/deepracer/leaderboard/SimulationJobs"
            else:
                log_group = "/aws/robomaker/SimulationJobs"

            fetch_log_file(stream_full_name, log_group, log_file_name)

            new_log = Log()
            new_log.parse(log_file_name)
            new_log.save()

            please_wait.destroy()
        except:
            please_wait.destroy()
            messagebox.showerror("Fetch File", "Unable to fetch file from AWS")
            traceback.print_exc()
        else:
            messagebox.showinfo("Fetch File", "Download succeeded!")
            pass   # Parse the new file received

    def validate(self):
        value = self.stream_name.get()
        if len(value) > 90 and value.startswith("sim-") and "/" in value and "SimulationApplicationLogs" in value:
            return True
        else:
            messagebox.showerror("Fetch File", "Invalid stream name format")
            return False
