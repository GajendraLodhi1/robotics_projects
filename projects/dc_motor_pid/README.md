# DC motor speed control study

This small Python model revisits the control ideas used in IIT Patna's ME3202 DC motor lab. It compares fixed PWM duty with a closed-loop PID controller for a simple first-order motor model. The model is educational: its speeds are normalized and are **not physical measurements from the lab**.

The [illustrated project report](reports/dc_motor_pid_study.pdf) explains the abstract, model, completed work and response plot.

## Run

```bash
python projects/dc_motor_pid/dc_motor_pid.py
python projects/dc_motor_pid/tests/test_dc_motor_pid.py
```

The script writes `results/motor_response.csv` for plotting in Excel, MATLAB, or Python. It prints the final open-loop and closed-loop speeds.

## Model

The simulated motor follows `d(speed)/dt = (gain * PWM - speed) / time_constant`. The controller calculates speed error from the target and uses proportional, integral, and derivative terms to choose PWM in the range 0 to 1. This is a simplified model of the lab's PWM and PID ideas, not a validated motor plant.

Try changing `--target`, `--kp`, `--ki`, and `--kd`, then plot the CSV. For an interview, explain how overshoot, steady-state error, saturation, sensor failure, and noisy speed feedback would affect a real system.
