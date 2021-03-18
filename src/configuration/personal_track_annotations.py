from src.graphics.track_annotations import Dot, Line, Cone, Route, RoutePoint, WorldDot

# Annotate each track with your personal indications for best route etc.
# Copy the syntax from the example shown here for the original DeepRacer track



reinvent_2018_annotations = [
    Dot(7, "L", 0, "green"),
    Dot(7, "L", 0.1, "yellow"),
    Dot(7, "R", 0.1, "yellow"),
    Dot(7, "L", 0.2, "red"),
    Dot(7, "R", 0.2, "red"),
    Line(22, "L", 0.25, "magenta", 154, 5),
    Cone(50, "R", 0.1, "orange", -100, 3, 10),
    WorldDot(6, 2, "white"),

    Route("grey", [
        RoutePoint(8, "L", 0.15, "R", 0.15),
        RoutePoint(10, "L", 0.2, "R", 0.1),
        RoutePoint(11, "L", 0.22, "R", 0.08),
        RoutePoint(12, "L", 0.24, "R", 0.06),
        RoutePoint(13, "L", 0.26, "R", 0.04),
        RoutePoint(14, "L", 0.28, "R", 0.02),
        RoutePoint(15, "L", 0.30, "R", 0.00),
        RoutePoint(16, "L", 0.30, "R", 0.00),
        RoutePoint(17, "L", 0.30, "R", 0.00),
        RoutePoint(18, "L", 0.30, "L", 0.05),
        RoutePoint(21, "L", 0.30, "L", 0.10),

    ])

    # 160 to 145    from wp 25




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

american_speedway_annotations = [
    Dot(2, "L", 0.01, "yellow"),
    Dot(2, "R", 0.3, "magenta"),

    Dot(6, "R", 0.1, "yellow"),
    Dot(6, "R", 0.3, "magenta"),

    Dot(15, "L", 0.7, "yellow"),
    Dot(15, "L", 0.4, "magenta"),

    Line(15, "L", 0.55, "orange", 36, 6),

    Dot(24, "R", 0.3, "yellow"),
    Dot(24, "R", 0.6, "magenta"),

    Dot(35, "R", 0.0, "yellow"),
    Dot(35, "R", 0.5, "magenta"),

    Dot(50, "R", 0.3, "yellow"),
    Dot(50, "R", 0.6, "magenta"),

    Line(50, "R", 0.45, "orange", -14.5, 6),

    Dot(61, "L", 0.2, "yellow"),
    Dot(61, "R", 0.2, "magenta"),

    Dot(70, "L", 0.6, "yellow"),
    Dot(70, "L", 0.3, "magenta"),

    Dot(80, "L", 0.2, "yellow"),
    Dot(80, "R", 0.4, "magenta"),

    Dot(87, "L", 0.7, "yellow"),
    Dot(87, "L", 0.4, "magenta"),

    Dot(97, "R", 0.1, "yellow"),
    Dot(97, "R", 0.5, "magenta"),

    Dot(105, "R", 0.1, "yellow"),
    Dot(105, "R", 0.4, "magenta"),

    Dot(115, "R", 0.1, "yellow"),
    Dot(115, "R", 0.3, "magenta"),

    Dot(128, "L", 0.7, "yellow"),
    Dot(128, "L", 0.4, "magenta"),

    Dot(136, "R", 0.4, "yellow"),
    Dot(136, "R", 0.7, "magenta"),

    Dot(149, "L", 0.7, "yellow"),
    Dot(149, "L", 0.05, "magenta"),

    Dot(160, "R", 0.1, "yellow"),
    Dot(160, "R", 0.5, "magenta"),

    Dot(170, "R", 0.1, "yellow"),
    Dot(170, "R", 0.5, "magenta"),

    Dot(180, "L", 0.15, "yellow"),
    Dot(180, "R", 0.5, "magenta"),

    Dot(190, "L", 0.6, "yellow"),
    Dot(190, "L", 0.1, "magenta"),

    Dot(200, "L", 0.7, "yellow"),
    Dot(200, "L", 0.4, "magenta"),

    Dot(210, "R", 0.1, "yellow"),
    Dot(210, "R", 0.3, "magenta"),

    Dot(220, "R", 0.1, "yellow"),
    Dot(220, "R", 0.3, "magenta"),


]

asia_pacific_bay_loop_annotations = []

european_seaside_circuit_annotations = [
    Line(12, "R", 0.65, "orange", -3, 7),
    Line(44, "L", 0.65, "orange", 57, 4),
    Line(71, "R", 0.5, "orange", -95, 2.5),
    Line(92, "L", 0.52, "orange", 8, 2.5),
    Line(124, "R", 0.3, "orange", 178.5, 9.5),
    Line(176, "L", 0.3, "orange", -98, 4.5),
    Line(217, "R", 0.55, "orange", 90, 2),
    Line(226, "R", 0.5, "orange", 69, 4),

]

european_seaside_circuit_annotations_V1 = [

    Route("grey", [
        RoutePoint(0, "R", 0, "R", 0.6),
        RoutePoint(4, "R", 0, "R", 0.6),
        RoutePoint(7, "R", 0, "R", 0.6),
        RoutePoint(9, "R", 0, "R", 0.6),
        RoutePoint(11, "R", 0, "R", 0.6),
        RoutePoint(13, "R", 0, "R", 0.6),
        RoutePoint(15, "R", 0, "R", 0.6)]),

    Route("grey", [
        RoutePoint(18, "L", 0.25, "R", 0.25),
        RoutePoint(31, "L", 0.25, "R", 0.25)]),

    Route("grey", [
        RoutePoint(33, "L", 0, "L", 0.6),
        RoutePoint(35, "L", 0, "L", 0.6),
        RoutePoint(37, "L", 0, "L", 0.6),
        RoutePoint(39, "L", 0, "L", 0.6),
        RoutePoint(41, "L", 0, "L", 0.6),
        RoutePoint(43, "L", 0, "L", 0.6),
        RoutePoint(45, "L", 0, "L", 0.6),
        RoutePoint(47, "L", 0, "L", 0.6)]),

    Route("grey", [
        RoutePoint(51, "L", 0.25, "R", 0.25),
        RoutePoint(53, "L", 0.25, "R", 0.25),
        RoutePoint(55, "L", 0.25, "R", 0.25),
        RoutePoint(57, "L", 0.25, "R", 0.25)]),

    Route("grey", [
        RoutePoint(59, "R", 0, "R", 0.6),
        RoutePoint(61, "R", 0, "R", 0.6),
        RoutePoint(63, "R", 0, "R", 0.6),
        RoutePoint(65, "R", 0, "R", 0.6),
        RoutePoint(67, "R", 0, "R", 0.6),
        RoutePoint(69, "R", 0, "R", 0.6),
        RoutePoint(71, "R", 0, "R", 0.6),
        RoutePoint(73, "R", 0, "R", 0.6),
        RoutePoint(75, "R", 0, "R", 0.6),
        RoutePoint(77, "R", 0, "R", 0.6)]),

    Route("grey", [
        RoutePoint(78, "L", 0, "L", 0.6),
        RoutePoint(80, "L", 0, "L", 0.6),
        RoutePoint(82, "L", 0, "L", 0.6),
        RoutePoint(84, "L", 0, "L", 0.6),
        RoutePoint(86, "L", 0, "L", 0.6),
        RoutePoint(88, "L", 0, "L", 0.6),
        RoutePoint(90, "L", 0, "L", 0.6),
        RoutePoint(92, "L", 0, "L", 0.6)]),

    Route("grey", [
        RoutePoint(99, "R", 0, "R", 0.6),
        RoutePoint(101, "R", 0, "R", 0.6),
        RoutePoint(103, "R", 0, "R", 0.6),
        RoutePoint(105, "R", 0, "R", 0.6),
        RoutePoint(107, "R", 0, "R", 0.6),
        RoutePoint(109, "R", 0, "R", 0.6),
        RoutePoint(111, "R", 0, "R", 0.6),
        RoutePoint(113, "R", 0, "R", 0.6),
        RoutePoint(115, "R", 0, "R", 0.6),
        RoutePoint(117, "R", 0, "R", 0.6),
        RoutePoint(119, "R", 0, "R", 0.6),
        RoutePoint(121, "R", 0, "R", 0.6),
        RoutePoint(123, "R", 0, "R", 0.6),
        RoutePoint(125, "R", 0, "R", 0.6),
        RoutePoint(127, "R", 0, "R", 0.6)]),

    Route("grey", [
        RoutePoint(145, "R", 0, "R", 0.6),
        RoutePoint(147, "R", 0, "R", 0.6),
        RoutePoint(149, "R", 0, "R", 0.6),
        RoutePoint(151, "R", 0, "R", 0.6),
        RoutePoint(153, "R", 0, "R", 0.6),
        RoutePoint(155, "R", 0, "R", 0.6)]),

    Route("grey", [
        RoutePoint(159, "L", 0, "L", 0.6),
        RoutePoint(161, "L", 0, "L", 0.6),
        RoutePoint(163, "L", 0, "L", 0.6),
        RoutePoint(165, "L", 0, "L", 0.6),
        RoutePoint(167, "L", 0, "L", 0.6),
        RoutePoint(169, "L", 0, "L", 0.6),
        RoutePoint(171, "L", 0, "L", 0.6),
        RoutePoint(173, "L", 0, "L", 0.6),
        RoutePoint(175, "L", 0, "L", 0.6),
        RoutePoint(177, "L", 0, "L", 0.6),
        RoutePoint(179, "L", 0, "L", 0.6),
        RoutePoint(181, "L", 0, "L", 0.6),
        RoutePoint(183, "L", 0, "L", 0.6),
        RoutePoint(185, "L", 0, "L", 0.6),
        RoutePoint(187, "L", 0, "L", 0.6),
        RoutePoint(189, "L", 0, "L", 0.6),
        RoutePoint(191, "L", 0, "L", 0.6)]),

    Route("grey", [
        RoutePoint(193, "R", 0, "R", 0.6),
        RoutePoint(195, "R", 0, "R", 0.6),
        RoutePoint(197, "R", 0, "R", 0.6),
        RoutePoint(199, "R", 0, "R", 0.6),
        RoutePoint(201, "R", 0, "R", 0.6),
        RoutePoint(203, "R", 0, "R", 0.6),
        RoutePoint(205, "R", 0, "R", 0.6),
        RoutePoint(207, "R", 0, "R", 0.6),
        RoutePoint(209, "R", 0, "R", 0.6),
        RoutePoint(211, "R", 0, "R", 0.6),
        RoutePoint(213, "R", 0, "R", 0.6),
        RoutePoint(215, "R", 0, "R", 0.6),
        RoutePoint(217, "R", 0, "R", 0.6),
        RoutePoint(219, "R", 0, "R", 0.6),
        RoutePoint(221, "R", 0, "R", 0.6),
        RoutePoint(223, "R", 0, "R", 0.6),
        RoutePoint(225, "R", 0, "R", 0.6),
        RoutePoint(227, "R", 0, "R", 0.6),
        RoutePoint(229, "R", 0, "R", 0.6),
        RoutePoint(231, "R", 0, "R", 0.6),
        RoutePoint(233, "R", 0, "R", 0.6)]),


    Dot(18, "L", 0.8, "green"), Dot(31, "L", 0.8, "green"),Dot(31, "L", 1, "green"),
    Dot(32, "L", 0.8, "red"), Dot(47, "L", 0.8, "red"), Dot(47, "L", 1, "red"),
    Dot(55, "L", 0.8, "red"), Dot(63, "L", 0.8, "red"), Dot(63, "L", 1, "red"),
    Dot(80, "L", 0.8, "red"), Dot(84, "L", 0.8, "red"), Dot(84, "L", 1, "red"),
    Dot(98, "L", 0.8, "red"), Dot(102, "L", 0.8, "red"), Dot(102, "L", 1, "red"),
    Dot(112, "L", 0.8, "green"), Dot(159, "L", 0.8, "green"), Dot(159, "L", 1, "green"),
    Dot(161, "L", 0.8, "red"), Dot(173, "L", 0.8, "red"), Dot(173, "L", 1, "red"),
    Dot(176, "L", 0.8, "green"), Dot(191, "L", 0.8, "green"), Dot(191, "L", 1, "green"),
    Dot(213, "L", 0.8, "green"), Dot(5, "L", 0.8, "green"), Dot(5, "L", 1, "green"),


]

# 6-8 R
# 49-51 L
# 96-97 R
# 133-134 L
# 184-186 R
# 229-231 L

