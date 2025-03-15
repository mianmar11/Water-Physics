import pygame, time, math, noise

class Node:
    def __init__(self, pos, size):
        self.ori_pos = pos
        self.x, self.y = pos
        self.vel = pygame.math.Vector2(0, 0)

        self.size = size
        self.rect = pygame.Rect(self.x, self.y, size, size)
    
    def draw(self, draw_surf, camera_offset):
        pygame.draw.circle(draw_surf, 'white', (self.x - camera_offset[0], self.y - camera_offset[1]), 5)
    
    def interact(self, pos):
        if self.rect.collidepoint(pos):
            self.rect.centery = max(min(pos[1], self.ori_pos[1] + 100), self.ori_pos[1] - 100)
            self.y = self.rect.y
            self.vel.y = 0
            return True
        return

    def wave_vertical(self, t, amplitude=0.5, waves=5, speed=4):
        value = noise.pnoise1(self.x * 0.01 + t * 0.0001)
        self.vel.y += amplitude * (math.sin(waves * self.x + speed * t) + 2 * value) * self.dt
    
    def wave_horizontal(self, t, amplitude=0.5, waves=5, speed=4):
        value = noise.pnoise1(self.y * 0.01 + t * 0.0001)
        self.vel.x += amplitude * (math.sin(waves * self.y + speed * t) + 2 * value) * self.dt

    def update(self, delta_time):
        self.dt = delta_time

        # self.apply_vertical_physics()
        self.apply_horizontal_physics()

    def apply_vertical_physics(self):
        # update movement
        extension = self.rect.y - self.ori_pos[1]
        energy_loss = -0.06 * self.vel.y  # % of velocity is lost
        
        stiffness = 0.04 # stiffness of spring which determines its movment (less = bouncy, more = rigid)
        force = -stiffness * extension + energy_loss

        self.vel.y += force * self.dt
    
    def apply_horizontal_physics(self):
        # update movement
        extension = self.rect.x - self.ori_pos[0]
        energy_loss = -0.06 * self.vel.x  # % of velocity is lost

        stiffness = 0.04 # stiffness of spring which determines its movment (less = bouncy, more = rigid)
        force = -stiffness * extension + energy_loss

        self.vel.x += force * self.dt

    def update_pos(self):
        self.x += self.vel.x * self.dt
        self.rect.centerx = self.x
        self.y += self.vel.y * self.dt
        self.rect.centery = self.y

    def spread_horizontal_neigbors(self, node, dt, speed=0.06):
        self.vel.y += (node.y - self.y) * speed * dt
    
    def spread_vertical_neigbors(self, node, dt, speed=0.06):
        self.vel.x += (node.x - self.x) * speed * dt


class NodeManager:
    def __init__(self):
        self.size = 10

        self.nodes = [Node((300, x), self.size) for x in range(0, 600+1, 10)]

    def draw(self, draw_surf, camera_offset=[0, 0]):
        # [node.draw(draw_surf, camera_offset) for node in self.nodes]
        # start_node = [(self.nodes[0].rect.x, 420)] # horizontal
        # end_node = [(self.nodes[-1].rect.x, 420)] # horizontal

        start_node = [(600, self.nodes[0].rect.y)] # vertical
        end_node = [(600, self.nodes[-1].rect.y)] # vertical

        pygame.draw.polygon(draw_surf, 'blue', start_node + [node.rect.topleft for node in self.nodes] + end_node)
        pygame.draw.lines(draw_surf, 'white', True, start_node + [node.rect.topleft for node in self.nodes] + end_node, 4)
    
    def update(self, delta_time):
        self.dt = delta_time

        for i, node in enumerate(self.nodes):
            if not node.interact(pygame.mouse.get_pos()):
                node.update(self.dt)
                node.update_pos()
                # node.wave_vertical(time.time())
                node.wave_horizontal(time.time())

            if i > 0:
                # self.nodes[i - 1].spread_horizontal_neigbors(node, self.dt, speed=0.1)
                self.nodes[i - 1].spread_vertical_neigbors(node, self.dt, speed=0.1)
            if i < len(self.nodes) - 1:
                # self.nodes[i + 1].spread_horizontal_neigbors(node, self.dt, speed=0.1)
                self.nodes[i + 1].spread_vertical_neigbors(node, self.dt, speed=0.1)
