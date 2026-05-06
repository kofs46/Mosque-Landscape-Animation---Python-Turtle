import turtle
import math

# ──────────────────────────────────────────────────────────
#  SCREEN SETUP
# ──────────────────────────────────────────────────────────
screen = turtle.Screen()
screen.title("A Mosque with Lamp Lights and Mic System")
screen.setup(width=1280, height=720)
screen.bgcolor("#3BB8E8")            # solid bright sky blue

turtle.tracer(0, 0)                  # manual refresh for smooth animation
GROUND_Y = -240
NIGHT_MODE = True    # change to False for day mode
HALF_W = 640

# Define colors
WALL_COLOR = "#8B1A1A"  # dark red
GOLD_COLOR = "#D4A017"  # golden yellow
CREAM_COLOR = "#F5DEB3"  # wheat / cream
BLACK_COLOR = "#111111"
WHITE_COLOR = "white"
SKY_COLOR = "#3BB8E8"
NIGHT_SKY_COLOR = "#0B1D3A"
HILL_COLOR1 = "#5DB84A"
HILL_COLOR2 = "#6DC45A"
GRASS_COLOR = "#4CAF50"
GRASS_HIGHLIGHT = "#66BB6A"
NIGHT_GRASS_COLOR = "#2E7D32"
NIGHT_GRASS_HIGHLIGHT = "#3E8E41"
ROAD_COLOR = "#555555"
DASH_COLOR = "#EEEEEE"

# ──────────────────────────────────────────────────────────
#  BRESENHAM'S LINE ALGORITHM
# ──────────────────────────────────────────────────────────

def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    x = x1
    y = y1
    points = [(x, y)]

    if dx > dy:
        pk = 2 * dy - dx
        for _ in range(dx):
            if pk < 0:
                x += sx
                pk += 2 * dy
            else:
                x += sx
                y += sy
                pk += 2 * dy - 2 * dx
            points.append((x, y))
    else:
        pk = 2 * dx - dy
        for _ in range(dy):
            if pk < 0:
                y += sy
                pk += 2 * dx
            else:
                x += sx
                y += sy
                pk += 2 * dx - 2 * dy
            points.append((x, y))

    return points


def draw_line_bresenham(t, x1, y1, x2, y2, color, pensize=1):
    points = bresenham(x1, y1, x2, y2)
    t.pencolor(color)
    t.pensize(pensize)
    t.penup()
    for i, (px, py) in enumerate(points):
        if i == 0:
            t.goto(px, py)
            t.pendown()
        else:
            t.goto(px, py)
    t.penup()

# ──────────────────────────────────────────────────────────
#  MIDPOINT CIRCLE ALGORITHM
# ──────────────────────────────────────────────────────────

def draw_filled_midpoint_circle(t, xc, yc, r, color):
    """Draws a solid filled circle using the midpoint circle algorithm."""
    t.pencolor(color)
    x = 0
    y = r
    pk = 1 - r

    def draw_circle_points(xc, yc, x, y):
        # Draw horizontal chords (lines) between symmetric points to fill the circle interior
        t.penup()
        t.goto(xc - x, yc + y); t.pendown(); t.goto(xc + x, yc + y); t.penup()
        t.goto(xc - x, yc - y); t.pendown(); t.goto(xc + x, yc - y); t.penup()
        t.goto(xc - y, yc + x); t.pendown(); t.goto(xc + y, yc + x); t.penup()
        t.goto(xc - y, yc - x); t.pendown(); t.goto(xc + y, yc - x); t.penup()

    draw_circle_points(xc, yc, x, y)
    while x < y:
        x = x + 1
        if pk < 0:
            pk = pk + 2 * x + 1
        else:
            y = y - 1
            pk = pk + 2 * x - 2 * y + 1
        draw_circle_points(xc, yc, x, y)


# ──────────────────────────────────────────────────────────
#  LOW-LEVEL DRAWING HELPERS
# ──────────────────────────────────────────────────────────

def pen():
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.hideturtle()
    return t


