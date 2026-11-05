"""ME3202 Lab 7 study: gravity-compensated PID for a planar two-link arm.

This is an independent educational simulation, not a record of a physical lab run.
Angles are in radians, time in seconds, torque in newton-metres.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


L1 = L2 = 0.5
M1 = M2 = 1.0
LC1 = LC2 = 0.25
I1 = I2 = M1 * L1 * L1 / 12
G = 9.81


def inertia_matrix(q2: float) -> tuple[float, float, float]:
    """Return the symmetric matrix entries M11, M12, M22."""
    m11 = I1 + I2 + M1 * LC1**2 + M2 * (L1**2 + LC2**2 + 2 * L1 * LC2 * math.cos(q2))
    m12 = I2 + M2 * (LC2**2 + L1 * LC2 * math.cos(q2))
    m22 = I2 + M2 * LC2**2
    return m11, m12, m22


def gravity(q1: float, q2: float) -> tuple[float, float]:
    g1 = (M1 * LC1 + M2 * L1) * G * math.sin(q1) + M2 * LC2 * G * math.sin(q1 + q2)
    g2 = M2 * LC2 * G * math.sin(q1 + q2)
    return g1, g2


def acceleration(q: list[float], dq: list[float], torque: list[float]) -> tuple[float, float]:
    m11, m12, m22 = inertia_matrix(q[1])
    coupling = M2 * L1 * LC2 * math.sin(q[1])
    c1 = -coupling * (2 * dq[0] * dq[1] + dq[1] ** 2)
    c2 = coupling * dq[0] ** 2
    g1, g2 = gravity(*q)
    viscous = 0.08
    b1 = torque[0] - c1 - g1 - viscous * dq[0]
    b2 = torque[1] - c2 - g2 - viscous * dq[1]
    determinant = m11 * m22 - m12 * m12
    if determinant <= 0:
        raise ValueError("Inertia matrix must be positive definite")
    return ((m22 * b1 - m12 * b2) / determinant,
            (-m12 * b1 + m11 * b2) / determinant)


def simulate(target: tuple[float, float] = (0.4, -0.25), duration: float = 3.0,
             dt: float = 0.002) -> list[tuple[float, ...]]:
    if duration <= 0 or dt <= 0 or dt > duration:
        raise ValueError("Use a positive duration and time step no longer than duration")
    q = [0.0, 0.0]
    dq = [0.0, 0.0]
    integral = [0.0, 0.0]
    kp, ki, kd = 12.0, 0.4, 2.5
    limit = 15.0
    rows: list[tuple[float, ...]] = []
    for step in range(round(duration / dt) + 1):
        time = step * dt
        error = [target[j] - q[j] for j in range(2)]
        for j in range(2):
            integral[j] = max(-1.0, min(1.0, integral[j] + error[j] * dt))
        compensation = gravity(*q)
        torque = [
            max(-limit, min(limit, compensation[j] + kp * error[j] + ki * integral[j] - kd * dq[j]))
            for j in range(2)
        ]
        rows.append((time, q[0], q[1], target[0], target[1], torque[0], torque[1]))
        ddq = acceleration(q, dq, torque)
        for j in range(2):
            dq[j] += ddq[j] * dt
            q[j] += dq[j] * dt
    return rows


def main() -> None:
    rows = simulate()
    output = Path(__file__).resolve().parent / "results" / "joint_response.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("time_s", "q1_rad", "q2_rad", "target_q1_rad", "target_q2_rad", "torque_1_Nm", "torque_2_Nm"))
        writer.writerows(rows)
    last = rows[-1]
    print(f"Final joint angles: q1={last[1]:.4f} rad, q2={last[2]:.4f} rad")
    print(f"Target: q1={last[3]:.4f} rad, q2={last[4]:.4f} rad")
    print(f"Absolute errors: {abs(last[3]-last[1]):.4f}, {abs(last[4]-last[2]):.4f} rad")
    print(f"CSV: {output}")


if __name__ == "__main__":
    main()
