import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quick_demo import Hour, dispatch, synthetic_hours  # noqa: E402


class DispatchTests(unittest.TestCase):
    def test_battery_stays_inside_limits(self):
        rows = dispatch(synthetic_hours())
        self.assertTrue(all(10 <= row.battery_kwh <= 100 for row in rows))

    def test_surplus_charges_then_curtailed(self):
        rows = dispatch([Hour(80, 0, 20)], initial_kwh=50, efficiency=1)
        self.assertEqual(rows[0].battery_kwh, 70)
        self.assertEqual(rows[0].curtailed_kwh, 40)

    def test_deficit_discharge_then_unmet(self):
        rows = dispatch([Hour(0, 0, 60)], initial_kwh=20, minimum_kwh=10,
                        efficiency=1)
        self.assertEqual(rows[0].battery_kwh, 10)
        self.assertEqual(rows[0].unmet_kwh, 50)


if __name__ == "__main__":
    unittest.main()
