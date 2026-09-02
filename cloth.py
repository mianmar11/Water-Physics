import math
from physics_attrib import *


CONSTRAINT_ADUSTMENT_ITERATION = 5 # more = stiffer cloth 
SPACING = 25
'''This will make vertical string, good to attach with the Bobber.'''
COLS = 1
ROWS = 12


# --------------------------- Classes --------------------------- 
# Node Point
class Point:
    def __init__(self, x, y, pinned=False):
        self.old_x = x
        self.old_y = y

        self.x = self.old_x
        self.y = self.old_y

        self.vel = [0, 0]

        self.pinned = pinned
    
    def update(self, dt):
        if self.pinned:
            return
        self.vel[0] += (((self.x - self.old_x) * FRICTION) - self.vel[0]) * dt
        self.vel[1] += (((self.y - self.old_y) * FRICTION) - self.vel[1]) * dt

        self.old_x = self.x
        self.old_y = self.y 

        self.x += self.vel[0] 
        self.y += self.vel[1] + GRAVITY * dt

    def drag(self, mx, my):
        self.x = self.old_x = mx
        self.y = self.old_y = my
    
    def __call__(self) -> tuple:
        return self.x, self.y

# Constaint    
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2 
        self.length = math.hypot(p1.x - p2.x, p1.y - p2.y)
        self.active = True # Flag to use if it has been cut or not 
    
    def satisfy_position(self):
        if self.active == False:
            return 
        
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y 
        distance = math.hypot(dx, dy)

        diff = (self.length - distance) / distance
        if diff == 0:
            return 
        
        offset_x = dx * diff * 0.5
        offset_y = dy * diff * 0.5

        if not self.p1.pinned:
            self.p1.x -= offset_x
            self.p1.y -= offset_y
        
        if not self.p2.pinned:
            self.p2.x += offset_x
            self.p2.y += offset_y


# --------------------------- Functions --------------------------- 
def find_nearest_point(points, mx, my) -> Point:
    for point in points:
        dx = mx - point.x
        dy = my - point.y
        dist = math.hypot(dx, dy)

        if dist < 20:
            return point
    return 

def find_nearest_contraint(lines, mx, my) -> Line:
    for stick in lines:
        dx = (stick.p2.x + stick.p1.x)/2
        dy = (stick.p2.y + stick.p1.y)/2
        distance = math.hypot(dx - mx, dy - my)

        if distance < 10:
            return stick
    return

def build_cloth(start_pos=(0, 0)):
    # Build points
    all_points = []
    for col in range(COLS):
        row_points = []
        x = start_pos[0] + col * SPACING

        for row in range(ROWS):
            y = start_pos[1] + row * SPACING
            row_points.append(Point(x, y, True if row == 0 else False))
        
        all_points.append(row_points)

    # Build Line Constraints
    line_constraints = []
    for col in range(COLS):
        for row in range(ROWS):

            # Attach Horizontal Points
            if col + 1 < COLS: 
                line_constraints.append(Line(all_points[col][row], all_points[col + 1][row]))

            # Attach Vertical Points
            if row + 1 < ROWS:
                line_constraints.append(Line(all_points[col][row], all_points[col][row + 1]))
    
    return all_points, line_constraints

def create_string_node(position_list, constraint_list, current_pos):
    position_list.append(Point(current_pos[0], current_pos[1], True if len(position_list) == 0 else False))
    if len(position_list) > 1:
        constraint_list.append(Line(position_list[-1], position_list[-2]))

def update_cloth(points, constraints, dt):
    if not len(points) or not len(constraints):
        return 
    
    # Points
    for point in points:
        point.update(dt)
    
    # Constraints
    for i in range(CONSTRAINT_ADUSTMENT_ITERATION):
        for stick in constraints:
            stick.satisfy_position()
