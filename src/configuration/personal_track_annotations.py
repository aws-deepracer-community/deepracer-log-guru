from src.graphics.track_annotations import Dot, Line, Cone, Route, RoutePoint

# Annotate each track with your personal indications for best route etc.
# Copy the syntax from the example shown here for the original DeepRacer track

reinvent_2018_annotations = [
    Dot(7, "L", 0, "green"),
    Dot(7, "L", 0.1, "yellow"),
    Dot(7, "R", 0.1, "yellow"),
    Dot(7, "L", 0.2, "red"),
    Dot(7, "R", 0.2, "red"),
    Line(22, "L", 0.3, "magenta", 155, 5),
    Cone(50, "R", 0.1, "orange", -100, 3, 10),

    Route("grey", [
        RoutePoint(10, "L", 0.2, "R", 0.1),
        RoutePoint(11, "L", 0.11, "R", 0.2),
        RoutePoint(12, "L", 0.1, "R", 0.25),
        RoutePoint(13, "L", 0.01, "R", 0.3)
    ])


]

championship_cup_2019_annotations = []

roger_raceway_annotations = []

fumiaki_loop_annotations = []

summit_raceway_annotations = []

sola_2020_annotations = []

baadal_2020_annotations = []

barcelona_annotations = []

yun_speedway_annotations = []