def rect(t, x, y, w, h, fill, outline=None, pensize=1):
    """Filled rectangle. (x,y) = bottom-left corner."""
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.fillcolor(fill)
    if outline:
        t.pencolor(outline)
        t.pensize(pensize)
    else:
        t.pencolor(fill)
        t.pensize(1)
    t.pendown()
    t.begin_fill()
    for _ in range(2):
        t.forward(w); t.left(90)
        t.forward(h); t.left(90)
    t.end_fill()
    t.penup()


def circle(t, cx, cy, r, fill, outline=None, pensize=1):
    t.penup()
    t.goto(cx, cy - r)
    t.setheading(0)
    t.fillcolor(fill)
    if outline:
        t.pencolor(outline)
        t.pensize(pensize)
    else:
        t.pencolor(fill)
        t.pensize(1)
    t.pendown()
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    t.penup()


def poly(t, pts, fill, outline=None, pensize=1):
    t.penup()
    t.goto(pts[0])
    t.fillcolor(fill)
    if outline:
        t.pencolor(outline)
        t.pensize(pensize)
    else:
        t.pencolor(fill)
        t.pensize(1)
    t.pendown()
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.goto(pts[0])
    t.end_fill()
    t.penup()


def dome(t, cx, cy, rx, ry, fill, outline=None, pensize=1):
    pts = []
    for d in range(181):
        rad = math.radians(d)
        pts.append((cx + rx * math.cos(math.pi - rad),
                    cy + ry * math.sin(rad)))
    pts += [(cx + rx, cy), (cx - rx, cy)]
    poly(t, pts, fill, outline, pensize)


# ──────────────────────────────────────────────────────────
#  SKY, STARS, & SUN/MOON
# ──────────────────────────────────────────────────────────

def draw_sky(t):
    """Sky changes based on day/night mode."""
    if NIGHT_MODE:
        rect(t, -640, -20, 1280, 380, NIGHT_SKY_COLOR)  # dark night sky
    else:
        rect(t, -640, -20, 1280, 380, SKY_COLOR)


def draw_sun(t):
    """Sun in day mode, moon in night mode."""
    if NIGHT_MODE:
        circle(t, -300, 280, 50, "#F5F3CE")
        circle(t, -285, 290, 45, NIGHT_SKY_COLOR)  # crescent cut
    else:
        draw_filled_midpoint_circle(t, -300, 280, 55, "#FFE600")


def draw_stars(t):
    if not NIGHT_MODE:
        return
    stars = [
        (-500, 300), (-420, 260), (-300, 320),
        (-100, 280), (0, 340), (120, 300),
        (250, 330), (400, 270), (520, 310)
    ]
    for x, y in stars:
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.pencolor(WHITE_COLOR)
        for i in range(5):  # 5 arms of star
            t.forward(12)
            t.right(144)
        t.penup()


# ──────────────────────────────────────────────────────────
#  CLOUDS
# ──────────────────────────────────────────────────────────

def draw_cloud(t, cx, cy, s=1.0):
    """Puffy white cloud made of overlapping circles."""
    parts = [(0, 0, 34), (-38, -6, 26), (38, -6, 26),
             (-18, 14, 20), (18, 14, 20), (0, 18, 18)]
    for dx, dy, r in parts:
        circle(t, cx + dx*s, cy + dy*s, int(r*s), WHITE_COLOR)


# ──────────────────────────────────────────────────────────
#  HILLS
# ──────────────────────────────────────────────────────────

def draw_hills(t):
    """Smooth green hills in the background."""
    poly(t, [(-640, 60), (-640, 180), (-80, 210), (200, 140), (400, 60)],
         HILL_COLOR1)
    poly(t, [(100, 60), (380, 180), (640, 200), (640, 60)],
         HILL_COLOR2)
    rect(t, -640, 60, 1280, 30, HILL_COLOR1)


# ──────────────────────────────────────────────────────────
#  RIVER
# ──────────────────────────────────────────────────────────

