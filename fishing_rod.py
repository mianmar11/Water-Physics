import pygame
from physics_attrib import *

class Bobber:
    def __init__(self, x, y, radius=10, vel=(0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 0, 0)  # Red color for the bobber

        self.is_active = False # Flag to use whether to update, display the bobber or not

        self.in_water = False
        self.on_surface = False
        self.water_interaction_count = 3

        self.vel = pygame.math.Vector2(*vel)

    def draw(self, draw_surf, camera_offset=[0, 0]):
        pygame.draw.circle(draw_surf, self.color, (int(self.x) - camera_offset[0], int(self.y) - camera_offset[1]), self.radius)

    def check_boundary_collision(self, chunk):
        # Get the first (topleft) and last (bottomright) nodes from the chunk 
        # Set up a rect with the first and last nodes data 
        # Check if the bobber is collided with the Rect
        
        first_node = (chunk[0].ori_pos[0], chunk[0].ori_pos[1])
        last_node = (chunk[-1].ori_pos[0], chunk[-1].ori_pos[1] + chunk[-1].border)
        chunk_rect = pygame.Rect(first_node[0], first_node[1], (last_node[0] - first_node[0]), (last_node[1] - first_node[1]))

        if chunk_rect.colliderect(pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)):
            self.in_water = True
            
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
        self.in_water = False

    def update(self, dt):
        self.dt = dt

        # Apply Gravity and Limit Downward Speed
        if self.in_water == False:
            self.vel.y += GRAVITY * self.dt  # Apply gravity to the vertical velocity
            if self.vel.y > 24:  # Limit the falling speed
                self.vel.y = 24
        
        elif self.in_water == True:
            if self.vel.y > 0:
                self.vel.y += 5 * BUOYANCY * self.dt  # Apply buoyancy with extra force to the vertical velocity
            elif self.vel.y <= 0:
                self.vel.y += BUOYANCY * self.dt  # Apply buoyancy to the vertical velocity
                if self.vel.y < -6:
                    self.vel.y = -6

        self.x += self.vel.x * self.dt
        self.y += self.vel.y * self.dt

        self.in_water = False 

    def __call__(self):
        return self.x, self.y
