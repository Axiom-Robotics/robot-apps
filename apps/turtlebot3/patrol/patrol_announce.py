#!/usr/bin/env python3
"""
TurtleBot3 Patrol & Announce App
Modern get_commands() format for Axiom OS
"""

def get_commands():
    """
    Returns a list of commands for a basic patrol route
    Robot performs: patrol 4 waypoints in a square pattern with announcements
    """
    return [
        # Start announcement
        {"command": "announce", "message": "Starting patrol route"},
        {"command": "wait", "duration": 1.0},
        
        # === Waypoint 1: Living Room ===
        {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3, "direction": "forward"}},
        {"command": "announce", "message": "Waypoint 1: Living room area checked"},
        {"command": "wait", "duration": 1.5},
        
        # Turn to next waypoint
        {"command": "turn", "direction": "left", "params": {"angle": 90, "angular_velocity": 45}},
        
        # === Waypoint 2: Kitchen ===
        {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3, "direction": "forward"}},
        {"command": "announce", "message": "Waypoint 2: Kitchen patrol complete"},
        {"command": "wait", "duration": 1.5},
        
        # Turn to next waypoint
        {"command": "turn", "direction": "left", "params": {"angle": 90, "angular_velocity": 45}},
        
        # === Waypoint 3: Bedroom ===
        {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3, "direction": "forward"}},
        {"command": "announce", "message": "Waypoint 3: Bedroom area secured"},
        {"command": "wait", "duration": 1.5},
        
        # Turn to next waypoint
        {"command": "turn", "direction": "left", "params": {"angle": 90, "angular_velocity": 45}},
        
        # === Waypoint 4: Hallway ===
        {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3, "direction": "forward"}},
        {"command": "announce", "message": "Waypoint 4: Hallway inspection done"},
        {"command": "wait", "duration": 1.5},
        
        # Return to start position
        {"command": "turn", "direction": "left", "params": {"angle": 90, "angular_velocity": 45}},
        
        # Final announcement
        {"command": "announce", "message": "Patrol route complete. All areas checked"},
        {"command": "stop"}
    ]

def get_metadata():
    """App metadata for Axiom OS"""
    return {
        "name": "Patrol & Announce",
        "version": "1.0",
        "description": "Robot patrols 4 waypoints in a square pattern and announces status at each location",
        "author": "Axiom Robotics",
        "category": "navigation",
        "duration": "~45 seconds",
        "commands": ["patrol", "start patrol", "patrol route", "security patrol"]
    }

# For testing standalone
if __name__ == "__main__":
    print("=== TurtleBot3 Patrol & Announce ===")
    commands = get_commands()
    metadata = get_metadata()
    
    print(f"\nApp: {metadata['name']}")
    print(f"Description: {metadata['description']}")
    print(f"Duration: {metadata['duration']}")
    print(f"\nTotal commands: {len(commands)}")
    print("\nCommand sequence:")
    for i, cmd in enumerate(commands, 1):
        cmd_type = cmd.get('command', cmd.get('action'))
        if cmd_type == 'announce':
            print(f"  {i}. 🔊 {cmd_type}: \"{cmd['message']}\"")
        elif cmd_type == 'move':
            print(f"  {i}. ➡️  {cmd_type}: {cmd['params']['distance']}m {cmd['params']['direction']}")
        elif cmd_type == 'turn':
            print(f"  {i}. 🔄 {cmd_type}: {cmd['params']['angle']}° {cmd['direction']}")
        elif cmd_type == 'wait':
            print(f"  {i}. ⏸️  {cmd_type}: {cmd['duration']}s")
        else:
            print(f"  {i}. {cmd_type}")
