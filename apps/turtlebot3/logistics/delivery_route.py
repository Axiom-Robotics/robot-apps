#!/usr/bin/env python3
# delivery_route.py - Multi-waypoint delivery system with announcements

def get_commands():
    """
    Delivery route with 4 stops:
    1. Reception desk
    2. Conference room
    3. Kitchen area
    4. Office wing
    Returns to starting position after delivery
    """
    
    delivery_waypoints = [
        # Waypoint 1: Reception (3m forward)
        {
            "waypoint": "Reception Desk",
            "commands": [
                {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3}},
                {"command": "announce", "message": "📦 Delivery 1/4: Package delivered to Reception Desk"}
            ]
        },
        # Waypoint 2: Conference Room (turn right, go 2m)
        {
            "waypoint": "Conference Room",
            "commands": [
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "right"},
                {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3}},
                {"command": "announce", "message": "📦 Delivery 2/4: Package delivered to Conference Room"}
            ]
        },
        # Waypoint 3: Kitchen (turn left, go 3m)
        {
            "waypoint": "Kitchen Area",
            "commands": [
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "left"},
                {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3}},
                {"command": "announce", "message": "📦 Delivery 3/4: Package delivered to Kitchen Area"}
            ]
        },
        # Waypoint 4: Office Wing (turn left, go 2m)
        {
            "waypoint": "Office Wing",
            "commands": [
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "left"},
                {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3}},
                {"command": "announce", "message": "📦 Delivery 4/4: Package delivered to Office Wing"}
            ]
        },
        # Return to start (turn around, retrace path)
        {
            "waypoint": "Return Home",
            "commands": [
                {"command": "rotate", "params": {"angle": 180, "angular_velocity": 30}, "direction": "right"},
                {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3}},
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "right"},
                {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3}},
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "right"},
                {"command": "move", "params": {"distance": 2.0, "linear_speed": 0.3}},
                {"command": "rotate", "params": {"angle": 90, "angular_velocity": 30}, "direction": "right"},
                {"command": "move", "params": {"distance": 3.0, "linear_speed": 0.3}},
                {"command": "announce", "message": "✅ All deliveries complete! Returned to starting position"}
            ]
        }
    ]
    
    # Flatten all commands into a single list
    all_commands = []
    
    for waypoint in delivery_waypoints:
        # Add waypoint announcement
        all_commands.append({
            "command": "announce",
            "message": f"🚀 Heading to: {waypoint['waypoint']}"
        })
        
        # Add all movement commands for this waypoint
        all_commands.extend(waypoint['commands'])
        
        # Add pause at each stop
        all_commands.append({
            "command": "wait",
            "duration": 2.0
        })
    
    return all_commands