def draw_river(t):
    """নদীর পানি আঁকার ফাংশন"""
    rect(t, -640, 16, 1280, 40, "#1976D2")
    
    # নদীর পানির ঢেউ (Waves)
    t.pencolor("#64B5F6")
    t.pensize(2)
    for i in range(-600, 600, 60):
        t.penup()
        t.goto(i, 36)
        t.pendown()
        t.forward(30)
        t.penup()


# ──────────────────────────────────────────────────────────
#  BACKGROUND BUILDINGS
# ──────────────────────────────────────────────────────────

def draw_buildings(t):
    """Two building clusters left and right, visible behind hills with illuminated windows at night."""
    # LEFT cluster
    rect(t, -620, 90, 110, 220, "#9E9E9E")
    for row in range(4):
        for col in range(3):
            win_color = "#FFEE58" if NIGHT_MODE else "#CFD8DC"
            rect(t, -608 + col*34, 104 + row*50, 24, 34, win_color)

    rect(t, -510, 90, 90, 170, "#6D4C41")
    for row in range(3):
        for col in range(2):
            win_color = "#FFEE58" if NIGHT_MODE else "#A1887F"
            rect(t, -500 + col*36, 104 + row*50, 24, 30, win_color)

    # RIGHT cluster
    rect(t, 460, 90, 105, 240, "#7C6BC2")
    for row in range(5):
        for col in range(2):
            win_color = "#FFEE58" if NIGHT_MODE else "#B39DDB"
            rect(t, 472 + col*44, 104 + row*42, 30, 26, win_color)

    rect(t, 560, 90, 80, 180, "#E91E8C")
    for row in range(4):
        for col in range(2):
            win_color = "#FFEE58" if NIGHT_MODE else "#F8BBD0"
            rect(t, 569 + col*34, 104 + row*40, 24, 24, win_color)

    rect(t, 570, 90, 70, 130, "#FF8A65")
    for i in range(5):
        win_color = "#FFEE58" if NIGHT_MODE else "#FFAB91"
        rect(t, 570, 100 + i*22, 70, 10, win_color)


# ──────────────────────────────────────────────────────────
#  GRASS STRIP
# ──────────────────────────────────────────────────────────

def draw_grass(t):
    """Grass adapts to night mode."""
    if NIGHT_MODE:
        grass_color = NIGHT_GRASS_COLOR
        highlight = NIGHT_GRASS_HIGHLIGHT
    else:
        grass_color = GRASS_COLOR
        highlight = GRASS_HIGHLIGHT

    rect(t, -640, -240, 1280, 260, grass_color)
    rect(t, -640, 16, 1280, 12, highlight)
    poly(t, [(0, -240), (-90, 20), (90, 20)], grass_color)


# ──────────────────────────────────────────────────────────
#  MOSQUE
# ──────────────────────────────────────────────────────────

