"""Grid-coverage demonstration for the ATOMQUEST cleaning bot concept.

This is a route-planning simulation, not software for physical hardware.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MAP = (
    "..........#..",
    "..##......#..",
    "......#......",
    "..#...#..##..",
    "..#..........",
    "......##.....",
)
Point = tuple[int, int]


@dataclass(frozen=True)
class CoverageReport:
    path: tuple[Point, ...]
    cleaned: frozenset[Point]
    reachable_count: int
    open_count: int

    @property
    def coverage_percent(self) -> float:
        return 100.0 * len(self.cleaned) / self.reachable_count


def validate_grid(grid: tuple[str, ...]) -> None:
    if not grid or not grid[0]:
        raise ValueError("Map must contain at least one cell")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("All map rows must have the same width")
    if any(char not in ".#" for row in grid for char in row):
        raise ValueError("Use only '.' for floor and '#' for obstacles")
    if all(char == "#" for row in grid for char in row):
        raise ValueError("Map has no open floor cell")


def neighbors(grid: tuple[str, ...], point: Point):
    x, y = point
    for nx, ny in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == ".":
            yield (nx, ny)


def reachable_cells(grid: tuple[str, ...], start: Point) -> set[Point]:
    seen = {start}
    queue = deque([start])
    while queue:
        for nxt in neighbors(grid, queue.popleft()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def shortest_path_to_uncleaned(
    grid: tuple[str, ...], start: Point, cleaned: set[Point]
) -> list[Point] | None:
    """Return an obstacle-free path to the nearest uncleaned reachable cell."""
    queue = deque([start])
    parent: dict[Point, Point | None] = {start: None}
    while queue:
        point = queue.popleft()
        if point not in cleaned:
            route = [point]
            while parent[point] is not None:
                point = parent[point]  # type: ignore[assignment]
                route.append(point)
            return list(reversed(route))
        for nxt in neighbors(grid, point):
            if nxt not in parent:
                parent[nxt] = point
                queue.append(nxt)
    return None


def simulate(grid: tuple[str, ...], start: Point | None = None) -> CoverageReport:
    validate_grid(grid)
    if start is None:
        start = next((x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == ".")
    x, y = start
    if not (0 <= y < len(grid) and 0 <= x < len(grid[0])) or grid[y][x] != ".":
        raise ValueError("Start must be an open cell inside the map")

    reachable = reachable_cells(grid, start)
    cleaned = {start}
    path = [start]
    current = start
    while len(cleaned) < len(reachable):
        route = shortest_path_to_uncleaned(grid, current, cleaned)
        if route is None:
            raise RuntimeError("A reachable cell could not be routed to")
        for point in route[1:]:
            path.append(point)
            cleaned.add(point)
        current = route[-1]

    return CoverageReport(
        path=tuple(path),
        cleaned=frozenset(cleaned),
        reachable_count=len(reachable),
        open_count=sum(row.count(".") for row in grid),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, help="Text map with '.' and '#' cells")
    parser.add_argument("--start", help="Start coordinate as X,Y (zero-based)")
    args = parser.parse_args()
    grid = tuple(args.map.read_text(encoding="utf-8").splitlines()) if args.map else DEFAULT_MAP
    start = tuple(map(int, args.start.split(","))) if args.start else None
    if start is not None and len(start) != 2:
        parser.error("--start must be X,Y")
    report = simulate(grid, start)  # type: ignore[arg-type]
    for row in grid:
        print(row)
    print(f"Cleaned reachable cells: {len(report.cleaned)}/{report.reachable_count}")
    print(f"Unreachable open cells: {report.open_count - report.reachable_count}")
    print(f"Coverage of reachable floor: {report.coverage_percent:.1f}%")
    print(f"Move count: {len(report.path) - 1}")


if __name__ == "__main__":
    main()
