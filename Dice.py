import random
import pygame
import Constants as C


class Dice(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = self.load_frames()    # Load the dice frames (1, 2, 3, 4, 5, 6; 6 sides of a dice)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]    # Shows the current side of the dice
        self.rect = self.image.get_rect(center=(x, y))  # Position of the dice on the screen
        self.animation_speed = C.ANIMATION_SPEED    # Adjust the animation speed
        self.last_update = pygame.time.get_ticks()
        self.animation_running = False  # Set to False to stop the animation
        self.held = False
        self.value = -1

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

    def roll(self):
        """Roll the dice and stop the animation on a frame that matches the random int"""
        self.value = random.randint(1, 6)
        return self.value

    def is_clicked(self):
        """Check if the dice is clicked"""
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
