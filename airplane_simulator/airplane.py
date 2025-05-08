import pygame



class Airplane:
    def __init__(self, x, y):
        self.x = x  # Fixed horizontal position
        self.y = y  # Vertical position
        self.lift = 0

    def update(self, keys):
        if keys[pygame.K_UP]:  # Move up
            self.lift = -5
        elif keys[pygame.K_DOWN]:  # Move down
            self.lift = 5
        else:
            self.lift = 0

        self.y += self.lift
        # Prevent airplane from leaving the screen
        self.y = max(0, min(550, self.y))