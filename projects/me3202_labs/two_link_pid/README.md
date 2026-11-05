# Lab 7 study: 2-DOF planar manipulator PID

**Gajendra | 2301ME18 | ME3202, IIT Patna**

This independent Python model follows the two-link dynamics described in the course Lab 7 manual: `M(q) qdd + C(q, qd) qd + G(q) = torque`. It applies gravity compensation and joint PID to a step target. Link lengths, masses, gains and torques are illustrative. The output is **simulation data**, not measurements from the IIT Patna lab.

The [illustrated project report](reports/two_link_arm_pid_study.pdf) explains the abstract, method, completed work and joint-response plot.

```bash
python projects/me3202_labs/two_link_pid/simulate.py
python projects/me3202_labs/two_link_pid/tests/test_simulate.py
```

The script writes `results/joint_response.csv` with both joint angles, targets and torques. Plot the angles against time, then vary the gains in `simulate.py` to compare settling and overshoot. To reproduce the original MATLAB/Simulink exercise, implement step, ramp and sinusoidal references there and compare trajectories.
