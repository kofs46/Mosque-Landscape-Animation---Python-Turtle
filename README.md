# Mosque-Landscape-Animation---Python-Turtle
An interactive mosque landscape animation featuring dynamic day/night modes, moving vehicles, and custom graphics algorithms built with Python Turtle.

Mosque Landscape Animation - Python Turtle
Welcome to the Mosque Landscape Animation repository! This project is a Python-based computer graphics application built using the native turtle graphics module. It features an interactive, animated daytime and nighttime scene of a mosque complete with dynamic elements like moving vehicles, flying birds, flowing clouds, and swaying trees.

This implementation utilizes custom-built, low-level computer graphics algorithms to draw lines and circles from scratch.

🚀 Key Features
Custom Algorithms: Uses custom implementations of Bresenham’s Line Algorithm and the Midpoint Circle Algorithm for rendering shapes without relying on built-in rendering functions.

Dynamic Day/Night Mode: Toggle the entire scene's background, lighting, and colors by pressing a single key.

Animated Objects: Vehicles cruising on the road, clouds drifting across the sky, birds flying, and flora swaying in the background.

Detailed Architectural Design: Features domes, minarets, pointed arch doors, and background buildings.

🎮 Controls
Press m on your keyboard to toggle between Day Mode and Night Mode.

🛠️ Requirements
Python 3.x or higher.

No external libraries are required (uses Python's built-in turtle and math modules).

📜 Code Structure & Function ReferenceThe application is modularized to ensure smooth rendering and interaction. Here is a breakdown of the core functions and their workflows:1. Computer Graphics Algorithmsbresenham(x1, y1, x2, y2): Computes the intermediate $(x, y)$ coordinates to draw a straight line between two points using integer arithmetic, optimizing rendering speed.draw_filled_midpoint_circle(t, xc, yc, r, color): Uses the Midpoint Circle Algorithm along with symmetric horizontal chords to draw and fill solid circles.2. Scene Rendering Functionsdraw_sky(t) and draw_sun(t): Renders the background, which swaps between a bright blue sky with a sun and a deep night sky featuring a moon and stars.draw_mosque(t): Builds the main structure by calling sub-components, including the main dome, minarets, and arched doors with glowing lights for the night mode.draw_minaret(t, x, y, w, h): Draws the tall towers adjacent to the mosque, capped with gold bands, domes, and finials.3. Environment & Backgrounddraw_hills and draw_river: Generates the rolling green hills and a flowing blue river with animated waves in the background.draw_buildings: Creates a cityscape in the background with windows that illuminate when Night Mode is active.draw_tree and draw_flower: Renders flora with different scaling factors to create depth across the terrain.4. Animation Engineanimate(): The main driver loop. Updates positions of the clouds, birds, and vehicles, clearing the respective canvases and redrawing them to create motion.
