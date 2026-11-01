"""Shared camera shot list (eye, target in cm, Z-up) for the DigitalTwin renders."""
SHOTS = [
    ("factory_floor",             (1500, -2700, 750), (-100, 200, 100)),
    ("production_line",           (650, -250, 420),   (-120, 230, 90)),
    ("asset_n02_pcb_router",      (330, -230, 300),   (-117, 150, 100)),
    ("asset_n03_feeder",          (120, 130, 260),    (-100, 275, 115)),
    ("machine_placement_closeup", (150, 330, 230),    (-110, 330, 100)),
]
# Factory navigation waypoints, ordered along the line: (name, note, eye, target)
WAYPOINTS = [
    ("Factory_Overview",        "Factory floor - whole hall with the production line in context.", (1500, -2700, 750), (-100, 200, 100)),
    ("Production_Line_Overview","Production Center - PL_001 main assembly line overview, N_01 to N_06.", (650, -250, 420), (-120, 230, 90)),
    ("N02_PCB_Router_Station",  "N_02 PCB Router - blue paint override from MaterialOverride.usd.", (330, -230, 300), (-117, 150, 100)),
    ("N03_Feeder_Station",      "N_03 Feeder - SCARA pick and place with conveyors.", (120, 130, 260), (-100, 275, 115)),
    ("N06_Test_Station",        "N_06 Test - end of the line.", (260, 470, 270), (-100, 490, 100)),
]
