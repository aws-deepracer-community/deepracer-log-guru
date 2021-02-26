import tkinter as tk

from src.event.event_meta import Event
from src.tracks.track import Track

from src.action_space.action_util import is_right_turn, is_left_turn
from src.utils.formatting import get_pretty_small_float, get_pretty_large_float, get_pretty_large_integer

class LogEventInfoWindow(tk.Toplevel):

    def __init__(self, parent):

        tk.Toplevel.__init__(self)

        self.title("Detailed Event Info")

        waypoint_frame = tk.LabelFrame(self, text="Closest Waypoint")
        state_frame = tk.LabelFrame(self, text="State")
        action_frame = tk.LabelFrame(self, text="Chosen Action")
        reward_frame = tk.LabelFrame(self, text="Reward")
        debug_frame = tk.LabelFrame(self, text="Log File Debug")

        waypoint_frame.grid(row=0, column=2, rowspan=2, pady=5, padx=5, sticky=tk.NW+tk.E)
        state_frame.grid(row=0, column=1, rowspan=2, pady=5, padx=5, sticky=tk.NW+tk.E)
        action_frame.grid(row=1, column=0, pady=5, padx=5, sticky=tk.NW+tk.E)
        reward_frame.grid(row=0, column=0, pady=5, padx=5, sticky=tk.NW+tk.E)
        debug_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky=tk.NW+tk.E)

        self.waypoint_id = tk.StringVar()
        self.waypoint_lap_position = tk.StringVar()
        self.waypoint_bearing_to_next = tk.StringVar()
        self.waypoint_distance_to_next = tk.StringVar()
        self.waypoint_bearing_from_previous = tk.StringVar()
        self.waypoint_distance_from_previous = tk.StringVar()

        self.make_label_and_value(waypoint_frame, 0, "Waypoint", self.waypoint_id)
        self.make_label_and_value(waypoint_frame, 1, "Lap Position", self.waypoint_lap_position)
        self.make_label_and_value(waypoint_frame, 2, "Bearing to Next", self.waypoint_bearing_to_next)
        self.make_label_and_value(waypoint_frame, 3, "Distance to Next", self.waypoint_distance_to_next)
        self.make_label_and_value(waypoint_frame, 4, "Bearing from Previous", self.waypoint_bearing_from_previous)
        self.make_label_and_value(waypoint_frame, 5, "Distance from Previous", self.waypoint_distance_from_previous)

        self.state_progress = tk.StringVar()
        self.state_time = tk.StringVar()
        self.state_step = tk.StringVar()
        self.state_track_speed = tk.StringVar()
        self.state_progress_speed = tk.StringVar()
        self.state_heading = tk.StringVar()
        self.state_true_bearing = tk.StringVar()
        self.state_slide = tk.StringVar()
        self.state_side = tk.StringVar()
        self.state_distance_from_centre = tk.StringVar()
        self.state_all_wheels_on_track = tk.StringVar()

        self.make_label_and_value(state_frame, 0, "Progress", self.state_progress)
        self.make_label_and_value(state_frame, 1, "Time", self.state_time)
        self.make_label_and_value(state_frame, 2, "Step", self.state_step)
        self.make_label_and_value(state_frame, 3, "Track Speed", self.state_track_speed)
        self.make_label_and_value(state_frame, 4, "Progress Speed", self.state_progress_speed)
        self.make_label_and_value(state_frame, 5, "Heading", self.state_heading)
        self.make_label_and_value(state_frame, 6, "True Bearing", self.state_true_bearing)
        self.make_label_and_value(state_frame, 7, "Slide", self.state_slide)
        self.make_label_and_value(state_frame, 8, "Side", self.state_side)
        self.make_label_and_value(state_frame, 9, "Distance from Centre", self.state_distance_from_centre)
        self.make_label_and_value(state_frame, 10, "All Wheels on Track", self.state_all_wheels_on_track)

        self.action_id = tk.StringVar()
        self.action_steering = tk.StringVar()
        self.action_speed = tk.StringVar()
        self.action_sequence = tk.StringVar()

        self.make_label_and_value(action_frame, 0, "Action", self.action_id)
        self.make_label_and_value(action_frame, 1, "Steering", self.action_steering)
        self.make_label_and_value(action_frame, 2, "Speed", self.action_speed)
        self.make_label_and_value(action_frame, 3, "Sequence", self.action_sequence)

        self.reward_value = tk.StringVar()
        self.reward_average = tk.StringVar()
        self.reward_total = tk.StringVar()

        self.make_label_and_value(reward_frame, 0, "Reward", self.reward_value)
        self.make_label_and_value(reward_frame, 1, "Average so far", self.reward_average)
        self.make_label_and_value(reward_frame, 2, "Total so far", self.reward_total)

        self.debug_output = tk.StringVar()

        tk.Label(debug_frame, textvariable=self.debug_output, justify=tk.LEFT, font='TkFixedFont').grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        self.geometry("+%d+%d" % (parent.winfo_rootx(), parent.winfo_rooty()))

    def make_label_and_value(self, parent_frame, row, label, tk_variable):
        tk.Label(parent_frame, text=label + ":").grid(row=row, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Label(parent_frame, textvariable=tk_variable).grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)


    def show_event(self, event :Event, track :Track):

        (next_bearing, next_distance) = track.get_bearing_and_distance_to_next_waypoint(event.closest_waypoint_index)
        (prev_bearing, prev_distance) = track.get_bearing_and_distance_from_previous_waypoint(event.closest_waypoint_index)

        self.waypoint_id.set(str(event.closest_waypoint_index))
        self.waypoint_lap_position.set(str(round(track.get_waypoint_percent_from_race_start(event.closest_waypoint_index), 1)) + "  %")
        self.waypoint_bearing_to_next.set(str(round(next_bearing)))
        self.waypoint_distance_to_next.set(str(round(next_distance, 2)) + " m")
        self.waypoint_bearing_from_previous.set(str(round(prev_bearing)))
        self.waypoint_distance_from_previous.set(str(round(prev_distance, 2)) + " m")

        self.state_progress.set(str(round(event.progress, 1)) + "  %")
        self.state_time.set(str(round(event.time_elapsed, 1)) + "  secs")
        self.state_step.set(str(event.step))
        self.state_track_speed.set(str(round(event.track_speed, 1)) + "  m/s")
        self.state_progress_speed.set(str(round(event.progress_speed, 1)) + "  m/s")
        self.state_heading.set(str(round(event.heading)))
        self.state_true_bearing.set(str(round(event.true_bearing)))
        self.state_slide.set(str(round(event.slide)))
        self.state_side.set(track._get_position_of_point_relative_to_waypoint((event.x, event.y), event.closest_waypoint_index))
        self.state_distance_from_centre.set("")
        self.state_all_wheels_on_track.set(str(event.all_wheels_on_track))

        self.action_id.set(str(event.action_taken))
        self.action_steering.set(get_formatted_steering(event.steering_angle))
        self.action_speed.set(str(event.speed) + "  m/s")
        self.action_sequence.set("")

        self.reward_value.set(get_pretty_large_float(round(event.reward, 5)))
        self.reward_average.set(get_pretty_large_integer(event.average_reward_so_far))
        self.reward_total.set(get_pretty_large_integer(event.reward_total))

        if event.debug_log:
            self.debug_output.set(event.debug_log[:1000])
        else:
            self.debug_output.set("")

        self.lift()

def get_formatted_steering(steering_angle):
    if is_right_turn(steering_angle):
        return "RIGHT " + get_pretty_small_float(abs(steering_angle), 30, 1)
    elif is_left_turn(steering_angle):
        return "LEFT " + get_pretty_small_float(abs(steering_angle), 30, 1)
    else:
        return "AHEAD"