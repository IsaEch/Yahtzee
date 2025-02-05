import pygame

import Constants as C


class Dice(pygame.sprite.Sprite):

    def __init__(self, x:int, y: int):
        super().__init__()
        # self.dice_sheet = pygame.image.load("images/dice_sheet5.png").convert_alpha()
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(C.DICE_X, C.DICE_Y))
        self.animation_speed = C.ANIMATION_SPEED    # Adjust the animation speed
        self.last_update = pygame.time.get_ticks()
        self.animation_running = False # Set to False to stop the animation
        self.held = False

    def load_frames(self):
        """Load the dice frames from the dice sheet to be used in the animation"""
        frames = []
        for n in range(1, 7):
            frame = pygame.image.load(f"images/dice{n}.png").convert_alpha()
            # Scale the dice image to make it bigger
            frame = pygame.transform.scale(frame, (C.DICE_WIDTH, C.DICE_HEIGHT))
            frames.append(frame)
        return frames

    def update(self):
        """Update the dice animation"""
        if self.animation_running:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed * 1000:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 6
                self.image = self.frames[self.current_frame]

    def start_animation(self):
        """Start the dice animation"""
        self.animation_running = True

    def stop_animation(self, frame):
        """Stop the animation on a specific frame to show what was rolled"""
        self.animation_running = False
        self.current = frame - 1
        self.image = self.frames[self.current]
