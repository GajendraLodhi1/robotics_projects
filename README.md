# Robotics and engineering portfolio

Projects prepared from **Gajendra's** (IIT Patna roll number **2301ME18**) coursework and hackathon material. Each folder has its own instructions and a runnable example or source sketch. His course was **ME3202 System Dynamics and Control**; the supplied older lab manuals are headed ME312.

| Project | What runs | Scope |
| --- | --- | --- |
| [Cleaning robot route simulator](projects/cleaning_bot/) | A Python grid-coverage simulation with obstacles, coverage metrics and an [illustrated PDF report](projects/cleaning_bot/reports/cleaning_robot_route_study.pdf) | Software demonstration of the ATOMQUEST 2025 *proposal*. It is not a built physical robot. |
| [DC motor PID study](projects/dc_motor_pid/) | A Python simulation comparing fixed PWM and closed-loop PID control, with an [illustrated PDF report](projects/dc_motor_pid/reports/dc_motor_pid_study.pdf) | Independent educational reproduction of concepts used in the ME3202 lab. It is not measured motor data. |
| [Renewable dispatch case study](projects/renewable_dispatch/) | A fast standard-library dispatch demo and the original advanced notebook | All data in these examples are synthetic. The notebook is exploratory and has extra dependencies. |
| [ME3202 lab study portfolio](projects/me3202_labs/) | DFT spectrum, 2-DOF arm PID, and root-locus scripts; Arduino keypad/LCD sketch and [illustrated reports](reports/) | Independent study reproductions from the course manuals, without borrowed lab measurements. |

## Quick start

Use Python 3.10 or newer from the repository root:

```bash
python projects/cleaning_bot/simulator.py
python projects/dc_motor_pid/dc_motor_pid.py
python projects/renewable_dispatch/quick_demo.py
python projects/me3202_labs/fft_signal/fft_demo.py
python projects/me3202_labs/two_link_pid/simulate.py
python projects/me3202_labs/root_locus/root_locus_demo.py
```

The motor and renewable demos write CSV files to their own `results/` folders, which Git ignores. The cleaning demo prints its route summary. No paid service, API key, or hardware is needed for the quick demos.

## Source and attribution

- The cleaning bot proposal was submitted by Team Super Kings (Harsh Raj, Rakesh Hembram, and Gajendra) for ATOMQUEST 2025. The proposal PDF is retained in that project's `docs/` folder.
- The renewable case study notebook was supplied with the user's project files. Its generator creates synthetic hourly records; the repository does not claim measured grid results.
- The DC motor study code here was newly prepared to make the ME3202 concepts reproducible. The original course manuals and another student's reference reports are intentionally not republished.

The code and notes here are intended as a learning portfolio. If extending them, record what you personally changed, tested, and observed.

## Illustrated PDF reports

See the [report index](reports/) for four two-page PDFs, their diagram images, and a short guide to the Abstract, Methods and Work Completed sections. Regenerate the diagrams and PDFs with `python tools/build_robotics_reports.py` after installing `reportlab` and `Pillow`.
