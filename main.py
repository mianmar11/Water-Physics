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

        self.node_manager = NodeManager()
    
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

            self.node_manager.draw(self.window, [0, 0])
            self.node_manager.update(dt)

            pygame.display.flip()
    

if __name__ == "__main__":
    app = App()
    app.update()
