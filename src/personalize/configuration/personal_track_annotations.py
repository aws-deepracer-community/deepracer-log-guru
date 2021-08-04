#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.graphics.track_annotations import Dot, Line, Cone, Route, RoutePoint, WorldDot

# Annotate each track with your personal indications for best route etc.
# Copy the syntax from the example shown here for the original DeepRacer track



reinvent_2018_annotations = [
    Dot(15, "L", 0, "green"),
    Dot(15, "L", 0.12, "yellow"),
    Dot(15, "R", 0.12, "yellow"),
    Dot(15, "L", 0.24, "red"),
    Dot(15, "R", 0.24, "red"),
    Line(37, "L", 0.25, "magenta", 154, 5),
    Cone(81, "R", 0.1, "orange", -100, 3, 10),
    WorldDot(6, 2, "white"),

    Route("grey", [
        RoutePoint(16, "L", 0.15, "R", 0.15),
        RoutePoint(22, "L", 0.2, "R", 0.1),
        RoutePoint(24, "L", 0.22, "R", 0.08),
        RoutePoint(26, "L", 0.24, "R", 0.06),
        RoutePoint(28, "L", 0.26, "R", 0.03),
        RoutePoint(30, "L", 0.28, "R", 0.00),
        RoutePoint(32, "L", 0.30, "L", 0.03),
        RoutePoint(34, "L", 0.32, "L", 0.06),
        RoutePoint(36, "L", 0.34, "L", 0.09),

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

cumulo_turnpike_annotations = []

stratus_loop_annotations = []

bowtie_annotations = []

american_speedway_annotations = []

asia_pacific_bay_loop_annotations = []

european_seaside_circuit_annotations = []

po_chun_speedway_annotations = []

po_chun_super_speedway_annotations = []

lars_loop_annotations = []

lars_circuit_annotations = []

kuei_raceway_annotations = []

kuei_super_raceway_annotations = []

cosmic_loop_annotations = []

cosmic_circuit_annotations = []

baja_highway_annotations = []

baja_turnpike_annotations = []

hot_rod_speedway_annotations = []

hot_rod_super_speedway_annotations = []

reinvent_2018_wide_annotations = []