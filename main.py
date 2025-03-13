import pygame
from node import NodeManager

class App:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 600, 500
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()

        self.fps_event = pygame.USEREVENT + 1
        self.fps_timer = pygame.time.set_timer(self.fps_event, 500)
    
        self.running = True

        # Water Nodes
        self.node_manager = NodeManager()
        self.WATER_SURF = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.WATER_SURF.set_colorkey((0, 0, 0)) # color to refresh
        self.WATER_SURF.set_alpha(255)
    
    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == self.fps_event:
                    pygame.display.set_caption(f"FPS: {self.clock.get_fps():.1f}")
            
            dt = self.clock.tick(1000) / 1000
            dt *= 60
            if dt > 1:
                dt = 1 
            
            self.window.fill((30, 30, 30))
            self.WATER_SURF.fill((0, 0, 0))

            self.node_manager.draw(self.WATER_SURF, [0, 0])
            self.node_manager.update(dt)

            pygame.draw.circle(self.window, 'red', pygame.mouse.get_pos(), 32)
            self.window.blit(self.WATER_SURF, (0, 0), special_flags=pygame.BLEND_ADD)

            pygame.display.flip()
    

if __name__ == "__main__":
    app = App()
    app.update()
