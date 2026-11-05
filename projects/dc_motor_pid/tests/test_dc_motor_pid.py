import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dc_motor_pid import simulate  # noqa: E402


class MotorPidTests(unittest.TestCase):
    def test_pid_tracks_target_more_closely_than_fixed_pwm(self):
        samples = simulate()
        final = samples[-1]
        self.assertLess(abs(final.closed_loop_speed - final.target), 0.03)
        self.assertLess(abs(final.closed_loop_speed - final.target),
                        abs(final.open_loop_speed - final.target))

    def test_pwm_stays_inside_actuator_limits(self):
        self.assertTrue(all(0 <= sample.pid_pwm <= 1 for sample in simulate()))

    def test_invalid_time_step_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate(dt=1.0)


if __name__ == "__main__":
    unittest.main()
