# Mosque-Landscape-Animation---Python-Turtle
An interactive mosque landscape animation featuring dynamic day/night modes, moving vehicles, and custom graphics algorithms built with Python Turtle.

**Night_Mode**
<img width="1538" height="857" alt="Screenshot from 2026-05-06 22-19-46" src="https://github.com/user-attachments/assets/0ddd2866-eead-43ab-96f7-5ffa2143cfe4" />

**Day_Mode**
<img width="1538" height="857" alt="image" src="https://github.com/user-attachments/assets/9e959140-d3a9-48ab-977f-0f345094bf22" />



**Mosque Landscape Animation - Python Turtle**
Welcome to the Mosque Landscape Animation repository! This project is a Python-based computer graphics application built using the native turtle graphics module. It features an interactive, animated daytime and nighttime scene of a mosque complete with dynamic elements like moving vehicles, flying birds, flowing clouds, and swaying trees.

This implementation utilizes custom-built, low-level computer graphics algorithms to draw lines and circles from scratch.

**🚀 Key Features**
Custom Algorithms: Uses custom implementations of Bresenham’s Line Algorithm and the Midpoint Circle Algorithm for rendering shapes without relying on built-in rendering functions.

Dynamic Day/Night Mode: Toggle the entire scene's background, lighting, and colors by pressing a single key.

Animated Objects: Vehicles cruising on the road, clouds drifting across the sky, birds flying, and flora swaying in the background.

Detailed Architectural Design: Features domes, minarets, pointed arch doors, and background buildings.

**🎮 Controls**
Press m on your keyboard to toggle between Day Mode and Night Mode.

🛠️ Requirements
Python 3.x or higher.

No external libraries are required (uses Python's built-in turtle and math modules).

**📜 Code Structure & Function Reference**
The application is modularized to ensure smooth rendering and interaction. Here is a breakdown of the core functions and their workflows:
**1. Computer Graphics Algorithms** **bresenham(x1, y1, x2, y2):** Computes the intermediate (x, y) coordinates to draw a straight line between two points using integer arithmetic, optimizing rendering speed.
 draw_filled_midpoint_circle(t, xc, yc, r, color): Uses the Midpoint Circle Algorithm along with symmetric horizontal chords to draw and fill solid circles.
 **2. Scene Rendering Functions**
 **draw_sky(t) and draw_sun(t):** Renders the background, which swaps between a bright blue sky with a sun and a deep night sky featuring a moon and stars.
** draw_mosque(t):** Builds the main structure by calling sub-components, including the main dome, minarets, and arched doors with glowing lights for the night mode.
**draw_minaret(t, x, y, w, h):** Draws the tall towers adjacent to the mosque, capped with gold bands, domes, and finials.
**3. Environment & Background**
**draw_hills and draw_river:** Generates the rolling green hills and a flowing blue river with animated waves in the background.
**draw_buildings: **Creates a cityscape in the background with windows that illuminate when Night Mode is active.
**draw_tree and draw_flower: **Renders flora with different scaling factors to create depth across the terrain.
**4. Animation Engineanimate(): **
The main driver loop. Updates positions of the clouds, birds, and vehicles, clearing the respective canvases and redrawing them to create motion.

**💻 How to Run**
Clone or download this repository to your local machine.

Open your terminal or command prompt.

Run the script using Python: _python mosque_animation.py_

**🤝 Contributing**
Contributions are welcome! If you would like to optimize the rendering speed, add new graphical assets, or improve the animation algorithms, feel free to fork the repository and submit a pull request.


||kofs_2026||
