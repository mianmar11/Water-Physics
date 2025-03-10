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
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(self.x, self.y, 16, 16).collidepoint(pos):
                self.rect.centery = pos[1]
                self.y = self.rect.y
                self.vel.y = 0
                return True
        return

    def wave(self, t, amplitude=0.5, waves=5, speed=2):
        value = noise.pnoise1(self.x * 0.04 + t * 0.0032)
        self.vel.y += amplitude * (math.sin(waves * self.x + speed * t) + value) * self.dt

    def update(self, delta_time):
        self.dt = delta_time

        # update movement
        extension = self.rect.y - self.ori_pos[1]
        energy_loss = -0.06 * self.vel.y  # % of velocity is lost
        
        stiffness = 0.04 # stiffness of spring which determines its movment (less = bouncy, more = rigid)
        force = -stiffness * extension + energy_loss

        self.vel.y += force * self.dt

    def update_pos(self):
        self.y += self.vel.y * self.dt
        self.rect.centery = self.y

    def spread(self, node, dt, speed=0.06):
        self.vel.y += (node.y - self.y) * speed * dt


class NodeManager:
    def __init__(self):
        self.size = 16

        self.nodes = [Node((x, 300), 10) for x in range(0, 600 + 1, 10)]
    
    def draw(self, draw_surf, camera_offset=[0, 0]):
        # [node.draw(draw_surf, camera_offset) for node in self.nodes]
        pygame.draw.lines(draw_surf, 'white', False, [node.rect.topleft for node in self.nodes], 1)
    
    def update(self, delta_time):
        self.dt = delta_time

        for i, node in enumerate(self.nodes):
            if not node.interact(pygame.mouse.get_pos()):
                node.update(self.dt)
                node.update_pos()
                node.wave(time.time())

            if i > 0:
                self.nodes[i - 1].spread(node, self.dt, speed=0.1)
            if i < len(self.nodes) - 1:
                self.nodes[i + 1].spread(node, self.dt, speed=0.1)
