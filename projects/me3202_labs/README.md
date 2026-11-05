# ME3202 System Dynamics and Control lab study portfolio

**Student:** Gajendra | **Roll number:** 2301ME18 | **Institute:** Indian Institute of Technology Patna

**Course:** ME3202 System Dynamics and Control (supplied older manuals are labelled ME312)

Gajendra completed the ME3202 labs at IIT Patna. This folder is a fresh, reproducible **study portfolio**, not a copy of his original submitted lab reports. The lab manuals supplied the topics; the programs here generate their own illustrative inputs and outputs. They do not use a senior student's report or represent synthetic values as measured results.

The [lab index](lab_index.md) covers experiments 1-9. The runnable studies focus on the most relevant control and robotics topics:

| Lab | Study artifact | Run |
| --- | --- | --- |
| 3 | [DFT spectrum of a synthetic signal](fft_signal/) | `python projects/me3202_labs/fft_signal/fft_demo.py` |
| 6 | [Arduino Uno keypad and I2C LCD](arduino_keypad_lcd/) | Open the sketch in Arduino IDE with the listed libraries and hardware |
| 7 | [2-DOF manipulator PID simulation](two_link_pid/) | `python projects/me3202_labs/two_link_pid/simulate.py` |
| 8 | [DC motor PWM and PID study](../dc_motor_pid/) | `python projects/dc_motor_pid/dc_motor_pid.py` |
| 9 | [Transfer function root locus](root_locus/) | `python projects/me3202_labs/root_locus/root_locus_demo.py` |

The [study report](reports/ME3202_control_labs_study_report.md) summarizes methods, outputs, and limitations. Generated CSV files go to each study's ignored `results/` folder. It is a fresh portfolio report and should not be presented as the original graded submission.
