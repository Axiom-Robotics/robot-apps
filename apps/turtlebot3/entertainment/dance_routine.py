#!/usr/bin/env python3
"""
TurtleBot3 Dance Routine App
Modern get_commands() format for Axiom OS
"""

def get_commands():
    """
    Returns a list of commands for a fun dance routine
    Robot performs: spin, shimmy left, shimmy right, double spin, bow, exit
    """
    return [
        # 1. Intro spin (360 degrees)
        {"command": "turn", "direction": "left", "params": {"angle": 360, "angular_velocity": 60}},
        {"command": "wait", "duration": 0.5},
        
        # 2. Shimmy left
        {"command": "move", "params": {"distance": 0.3, "linear_speed": 0.15, "direction": "forward"}},
        {"command": "turn", "direction": "left", "params": {"angle": 45, "angular_velocity": 45}},
        {"command": "move", "params": {"distance": 0.3, "linear_speed": 0.15, "direction": "backward"}},
        {"command": "turn", "direction": "right", "params": {"angle": 45, "angular_velocity": 45}},
        
        # 3. Shimmy right
        {"command": "move", "params": {"distance": 0.3, "linear_speed": 0.15, "direction": "forward"}},
        {"command": "turn", "direction": "right", "params": {"angle": 45, "angular_velocity": 45}},
        {"command": "move", "params": {"distance": 0.3, "linear_speed": 0.15, "direction": "backward"}},
        {"command": "turn", "direction": "left", "params": {"angle": 45, "angular_velocity": 45}},
        
        # 4. Big double spin (720 degrees)
        {"command": "turn", "direction": "right", "params": {"angle": 720, "angular_velocity": 90}},
        {"command": "wait", "duration": 0.5},
        
        # 5. Bow (forward and back)
        {"command": "move", "params": {"distance": 0.2, "linear_speed": 0.1, "direction": "forward"}},
        {"command": "wait", "duration": 0.3},
        {"command": "move", "params": {"distance": 0.2, "linear_speed": 0.1, "direction": "backward"}},
        
        # 6. Final flourish (180 turn)
        {"command": "turn", "direction": "left", "params": {"angle": 180, "angular_velocity": 60}},
        {"command": "stop"}
    ]

def get_metadata():
    """App metadata for Axiom OS"""
    return {
        "name": "Dance Routine",
        "version": "1.0",
        "description": "A fun dance routine with spins, shimmies, and a bow!",
        "author": "Axiom Robotics",
        "category": "entertainment",
        "duration": "~20 seconds",
        "commands": ["dance", "dance routine", "perform dance"]
    }

# For testing standalone
if __name__ == "__main__":
    print("=== TurtleBot3 Dance Routine ===")
    commands = get_commands()
    metadata = get_metadata()
    
    print(f"\nApp: {metadata['name']}")
    print(f"Description: {metadata['description']}")
    print(f"Duration: {metadata['duration']}")
    print(f"\nTotal commands: {len(commands)}")
    print("\nCommand sequence:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i}. {cmd.get('command', cmd.get('action'))}")
