# Cleaning robot route simulator

This is a **software simulation** based on Team Super Kings' circular, quadrant-based cleaning robot proposal for ATOMQUEST 2025. The [team proposal](docs/ATOMQUEST_2025_cleaning_bot_proposal.pdf) describes brush, vacuum, and mop modules with a removable dust compartment. The simulation below only demonstrates route coverage and obstacle avoidance. It does not model cleaning physics or prove that hardware was built.

The [illustrated project report](reports/cleaning_robot_route_study.pdf) explains the abstract, route method, completed work and generated diagrams.

## Run

From the repository root:

```bash
python projects/cleaning_bot/simulator.py
python projects/cleaning_bot/simulator.py --map projects/cleaning_bot/example_map.txt
python projects/cleaning_bot/tests/test_simulator.py
```

Map symbols: `.` is a traversable cell and `#` is an obstacle. The robot starts at the first open cell unless `--start X,Y` is supplied. The program searches for the closest uncleaned reachable cell, walks to it, and reports coverage. Unreachable areas are reported separately.

## What to study

1. Read `shortest_path_to_uncleaned()` to see how breadth-first search avoids obstacles.
2. Change the map and compare route length with the number of reachable cells.
3. Add a simulated battery limit or a return-to-dock rule, then write a test showing what happens.
4. If you build the real robot later, add actual circuit diagrams, photos, measurements, and a clear division of team contributions.
