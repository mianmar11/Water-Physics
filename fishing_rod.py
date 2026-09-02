import pygame
from physics_attrib import *
from cloth import Point, FRICTION

class Bobber(Point):
    def __init__(self, x, y, radius=10, vel=(0, 0)):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 0, 0)  # Red color for the bobber

        self.is_active = False # Flag to use whether to update, display the bobber or not
        self.has_touched_water = False
        self.in_water = False
        self.on_surface = False
        self.water_interaction_count = 3

        self.vel = pygame.math.Vector2(*vel)

        self.touched_water_event = pygame.USEREVENT + 2
        self.touched_water_event_timer = pygame.time.set_timer(self.touched_water_event, 50)

    def draw(self, draw_surf, camera_offset=[0, 0]):
        pygame.draw.circle(draw_surf, self.color, (int(self.x) - camera_offset[0], int(self.y) - camera_offset[1]), self.radius)

    def check_boundary_collision(self, chunk):
        # Get the first (topleft) and last (bottomright) nodes from the chunk 
        # Set up a rect with the first and last nodes data 
        # Check if the bobber is collided with the Rect
        
        first_node = (chunk[0].ori_pos[0], chunk[0].ori_pos[1])
        last_node = (chunk[-1].ori_pos[0], chunk[-1].border)
        chunk_rect = pygame.Rect(first_node[0], first_node[1], (last_node[0] - first_node[0]), (last_node[1] - first_node[1]))

        if chunk_rect.colliderect(pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)):
            self.in_water = True
            self.pinned = True
            
            for node in chunk:
                if node.rect.colliderect(pygame.Rect(self.x, self.y + self.radius, self.radius * 2, self.radius * 2)):
                    self.on_surface = True
                    self.in_water = False
                    break
                else:
                    self.on_surface = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_vel(self, vel=(0, -7)):
        self.vel.xy = vel

    def get_pos(self):
        return self.x, self.y
    
    def get_vel(self):
        return self.vel.xy
    
    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False

    def reset(self):
        self.water_interaction_count = 3
        self.has_touched_water = False
        self.in_water = False
        self.on_surface = False
        self.pinned = False

    def update_verlet_x_pos(self, dt):
        friction = FRICTION
        if self.in_water:
            friction = 0

        self.vel.x += (((self.x - self.old_x) * friction) - self.vel.x) * dt
        self.old_x = self.x
    
    def update_verlet_y_pos(self, dt):
        if self.pinned:
            return
        
        friction = FRICTION
        if self.in_water:
            friction = 0

        self.vel.y += (((self.y - self.old_y) * friction) - self.vel.y) * dt
        self.old_y = self.y

    def is_water_interaction_event(self, event):
        if event.type == self.touched_water_event:
            return True
        return False

    def update(self, dt):
        self.dt = dt

        # self.update_verlet_x_pos(dt)

        # Apply Gravity if not touching water or on surface
        if not self.in_water:
            self.vel.y += GRAVITY * self.dt  # Apply gravity to the vertical velocity
            if self.vel.y > 24:  # Limit the falling speed
                self.vel.y = 24
            
            # if not self.on_surface:
            #     self.update_verlet_y_pos(dt) # If absolutely no water interaction
        
        # Apply Buoyancy if in water
        elif self.in_water == True:
            
            # Update Vertical Velocity
            # Apply buoyancy with extra force to the vertical velocity
            if self.vel.y > 0:
                self.vel.y += 5 * BUOYANCY * self.dt  
            
            # Apply buoyancy to the vertical velocity
            elif self.vel.y <= 0:
                self.vel.y += BUOYANCY * self.dt 
                if self.vel.y < -6:
                    self.vel.y = -6
            
            # Update Horizontal Velocity
            self.vel.x += -self.vel.x * 0.08 * self.dt  # Apply damping to horizontal velocity in water

        # Update Position 
        self.x += self.vel.x * self.dt
        self.y += self.vel.y * self.dt

        self.in_water = False 
        self.on_surface = False

    def __call__(self):
        return self.x, self.y
