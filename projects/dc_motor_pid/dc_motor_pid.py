"""Compare fixed PWM and PID on a simplified, normalized DC motor model."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Sample:
    time_s: float
    target: float
    open_loop_speed: float
    closed_loop_speed: float
    pid_pwm: float


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def simulate(
    *, target: float = 0.70, fixed_pwm: float = 0.45, duration: float = 4.0,
    dt: float = 0.02, kp: float = 1.6, ki: float = 3.5, kd: float = 0.03,
    gain: float = 1.0, time_constant: float = 0.55,
) -> list[Sample]:
    if not (0 <= target <= 1 and 0 <= fixed_pwm <= 1):
        raise ValueError("target and fixed_pwm must be between 0 and 1")
    if min(duration, dt, gain, time_constant) <= 0:
        raise ValueError("duration, dt, gain and time_constant must be positive")
    if dt > time_constant:
        raise ValueError("dt must be smaller than the motor time constant")

    open_speed = closed_speed = integral = previous_speed = 0.0
    samples: list[Sample] = []
    steps = int(round(duration / dt))
    for step in range(steps + 1):
        time_s = step * dt
        error = target - closed_speed
        derivative = -(closed_speed - previous_speed) / dt
        raw_pwm = kp * error + ki * integral + kd * derivative
        pwm = clamp(raw_pwm, 0.0, 1.0)
        samples.append(Sample(time_s, target, open_speed, closed_speed, pwm))

        # Conditional integration reduces windup while the actuator is saturated.
        if (0 < raw_pwm < 1) or (raw_pwm >= 1 and error < 0) or (raw_pwm <= 0 and error > 0):
            integral += error * dt
        previous_speed = closed_speed
        open_speed += dt * (gain * fixed_pwm - open_speed) / time_constant
        closed_speed += dt * (gain * pwm - closed_speed) / time_constant
    return samples


def write_csv(samples: list[Sample], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("time_s", "target", "open_loop_speed", "closed_loop_speed", "pid_pwm"))
        for sample in samples:
            writer.writerow((sample.time_s, sample.target, sample.open_loop_speed,
                             sample.closed_loop_speed, sample.pid_pwm))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=float, default=0.70)
    parser.add_argument("--kp", type=float, default=1.6)
    parser.add_argument("--ki", type=float, default=3.5)
    parser.add_argument("--kd", type=float, default=0.03)
    args = parser.parse_args()
    samples = simulate(target=args.target, kp=args.kp, ki=args.ki, kd=args.kd)
    output = Path(__file__).resolve().parent / "results" / "motor_response.csv"
    write_csv(samples, output)
    last = samples[-1]
    print(f"Fixed PWM final speed: {last.open_loop_speed:.3f}")
    print(f"PID final speed:       {last.closed_loop_speed:.3f}")
    print(f"Target speed:          {last.target:.3f}")
    print(f"CSV: {output}")


if __name__ == "__main__":
    main()
