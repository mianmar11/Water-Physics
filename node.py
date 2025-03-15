import pygame, time, math, noise

class Node:
    def __init__(self, pos, size, direction):
        self.ori_pos = pos
        self.x, self.y = pos
        self.vel = pygame.math.Vector2(0, 0)

        self.direction = direction

        self.size = size
        self.rect = pygame.Rect(self.x, self.y, size, size)
    
    def draw(self, draw_surf, camera_offset):
        pygame.draw.circle(draw_surf, 'white', (self.x - camera_offset[0], self.y - camera_offset[1]), 5)
    
    def interact(self, pos):
        if self.rect.collidepoint(pos):
            if self.direction == 'h': # drag up and down
                self.rect.centery = max(min(pos[1], self.ori_pos[1] + 100), self.ori_pos[1] - 100)
                self.y = self.rect.y
                self.vel.y = 0
            else: # drag left and right
                self.rect.centerx = max(min(pos[0], self.ori_pos[0] + 100), self.ori_pos[0] - 100)
                self.x = self.rect.x
                self.vel.x = 0
            return True
        return False

    def wave_y(self, t, amplitude=0.5, waves=5, speed=4):
        value = noise.pnoise1(self.x * 0.01 + t * 0.0001)
        self.vel.y += amplitude * (math.sin(waves * self.x + speed * t) + 2 * value) * self.dt
    
    def wave_x(self, t, amplitude=0.5, waves=5, speed=4):
        value = noise.pnoise1(self.y * 0.01 + t * 0.0001)
        self.vel.x += amplitude * (math.sin(waves * self.y + speed * t) + 2 * value) * self.dt

    def update(self, delta_time):
        self.dt = delta_time
        
        if self.direction == 'h':
            self.apply_y_physics()
            self.wave_y(time.time())
        else:
            self.apply_x_physics()
            self.wave_x(time.time())

    def apply_y_physics(self):
        # update movement
        extension = self.rect.y - self.ori_pos[1]
        energy_loss = -0.06 * self.vel.y  # % of velocity is lost
        
        stiffness = 0.04 # stiffness of spring which determines its movment (less = bouncy, more = rigid)
        force = -stiffness * extension + energy_loss

        self.vel.y += force * self.dt
    
    def apply_x_physics(self):
        # update movement
        extension = self.rect.x - self.ori_pos[0]
        energy_loss = -0.06 * self.vel.x  # % of velocity is lost

        stiffness = 0.04 # stiffness of spring which determines its movment (less = bouncy, more = rigid)
        force = -stiffness * extension + energy_loss

        self.vel.x += force * self.dt

    def update_pos(self):
        self.x += self.vel.x * self.dt
        self.rect.x = self.x
        self.y += self.vel.y * self.dt
        self.rect.y = self.y

    def spread_horizontally(self, node, dt, speed=0.06):
        self.vel.y += (node.y - self.y) * speed * dt
    
    def spread_vertically(self, node, dt, speed=0.06):
        self.vel.x += (node.x - self.x) * speed * dt


class NodeManager:
    def __init__(self):
        self.size = 10

        self.nodes = [Node((300, x), self.size, 'v') for x in range(0, 600+1, 10)]

    def draw(self, draw_surf, camera_offset=[0, 0]):
        # [node.draw(draw_surf, camera_offset) for node in self.nodes]
        # start_node = [(self.nodes[0].rect.x, 600)] # horizontal
        # end_node = [(self.nodes[-1].rect.x, 600)] # horizontal

        start_node = [(0, self.nodes[0].rect.y)] # vertical
        end_node = [(0, self.nodes[-1].rect.y)] # vertical

        pygame.draw.polygon(draw_surf, 'blue', start_node + [node.rect.topleft for node in self.nodes] + end_node)
        pygame.draw.lines(draw_surf, 'white', True, start_node + [node.rect.topleft for node in self.nodes] + end_node, 4)
    
    def update(self, delta_time):
        self.dt = delta_time

        for i, node in enumerate(self.nodes):
            if not node.interact(pygame.mouse.get_pos()):
                node.update(self.dt)
                node.update_pos()

            if i > 0:
                if self.nodes[i - 1].direction == 'h':
                    self.nodes[i - 1].spread_horizontally(node, self.dt, speed=0.1)
                else:
                    self.nodes[i - 1].spread_vertically(node, self.dt, speed=0.1)
            if i < len(self.nodes) - 1:
                if self.nodes[i + 1].direction == 'h':
                    self.nodes[i + 1].spread_horizontally(node, self.dt, speed=0.1)
                else:
                    self.nodes[i + 1].spread_vertically(node, self.dt, speed=0.1)
