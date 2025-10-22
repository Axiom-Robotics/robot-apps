#!/usr/bin/env python3

# draw_square.py

def get_shapes():
    return {
        "square": {
            "action": "sequence",
            "params": [
                {"action": "move", "params": {"linear_speed": 1.0, "distance": 2.0, "is_forward": True, "unit": "meter"}},
                {"action": "rotate", "params": {"angular_velocity": 30, "angle": 90, "is_clockwise": False, "unit": "degrees"}},
                {"action": "move", "params": {"linear_speed": 1.0, "distance": 2.0, "is_forward": True, "unit": "meter"}},
                {"action": "rotate", "params": {"angular_velocity": 30, "angle": 90, "is_clockwise": False, "unit": "degrees"}},
                {"action": "move", "params": {"linear_speed": 1.0, "distance": 2.0, "is_forward": True, "unit": "meter"}},
                {"action": "rotate", "params": {"angular_velocity": 30, "angle": 90, "is_clockwise": False, "unit": "degrees"}},
                {"action": "move", "params": {"linear_speed": 1.0, "distance": 2.0, "is_forward": True, "unit": "meter"}},
                {"action": "rotate", "params": {"angular_velocity": 30, "angle": 90, "is_clockwise": False, "unit": "degrees"}}
            ]
        }
    }

