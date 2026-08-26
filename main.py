import pygame
from node import NodeManager
from fishing_rod import Bobber

class App:
    def __init__(self):
        pygame.init()

        # Create Window
        self.WIDTH, self.HEIGHT = 640, 640
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()

        # FPS Timer to Display FPS in the Window Title
        self.fps_event = pygame.USEREVENT + 1
        self.fps_timer = pygame.time.set_timer(self.fps_event, 500)
    
        self.running = True

        # Water Nodes
        self.node_manager = NodeManager()
        self.WATER_SURF = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA).convert_alpha() # Create a Indepedent Surface for the Water Nodes and Polygon Surface
        self.WATER_SURF.set_colorkey((0, 0, 0)) # Color key for transparency (use to refresh the Surface)
        self.WATER_SURF.set_alpha(128) # Transparency of the water surface

        # Fishing Rod
        self.bobber = Bobber(0, 0, 10, (0, 0))

        # brush and stuff
        self.grid_size = 30
        self.pos1 = None
        self.pos2 = None
    
    def update(self):
        while self.running:
            dt = self.clock.tick(1000) / 1000
            dt *= 60
            if dt > 1:
                dt = 1 
            
            # Get Mouse Position
            self.mpos = pygame.mouse.get_pos()
            
            # Clear Window and Water Surface
            self.window.fill((0, 0, 0))
            self.WATER_SURF.fill((0, 0, 0))

            # Draw and Update Water Nodes and Polygon Surface onto the Water Surface
            self.node_manager.draw(self.WATER_SURF, [0, 0])
            self.node_manager.update(dt, self.bobber)
            

            # Draw and Update Bobbers onto the Window
            # [[bobber.update(dt), [bobber.check_boundary_collision(nodes) for nodes in self.node_manager.chunks], bobber.draw(self.window, (0, 0)), self.bobbers.remove(bobber) if bobber.y > self.HEIGHT else None] for bobber in self.bobbers]
            if self.bobber.is_active == True:
                self.bobber.update(dt)
                [self.bobber.check_boundary_collision(nodes) for nodes in self.node_manager.chunks]
                self.bobber.draw(self.window, (0, 0))

            # Draw the Water Surface onto the Window with Additive Blending
            # pygame.draw.circle(self.window, 'red', self.mpos, 32)
            self.window.blit(self.WATER_SURF, (0, 0), special_flags=pygame.BLEND_ADD)

            # ui stuff
            if self.pos1 != None:
                self.pos2 = self.mpos[0]//self.grid_size * self.grid_size, self.mpos[1]//self.grid_size * self.grid_size, 
                dx, dy = self.pos2[0] - self.pos1[0], self.pos2[1] - self.pos1[1]
                pygame.draw.lines(self.window, 'white', True, [self.pos1, (self.pos1[0], self.pos1[1] + dy), self.pos2, (self.pos1[0] + dx, self.pos1[1]),])

            # Update the Display and Handle Events
            pygame.display.flip()
            for event in pygame.event.get():

                # Handle Window Close Event
                if event.type == pygame.QUIT:
                    self.running = False
                
                # FPS timer to update the fps in the window title
                if event.type == self.fps_event:
                    pygame.display.set_caption(f"FPS: {self.clock.get_fps():.1f}")
                
                # Mouse Button Down Event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Set First Position
                    if event.button == pygame.BUTTON_LEFT:
                        self.pos1 = (self.mpos[0]//self.grid_size * self.grid_size, self.mpos[1]//self.grid_size * self.grid_size)
                    
                    # Create Bobber
                    if event.button == pygame.BUTTON_RIGHT:
                        if self.bobber.is_active == False:
                            self.bobber.activate()
                            self.bobber.set_pos(*self.mpos)
                            self.bobber.set_vel((0, -10))
                        elif self.bobber.is_active == True:
                            self.bobber.deactivate()
                
                # Mouse Button Up Event
                if event.type == pygame.MOUSEBUTTONUP:
                    # Set Second Position
                    if event.button == pygame.BUTTON_LEFT:
                        # Create Water Nodes
                        if (self.pos1[0] - self.pos2[0])**2 + (self.pos1[1] - self.pos2[1])**2 != 0:
                            # Border
                            start = [min(self.pos1[0], self.pos2[0]), min(self.pos1[1], self.pos2[1])]
                            end = [max(self.pos1[0], self.pos2[0]), max(self.pos1[1], self.pos2[1])]
                            self.node_manager.add_chunk(start, end, 'h')

                        self.pos1 = None
    

if __name__ == "__main__":
    app = App()
    app.update()
