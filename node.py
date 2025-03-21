import pygame, time, math, noise

class Node:
    def __init__(self, pos, size, direction, border):
        self.ori_pos = pos
        self.x, self.y = pos
        self.vel = pygame.math.Vector2(0, 0)

        self.direction = direction
        self.border = border

        self.size = size
        self.rect = pygame.Rect(self.x, self.y, size, size)
    
    def draw(self, draw_surf, camera_offset):
        pygame.draw.circle(draw_surf, 'white', (self.x - camera_offset[0], self.y - camera_offset[1]), 5)
    
    def interact(self, pos, rel=(0, 0)):
        if self.rect.collidepoint(pos):
            if self.direction == 'h' and abs(rel[1]) > 0: # drag up and down
                self.rect.centery = max(min(pos[1], self.ori_pos[1] + 100), self.ori_pos[1] - 100)
                self.y = self.rect.y
                self.vel.y = 0
            elif self.direction == 'v' and abs(rel[0]) > 0: # drag left and right
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

        # chunks of nodes
        # self.chunks = [[Node((x, 300), self.size, 'h') for x in range(0, 600+1, 10)]]
        self.chunks = []

    def draw(self, draw_surf, camera_offset=[0, 0]):
        for nodes in self.chunks:
            # [node.draw(draw_surf, camera_offset) for node in self.nodes]
            # start_node = [(nodes[0].rect.x, 600)] # horizontal
            # end_node = [(nodes[-1].rect.x, 600)] # horizontal

            # start_node = [(0, self.nodes[0].rect.y)] # vertical
            # end_node = [(0, self.nodes[-1].rect.y)] # vertical

            if nodes[0].direction == 'h':
                start_node = [(nodes[0].rect.x, nodes[0].border)]
                end_node = [(nodes[-1].rect.x, nodes[-1].border)]
            else:
                start_node = [(nodes[0].border, nodes[0].rect.y)]
                end_node = [(nodes[-1].border, nodes[-1].rect.y)]

            pygame.draw.polygon(draw_surf, 'blue', start_node + [node.rect.topleft for node in nodes] + end_node)
            pygame.draw.lines(draw_surf, 'white', True, start_node + [node.rect.topleft for node in nodes] + end_node, 4)
    
    def add_chunk(self, start, end, direction='h'):
        size = end[0] - start[0], end[1] - start[1]

        if direction == 'h':
            self.chunks.append([Node((start[0] + x, start[1]), self.size, direction, end[1]) for x in range(0, size[0] + 1, 10)])
        else:
            self.chunks.append([Node((start[0], start[1] + y), self.size, direction, end[0]) for y in range(0, size[1] + 1, 10)])

    def update(self, delta_time):
        self.dt = delta_time

        mpos = pygame.mouse.get_pos()
        mrel = pygame.mouse.get_rel()
        
        for nodes in self.chunks:
            for i, node in enumerate(nodes):
                if not node.interact(mpos, mrel):
                    node.update(self.dt)
                    node.update_pos()

                if i > 0:
                    if nodes[i - 1].direction == 'h':
                        nodes[i - 1].spread_horizontally(node, self.dt, speed=0.1)
                    else:
                        nodes[i - 1].spread_vertically(node, self.dt, speed=0.1)
                if i < len(nodes) - 1:
                    if nodes[i + 1].direction == 'h':
                        nodes[i + 1].spread_horizontally(node, self.dt, speed=0.1)
                    else:
                        nodes[i + 1].spread_vertically(node, self.dt, speed=0.1)
