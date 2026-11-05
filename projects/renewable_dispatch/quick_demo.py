"""A small renewable and battery dispatch simulation using synthetic data."""

from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Hour:
    wind_kwh: float
    solar_kwh: float
    demand_kwh: float


@dataclass(frozen=True)
class Dispatch:
    hour: int
    generation_kwh: float
    demand_kwh: float
    battery_kwh: float
    unmet_kwh: float
    curtailed_kwh: float


def synthetic_hours(count: int = 72, seed: int = 42) -> list[Hour]:
    if count <= 0:
        raise ValueError("count must be positive")
    rng = random.Random(seed)
    records = []
    for hour in range(count):
        daily = hour % 24
        wind = max(0.0, 24 + 8 * math.sin(hour / 7) + rng.uniform(-4, 4))
        solar = max(0.0, 45 * math.sin(math.pi * (daily - 6) / 12))
        demand = max(0.0, 48 + 7 * math.sin(math.pi * daily / 12) + rng.uniform(-3, 3))
        records.append(Hour(wind, solar, demand))
    return records


def dispatch(
    records: list[Hour], *, capacity_kwh: float = 100.0,
    power_limit_kwh: float = 20.0, initial_kwh: float = 50.0,
    minimum_kwh: float = 10.0, efficiency: float = 0.95,
) -> list[Dispatch]:
    if not (capacity_kwh > 0 and power_limit_kwh > 0 and
            0 <= minimum_kwh <= initial_kwh <= capacity_kwh and 0 < efficiency <= 1):
        raise ValueError("Invalid battery parameters")
    battery = initial_kwh
    output = []
    for index, record in enumerate(records):
        if min(record.wind_kwh, record.solar_kwh, record.demand_kwh) < 0:
            raise ValueError("Hourly energy values cannot be negative")
        generation = record.wind_kwh + record.solar_kwh
        balance = generation - record.demand_kwh
        unmet = curtailed = 0.0
        if balance >= 0:
            stored = min(balance * efficiency, power_limit_kwh, capacity_kwh - battery)
            battery += stored
            curtailed = balance - stored / efficiency
        else:
            withdrawn = min(-balance / efficiency, power_limit_kwh, battery - minimum_kwh)
            battery -= withdrawn
            unmet = -balance - withdrawn * efficiency
        output.append(Dispatch(index, generation, record.demand_kwh, battery,
                               max(0.0, unmet), max(0.0, curtailed)))
    return output


def main() -> None:
    records = synthetic_hours()
    rows = dispatch(records)
    destination = Path(__file__).resolve().parent / "results" / "dispatch.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("hour", "generation_kwh", "demand_kwh", "battery_kwh",
                         "unmet_kwh", "curtailed_kwh"))
        for row in rows:
            writer.writerow((row.hour, row.generation_kwh, row.demand_kwh,
                             row.battery_kwh, row.unmet_kwh, row.curtailed_kwh))
    print(f"Hours simulated: {len(rows)}")
    print(f"Unmet demand: {sum(row.unmet_kwh for row in rows):.2f} kWh")
    print(f"Curtailed energy: {sum(row.curtailed_kwh for row in rows):.2f} kWh")
    print(f"CSV: {destination}")


if __name__ == "__main__":
    main()
