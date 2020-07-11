# closest waypoint
# 	waypoint #
# 	heading from previous
# 	distance from previous
# 	heading to next
# 	distance to next
# state
# 	progress %
# 	elapsed time
# 	track speed
# 	heading
# 	L/R
# 	distance from centre
# 	all wheels on track
#
# action
# 	id
# 	steering
# 	speed
#
# reward
# 	reward
#
#
# debug

import tkinter as tk
from src.event.event_meta import Event

class LogEventInfoWindow(tk.Toplevel):

    def __init__(self, parent):

        tk.Toplevel.__init__(self)

        self.title("Action Info")

        self.message_widget = tk.Message(self, width=800)
        self.message_widget.pack()

        self.geometry("+%d+%d" % (parent.winfo_rootx(), parent.winfo_rooty()))

    def show_event(self, event :Event):
        info = "Waypoint = #" + str(event.closest_waypoint_index)
        info += "\nReward = " + str(event.reward)
        info += "\nAction = " + str(event.speed) + " m/s "
        info += "   turning " + str(event.steering_angle) + " degrees"

        if event.debug_log:
            info += "\n\nDEBUG:\n" + event.debug_log

        self.message_widget.configure(text=info)
        self.lift()