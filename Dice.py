import random
import pygame
import Constants as C
import sys
import os

class Dice(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = self.load_frames()    # Load the dice frames (1, 2, 3, 4, 5, 6; 6 sides of a dice)
        self.current_frame = 0       # The current frame index of the dice
        self.image = self.frames[self.current_frame]    # Shows the current side of the dice
        self.rect = self.image.get_rect(center=(x, y))  # Position of the dice on the screen
        self.animation_speed = C.ANIMATION_SPEED    # Adjust the animation speed
        self.last_update = pygame.time.get_ticks()
        self.animation_running = False  # Set to False to stop the animation
        self.held = False
        self.value = -1


    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            # Running in a PyInstaller bundle
            return os.path.join(sys._MEIPASS, relative_path)
        # Running in development mode (not packed)
        return os.path.join(os.path.abspath("."), relative_path)

    def load_frames(self):
        """Load the dice frames from the images to be used in the animation"""
        frames = []
        for n in range(1, 7):
            image_path = self.resource_path(f"images/dice{n}.png")
            frame = pygame.image.load(image_path).convert_alpha()
            # Scale the dice image to make it bigger
            frame = pygame.transform.scale(frame, (C.DICE_WIDTH, C.DICE_HEIGHT))
            frames.append(frame)
        return frames

    def update(self):
        """Updates the dice animation. Controls the speed of the animation"""
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
        """Stop the animation on a specific frame to show what was rolled

        :param frame: The frame to stop the animation on
        """
        self.animation_running = False
        current = frame - 1
        self.image = self.frames[current]

    def roll(self):
        """Roll the dice and stop the animation on a frame that matches the random int

        :returns:
            int: The value of the dice roll/random int
        """
        self.value = random.randint(1, 6)
        return self.value

    def is_clicked(self):
        """Check if the dice is clicked

        :returns:
            bool: True if the dice is clicked, False otherwise
        """
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