def draw_arch_door(t, x, y, w, h, fill=BLACK_COLOR):
    """Pointed Gothic/Islamic arch door or window."""
    rect(t, x, y, w, h - w//2, fill)
    hw = w // 2
    poly(t, [(x, y+h-hw), (x+hw, y+h), (x+w, y+h-hw)], fill)


def draw_minaret(t, x, y, w, h, outline=None, pensize=1):
    """Tall minaret: shaft + gold band + small dome + ball finial."""
    rect(t, x, y, w, h, WALL_COLOR, outline=outline, pensize=pensize)
    rect(t, x-3, y+h-22, w+6, 12, GOLD_COLOR, outline=outline, pensize=pensize)
    dome(t, x+w//2, y+h-8, w//2+5, 20, GOLD_COLOR, outline=outline, pensize=pensize)
    circle(t, x+w//2, y+h+14, 5, "#8B0000", outline=outline, pensize=pensize)


def draw_microphone_stand(t, x, y):
    rect(t, x - 3, y, 6, 120, "#37474F")
    rect(t, x - 12, y, 24, 6, "#212121")
    rect(t, x - 10, y + 112, 20, 10, "#B0BEC5", outline=BLACK_COLOR, pensize=1)
    circle(t, x, y + 122, 6, "#E53935", outline=BLACK_COLOR, pensize=1)


def draw_mosque(t):
    """Central mosque matching the reference image."""
    border_pensize = 2

    # Base platform
    rect(t, -270, -108, 540, 16, "#5D4037")
    rect(t, -270,  -92, 540, 72, WALL_COLOR, outline=BLACK_COLOR, pensize=border_pensize)

    # Horizontal cream bands on ground floor
    rect(t, -270,  -78, 540, 10, CREAM_COLOR)
    rect(t, -270,  -48, 540, 10, CREAM_COLOR)

    # Arched windows / niches (ground floor)
    arch_xs = [-245, -180, -112, -45, 22, 90, 158, 222]
    for ax in arch_xs:
        if NIGHT_MODE:
            draw_arch_door(t, ax, -88, 36, 54, "#FFD54F")  # Glows at night
        else:
            draw_arch_door(t, ax, -88, 36, 54, BLACK_COLOR)

    # Second storey wall
    s2_y = -20
    rect(t, -240, s2_y, 480, 52, WALL_COLOR, outline=BLACK_COLOR, pensize=border_pensize)
    rect(t, -240, s2_y+40, 480, 10, CREAM_COLOR)

    # Side domes (4 medium)
    side_domes = [(-200, s2_y+52, 38, 30),
                  (-105, s2_y+52, 38, 30),
                  ( 68, s2_y+52, 38, 30),
                  ( 163, s2_y+52, 38, 30)]
    for dcx, dcy, drx, dry in side_domes:
        dome(t, dcx, dcy, drx, dry, GOLD_COLOR, outline=BLACK_COLOR, pensize=border_pensize)
        cx2, cy2 = dcx, dcy + dry + 4
        circle(t, cx2, cy2, 8, GOLD_COLOR, outline=BLACK_COLOR, pensize=border_pensize)
        
        # Corrected: Center the wall color circle and add outline/pensize
        circle(t, cx2, cy2, 6, WALL_COLOR, outline=BLACK_COLOR, pensize=border_pensize)
        
        circle(t, dcx, dcy + dry + 14, 4, "#8B0000", outline=BLACK_COLOR, pensize=border_pensize)

    # Central arch entrance (cream/white)
    draw_arch_door(t, -40,  -92, 80, 105, CREAM_COLOR)
    if NIGHT_MODE:
        draw_arch_door(t, -30,  -88, 60,  90, "#FFD54F")  # Glows at night
    else:
        draw_arch_door(t, -30,  -88, 60,  90, BLACK_COLOR)

    # Central large dome
    dome(t, 0, s2_y+52, 88, 72, GOLD_COLOR, outline=BLACK_COLOR, pensize=border_pensize)
    circle(t, 0, s2_y+52+72+5, 7, "#8B0000", outline=BLACK_COLOR, pensize=border_pensize)

    # 4 Tall minarets with BLACK outlines
    draw_minaret(t, -280, -108, 32, 170, outline=BLACK_COLOR, pensize=border_pensize)
    draw_minaret(t, -200, -108, 26, 138, outline=BLACK_COLOR, pensize=border_pensize)
    draw_minaret(t,  175, -108, 26, 138, outline=BLACK_COLOR, pensize=border_pensize)
    draw_minaret(t,  248, -108, 32, 170, outline=BLACK_COLOR, pensize=border_pensize)


# ──────────────────────────────────────────────────────────
#  SHRUBS & PLANTS
# ──────────────────────────────────────────────────────────

def draw_shrub(t, x, y):
    circle(t, x, y, 10, "#4CAF50")
    circle(t, x - 5, y + 2, 5, "#FF9800") 
    circle(t, x + 5, y - 2, 4, "#FFC107")
    circle(t, x,     y + 5, 4, "#FFEB3B")


# ──────────────────────────────────────────────────────────
#  CONNECTING ROAD
# ──────────────────────────────────────────────────────────

def draw_connecting_road(t):
    """Draws an access road connecting the mosque to the main road using Bresenham's."""
    rect(t, -50, -240, 100, 132, ROAD_COLOR)
    
    draw_line_bresenham(t, -50, -240, -50, -108, WHITE_COLOR, pensize=2)
    draw_line_bresenham(t, 50, -240, 50, -108, WHITE_COLOR, pensize=2)

    for y_pos in [-220, -180, -140]:
        draw_shrub(t, -62, y_pos)
        draw_shrub(t, 62, y_pos)


# ──────────────────────────────────────────────────────────
#  TREES
# ──────────────────────────────────────────────────────────

def draw_tree(t, x, y, scale=1.0, sway=0):
    """Cartoon tree: brown trunk + round green canopy with swaying animation."""
    tw = int(16 * scale)
    th = int(50 * scale)
    cr = int(38 * scale)

    rect(t, x - tw//2, y, tw, th, "#795548")
    circle(t, x + sway,            y + th + cr - 8,  cr,            NIGHT_GRASS_COLOR)
    circle(t, x - int(20*scale) + sway, y + th + cr - 18, int(cr*0.78), "#388E3C")
    circle(t, x + int(18*scale) + sway, y + th + cr - 16, int(cr*0.78), "#43A047")


def redraw_trees(t, sway):
    t.clear()
    G = GROUND_Y
    draw_tree(t, -560, G, 2.8, sway)
    draw_tree(t, -410, G, 1.1, sway)
    draw_tree(t, -340, G, 0.95, sway)
    draw_tree(t, -265, G, 0.85, sway)
    draw_tree(t,  225, G, 0.85, sway)
    draw_tree(t,  300, G, 0.95, sway)
    draw_tree(t,  370, G, 1.0, sway)
    draw_tree(t,  450, G, 1.1, sway)
    draw_tree(t,  580, G, 0.9, sway)
    draw_tree(t,  620, G, 0.75, sway)
    draw_tree(t, -490, G, 0.70, sway)
    draw_tree(t, -155, G, 0.65, sway)
    draw_tree(t,  110, G, 0.65, sway)
    draw_tree(t,  530, G, 0.70, sway)


# ──────────────────────────────────────────────────────────
#  FLOWERS
# ──────────────────────────────────────────────────────────

def draw_flower(t, x, y, color="#FF1744", sway=0):
    """Small cartoon flower: stem + 6 petals + yellow centre with swaying animation."""
    t.pencolor("#8AB78D"); t.pensize(2)
    t.goto(x, y); t.setheading(90)
    t.pendown(); t.forward(15); t.penup(); t.pensize(1)
    
    cx, cy = x + sway, y + 15
    for ang in range(0, 360, 60):
        r = math.radians(ang)
        circle(t, cx + 7*math.cos(r), cy + 7*math.sin(r), 5, color)
    circle(t, cx, cy, 4, "#FFD600")


def redraw_flowers(t, sway):
    t.clear()
    G = GROUND_Y + 5 
    data = [
        (-590, G, "#FF1744"), (-570, G, "#E040FB"), (-540, G, "#FF6D00"),
        (-470, G, "#FF1744"), (-450, G, "#FFEB3B"), (-300, G, "#FF1744"), 
        (-280, G, "#E040FB"), (-200, G, "#FF6D00"), (155, G, "#FF1744"), 
        (175, G, "#E040FB"), (330, G, "#FF1744"), (350, G, "#FFEB3B"), 
        (380, G, "#FF6D00"), (400, G, "#E040FB"), (425, G, "#FF1744"), 
        (500, G, "#FF6D00"), (520, G, "#FF1744"), (545, G, "#E040FB"), 
        (565, G, "#FFEB3B"), (590, G, "#FF1744"), (610, G, "#FF6D00"),
    ]
    for fx, fy, fc in data:
        draw_flower(t, fx, fy, fc, sway)


# ──────────────────────────────────────────────────────────
#  LAMP POST
# ──────────────────────────────────────────────────────────

def draw_lamp_structure(t, x, y):
    rect(t, x-3, y, 6, 85, "#424242")
    rect(t, x-18, y+82, 36, 5, "#424242")
    circle(t, x, y+87, 9, "#9E9E9E")


def draw_lamp_light(t, x, y, on):
    if on:
        circle(t, x, y+87, 6, "#FFEE58") # Glowing Yellow
    else:
        circle(t, x, y+87, 6, "#424242") # Turned Off


# ──────────────────────────────────────────────────────────
#  ROAD
# ──────────────────────────────────────────────────────────

def draw_road(t):
    """Dark grey road at the bottom using Bresenham's algorithm."""
    road_y = -360
    road_h = 120
    rect(t, -640, road_y, 1280, road_h, ROAD_COLOR)

    for lane_y in [road_y + 38, road_y + 78]:
        x = -620
        while x < 640:
            draw_line_bresenham(t, x, lane_y, x + 42, lane_y, DASH_COLOR, pensize=3)
            x += 72

    for ey in [road_y + 6, road_y + road_h - 6]:
        draw_line_bresenham(t, -640, ey, 640, ey, WHITE_COLOR, pensize=3)


# ──────────────────────────────────────────────────────────
#  VEHICLES
# ──────────────────────────────────────────────────────────

def draw_car(t, x, y, body="#E53935", roof_color=None):
    rc = roof_color or body
    rect(t, x, y, 80, 24, body)
    poly(t, [(x+10, y+24), (x+16, y+46),
             (x+64, y+46), (x+70, y+24)], rc)
    poly(t, [(x+20, y+26), (x+24, y+43),
             (x+48, y+43), (x+52, y+26)], "#B3E5FC")
    poly(t, [(x+54, y+26), (x+57, y+43),
             (x+66, y+43), (x+68, y+26)], "#B3E5FC")
    rect(t, x+72, y+7, 8, 10, "#FFEE58") # Headlight
    
    if NIGHT_MODE:
        poly(t, [(x+80, y+7), (x+140, y-15), (x+140, y+35)], "#FFF59D")
        circle(t, x+76, y+12, 5, "#FFEE58")  # Glow effect

    for wx in [x+14, x+58]:
        circle(t, wx, y+1,  14, "#212121")
        circle(t, wx, y+1,   7, "#9E9E9E")
        circle(t, wx, y+1,   3, "#616161")


def draw_bus(t, x, y):
    BW, BH = 120, 48
    rect(t, x, y, BW, BH, "#FFD600")
    rect(t, x, y+BH, BW, 8,  "#F9A825")
    for i in range(4):
        rect(t, x+10+i*26, y+18, 20, 22, "#B3E5FC")
    rect(t, x+4,  y+22,  6, 14, "#B3E5FC")
    rect(t, x+BW-3, y+12, 4, 12, "#FFEE58") # Headlight
    
    if NIGHT_MODE:
        poly(t, [(x+BW, y+12), (x+BW+65, y-5), (x+BW+65, y+35)], "#FFF59D")
        circle(t, x+BW-1, y+18, 6, "#FFEE58") # Headlight glow
        
    for wx in [x+18, x+BW-20]:
        circle(t, wx, y+1,  15, "#212121")
        circle(t, wx, y+1,   8, "#757575")
        circle(t, wx, y+1,   3, "#424242")


# ──────────────────────────────────────────────────────────
#  BIRDS
# ──────────────────────────────────────────────────────────

def draw_bird(t, x, y, color):
    t.penup()
    t.goto(x, y)
    t.pencolor(color)
    t.pensize(2)

    t.setheading(35)
    t.pendown()
    t.forward(10)

    t.penup()
    t.goto(x, y)

    t.setheading(145)
    t.pendown()
    t.forward(10)
    t.penup()


# ──────────────────────────────────────────────────────────
#  ANIMATION STATE
# ──────────────────────────────────────────────────────────

vehicles = [
    [-640, -348, 2.6, "bus",  "#FFD600", None      ],   
    [-460, -346, 3.5, "car",  "#E53935", "#E53935" ],   
    [-160, -347, 4.2, "car",  "#00BCD4", "#00BCD4" ],   
    [ 200, -347, 3.0, "car",  "#7B1FA2", "#9C27B0" ],   
]

clouds = [
    [-490, 280, 0.45, 1.15],
    [ -10, 300, 0.28, 0.90],
    [ 370, 290, 0.38, 0.95],
]

birds = [
    [-350, 260, 1.5],
    [-325, 275, 1.5],
    [-340, 290, 1.5],
    [ 280, 280, 2.0],
    [ 300, 300, 2.0],
    [ 315, 265, 2.0],
]

anim_pen = pen()
cloud_pen2 = pen()
bird_pen = pen()
tree_pen = pen()
flower_pen = pen()
lamp_light_pen = pen()

time_val = 0.0


def redraw_lamp_lights():
    lamp_light_pen.clear()
    draw_lamp_light(lamp_light_pen, -445, -250, NIGHT_MODE)
    draw_lamp_light(lamp_light_pen, 395, -250, NIGHT_MODE)


def redraw_vehicles():
    anim_pen.clear()
    for v in vehicles:
        vx, vy, _, vtype, vcol, vroof = v
        if vtype == "car":
            draw_car(anim_pen, vx, vy, vcol, vroof)
        else:
            draw_bus(anim_pen, vx, vy)


def update_vehicles():
    for v in vehicles:
        v[0] += v[2]
        vw = 80 if v[3] == "car" else 120
        if v[0] > HALF_W + 30:
            v[0] = -HALF_W - vw - 30


def redraw_clouds():
    cloud_pen2.clear()
    for c in clouds:
        draw_cloud(cloud_pen2, c[0], c[1], c[3])


def update_clouds():
    for c in clouds:
        c[0] += c[2]
        if c[0] > HALF_W + 130:
            c[0] = -HALF_W - 130


def redraw_birds():
    bird_pen.clear()
    bird_color = WHITE_COLOR if NIGHT_MODE else BLACK_COLOR
    for b in birds:
        draw_bird(bird_pen, b[0], b[1], bird_color)


def update_birds():
    for b in birds:
        b[0] += b[2]
        if b[0] > HALF_W + 50:
            b[0] = -HALF_W - 50


# ──────────────────────────────────────────────────────────
#  STATIC SCENE DRAW
# ──────────────────────────────────────────────────────────
static_pen = pen()

def draw_static_scene():
    static_pen.clear()

    draw_sky(static_pen)
    draw_stars(static_pen)
    draw_hills(static_pen)
    draw_buildings(static_pen)
    draw_sun(static_pen)
    draw_river(static_pen)
    draw_grass(static_pen)
    draw_mosque(static_pen)
    draw_microphone_stand(static_pen, -150, -92)
    draw_connecting_road(static_pen)
    
    redraw_trees(tree_pen, 0)
    redraw_flowers(flower_pen, 0)
    
    draw_lamp_structure(static_pen, -445, -250)
    draw_lamp_structure(static_pen, 395, -250)
    
    redraw_lamp_lights()
    draw_road(static_pen)


# ──────────────────────────────────────────────────────────
#  ANIMATION LOOP
# ──────────────────────────────────────────────────────────

def animate():
    global time_val
    time_val += 0.25
    
    update_vehicles()
    redraw_vehicles()
    
    update_clouds()
    redraw_clouds()
    
    update_birds()
    redraw_birds()
    
    turtle.update()
    screen.ontimer(animate, 30) 


def toggle_mode():
    global NIGHT_MODE

    NIGHT_MODE = not NIGHT_MODE

    anim_pen.clear()
    cloud_pen2.clear()
    bird_pen.clear()
    static_pen.clear()

    draw_static_scene()
    redraw_clouds()
    redraw_birds()
    redraw_vehicles()
    turtle.update()


# ──────────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    draw_static_scene()
    redraw_clouds()
    redraw_birds()
    turtle.update()

    screen.listen()
    screen.onkey(toggle_mode, "m")

    animate()
    turtle.done()
