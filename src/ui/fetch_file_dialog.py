import traceback
from tkinter import Label, Entry, messagebox, StringVar, Radiobutton, W, LEFT

from src.aws.log_file import fetch_log_file
# from src.log.parse import create_meta_file
from src.ui.dialog import Dialog
from src.ui.please_wait import PleaseWaitDialog
from src.log.log import Log

class FetchFileDialog(Dialog):

    def body(self, master):

        Label(master, text="Enter the FULL name of the log file stream:").pack(anchor=W)
        self.stream_name_entry = Entry(master, width=110)
        self.stream_name_entry.pack(anchor=W)

        Label(master).pack()

        Label(master, text="OPTIONAL - Provide a description:").pack(anchor=W)
        self.description_entry = Entry(master, width=70)
        self.description_entry.pack(anchor=W)

        Label(master).pack()

        Label(master, text="Indicate the type of log file:").pack(anchor=W)
        self.radio_button_value = StringVar()
        self.radio_button_value.set("NT")
        Radiobutton(master, text="Normal Training", variable=self.radio_button_value, value="NT").pack(anchor=W,side=LEFT)
        Radiobutton(master, text="Normal Evaluation", variable=self.radio_button_value, value="NE").pack(anchor=W,side=LEFT)
        Radiobutton(master, text="Virtual Race Evaluation", variable=self.radio_button_value, value="VR").pack(anchor=W,side=LEFT)

        return self.stream_name_entry

    def apply(self):
        please_wait = PleaseWaitDialog(self.parent)
        try:
            stream_full_name = self.stream_name_entry.get()

            prefix = stream_full_name.split("/", 1)[0]
            log_file_name = prefix + "_" + self.radio_button_value.get() + ".log"

            if self.radio_button_value.get() == "VR":
                log_group = "/aws/deepracer/leaderboard/SimulationJobs"
            else:
                log_group = "/aws/robomaker/SimulationJobs"

            fetch_log_file(stream_full_name, log_group, log_file_name)

            new_log = Log()
            new_log.parse(log_file_name, self.description_entry.get())
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
        value = self.stream_name_entry.get()
        if len(value) > 90 and value.startswith("sim-") and "/" in value and "SimulationApplicationLogs" in value:
            return True
        else:
            messagebox.showerror("Fetch File", "Invalid stream name format")
            return False
