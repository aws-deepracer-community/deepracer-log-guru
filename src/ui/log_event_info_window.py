import tkinter as tk
from src.event.event_meta import Event

class LogEventInfoWindow(tk.Toplevel):

    def __init__(self, parent):

        tk.Toplevel.__init__(self)

        self.title("Detailed Event Info")

        waypoint_frame = tk.LabelFrame(self, text="Closest Waypoint")
        state_frame = tk.LabelFrame(self, text="State")
        action_frame = tk.LabelFrame(self, text="Chosen Action")
        reward_frame = tk.LabelFrame(self, text="Reward")
        debug_frame = tk.LabelFrame(self, text="Log File Debug")

        waypoint_frame.grid(row=0, column=2, rowspan=2, pady=5, padx=5, sticky=tk.NW)
        state_frame.grid(row=0, column=1, rowspan=2, pady=5, padx=5, sticky=tk.NW)
        action_frame.grid(row=1, column=0, pady=5, padx=5, sticky=tk.NW)
        reward_frame.grid(row=0, column=0, pady=5, padx=5, sticky=tk.NW)
        debug_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky=tk.NW)

        self.waypoint_id = tk.StringVar()
        self.waypoint_bearing_to_next = tk.StringVar()
        self.waypoint_distance_to_next = tk.StringVar()
        self.waypoint_bearing_from_previous = tk.StringVar()
        self.waypoint_distance_from_previous = tk.StringVar()

        self.make_label_and_value(waypoint_frame, 0, "Waypoint", self.waypoint_id)
        self.make_label_and_value(waypoint_frame, 1, "Bearing to Next", self.waypoint_bearing_to_next)
        self.make_label_and_value(waypoint_frame, 2, "Distance to Next", self.waypoint_distance_to_next)
        self.make_label_and_value(waypoint_frame, 3, "Bearing from Previous", self.waypoint_bearing_from_previous)
        self.make_label_and_value(waypoint_frame, 4, "Distance from Previous", self.waypoint_distance_from_previous)

        self.state_progress = tk.StringVar()
        self.state_time = tk.StringVar()
        self.state_step = tk.StringVar()
        self.state_track_speed = tk.StringVar()
        self.state_bearing = tk.StringVar()
        self.state_side = tk.StringVar()
        self.state_distance_from_centre = tk.StringVar()
        self.state_all_wheels_on_track = tk.StringVar()

        self.make_label_and_value(state_frame, 0, "Progress", self.state_progress)
        self.make_label_and_value(state_frame, 1, "Time", self.state_time)
        self.make_label_and_value(state_frame, 2, "Step", self.state_step)
        self.make_label_and_value(state_frame, 3, "Track Speed", self.state_track_speed)
        self.make_label_and_value(state_frame, 4, "Bearing", self.state_bearing)
        self.make_label_and_value(state_frame, 5, "Side", self.state_side)
        self.make_label_and_value(state_frame, 6, "Distance from Centre", self.state_distance_from_centre)
        self.make_label_and_value(state_frame, 7, "All Wheels on Track", self.state_all_wheels_on_track)

        self.action_id = tk.StringVar()
        self.action_steering = tk.StringVar()
        self.action_speed = tk.StringVar()
        self.action_sequence = tk.StringVar()

        self.make_label_and_value(action_frame, 0, "Action", self.action_id)
        self.make_label_and_value(action_frame, 1, "Steering", self.action_steering)
        self.make_label_and_value(action_frame, 2, "Speed", self.action_speed)
        self.make_label_and_value(action_frame, 3, "Sequence", self.action_sequence)

        self.reward_value = tk.StringVar()
        self.reward_rank = tk.StringVar()
        self.reward_total = tk.StringVar()

        self.make_label_and_value(reward_frame, 0, "Reward", self.reward_value)
        self.make_label_and_value(reward_frame, 1, "Rank", self.reward_rank)
        self.make_label_and_value(reward_frame, 2, "Total so far", self.reward_total)

        self.debug_output = tk.StringVar()

        tk.Label(debug_frame, textvariable=self.debug_output, justify=tk.LEFT).grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        self.geometry("+%d+%d" % (parent.winfo_rootx(), parent.winfo_rooty()))

    def make_label_and_value(self, parent_frame, row, label, tk_variable):
        tk.Label(parent_frame, text=label + ":").grid(row=row, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Label(parent_frame, textvariable=tk_variable).grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)


    def show_event(self, event :Event):

        self.waypoint_id.set(str(event.closest_waypoint_index))
        self.waypoint_bearing_to_next.set("")
        self.waypoint_distance_to_next.set("")
        self.waypoint_bearing_from_previous.set("")
        self.waypoint_distance_from_previous.set("")

        self.state_progress.set(str(round(event.progress, 1)) + "  %")
        self.state_time.set(str(round(event.time_elapsed, 1)) + "  secs")
        self.state_step.set(str(event.step))
        self.state_track_speed.set(str(round(event.track_speed, 1)) + "  m/s")
        self.state_bearing.set(str(round(event.heading, 1)) + "  degrees")
        self.state_side.set("")
        self.state_distance_from_centre.set("")
        self.state_all_wheels_on_track.set(str(event.all_wheels_on_track))

        self.action_id.set(str(event.action_taken))
        self.action_steering.set(str(event.steering_angle) + "  degrees")
        self.action_speed.set(str(event.speed) + "  m/s")
        self.action_sequence.set("")

        self.reward_value.set(str(round(event.reward, 5)))
        self.reward_rank.set("")
        self.reward_total.set(str(round(event.reward_total, 5)))

        if event.debug_log:
            self.debug_output.set(event.debug_log)
        else:
            self.debug_output.set("")

        self.lift()