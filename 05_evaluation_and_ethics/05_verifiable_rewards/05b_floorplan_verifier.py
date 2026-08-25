"""Demo: a program-based verifier for a structured, spatial output (a
floor plan), instead of a metric formula or a second model.

See 05b_floorplan_verifier.md for the full explanation.
The same verifier idea as 05_math_verifier.py, applied to constraints
that have nothing to do with text overlap: no two rooms may occupy the
same space, and every room needs a door.
"""

Rect = tuple[float, float, float, float]  # (x1, y1, x2, y2)
Door = tuple[str, str]  # (room_a, room_b) sharing a wall with a door cut into it


def rooms_overlap(a: Rect, b: Rect) -> bool:
    """True if rectangles a and b share more than just a touching edge."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    x_overlap = min(ax2, bx2) - max(ax1, bx1)
    y_overlap = min(ay2, by2) - max(ay1, by1)
    return x_overlap > 0 and y_overlap > 0


def shares_wall(a: Rect, b: Rect) -> bool:
    """True if rectangles a and b touch along an edge (a candidate wall for a door)."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    vertical_touch = (ax2 == bx1 or bx2 == ax1) and min(ay2, by2) - max(ay1, by1) > 0
    horizontal_touch = (ay2 == by1 or by2 == ay1) and min(ax2, bx2) - max(ax1, bx1) > 0
    return vertical_touch or horizontal_touch


def verify_floorplan(rooms: dict[str, Rect], doors: list[Door]) -> list[str]:
    """Return a list of constraint violations; an empty list means the plan is valid."""
    violations = []
    names = list(rooms)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if rooms_overlap(rooms[a], rooms[b]):
                violations.append(f"rooms overlap: {a!r} and {b!r}")
    connected = {name: False for name in rooms}
    for room_a, room_b in doors:
        if not shares_wall(rooms[room_a], rooms[room_b]):
            violations.append(f"door between {room_a!r} and {room_b!r} is not on a shared wall")
        connected[room_a] = connected[room_b] = True
    for name, has_door in connected.items():
        if not has_door:
            violations.append(f"room has no door: {name!r}")
    return violations


PLANS = {
    "valid layout": {
        "rooms": {
            "bedroom": (0, 0, 4, 4),
            "bathroom": (4, 0, 6, 4),
            "hallway": (0, 4, 6, 5),
        },
        "doors": [("bedroom", "hallway"), ("bathroom", "hallway")],
    },
    "overlapping rooms": {
        "rooms": {
            "bedroom": (0, 0, 4, 4),
            "bathroom": (3, 0, 6, 4),  # overlaps bedroom between x=3 and x=4
            "hallway": (0, 4, 6, 5),
        },
        "doors": [("bedroom", "hallway"), ("bathroom", "hallway")],
    },
    "room with no door": {
        "rooms": {
            "bedroom": (0, 0, 4, 4),
            "bathroom": (4, 0, 6, 4),
            "hallway": (0, 4, 6, 5),
        },
        "doors": [("bedroom", "hallway")],  # bathroom never gets a door
    },
}

for label, plan in PLANS.items():
    violations = verify_floorplan(plan["rooms"], plan["doors"])
    verdict = "PASS" if not violations else "FAIL"
    print(f"--- {label}: {verdict} ---")
    for violation in violations:
        print(f"  {violation}")
    print()
