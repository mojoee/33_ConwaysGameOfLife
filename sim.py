from config import Config
import pygame
from pygame.sprite import Group, Sprite
from typing import Sequence
from pygame.sprite import AbstractGroup, Sprite
from abc import ABC


class Sim():
    def __init__(self, n, screen) -> None:
        self.field = None
        self.minions = None
        self.alive = True
        self.screen = screen
        self.paddingH = Config.screenResolution[0]/2-n/2*16
        self.paddingV = Config.screenResolution[1]/2-n/2*16
        self.clock = pygame.time.Clock()
        self.clockFont = pygame.font.SysFont(Config.clockFont, 30)
        self.setup(n)

    def setup(self, n):
        self.field = Field()
        for i in range(n):
            for j in range(n):
                SimTile(self.field, top=i*16, left=j*16,
                        paddingH=self.paddingH, paddingV=self.paddingV)

        self.field.draw(self.screen)

    def game_over(self):
        self.alive = False

    def count_bombs(self, x, y):
        pass


class Field(pygame.sprite.Group):
    def __init__(self, *sprites: Sprite | Sequence[Sprite]) -> None:
        super().__init__(*sprites)


class Tile(pygame.sprite.Sprite, ABC):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        if not self.clicked:
                            self.change_color(Config.colorClick)
                        else:
                            self.change_color(Config.noClick)
                elif event.button == 3:
                    pass

    def change_color(self):
        pass


class SimTile(Tile):
    def __init__(self, *groups: AbstractGroup, top, left, paddingH, paddingV) -> None:
        super().__init__(*groups)
        self.groups = groups
        self.width = 16
        self.top = paddingH+top
        self.left = paddingV+left
        self.bottom = top+self.width
        self.right = left+self.width
        self.rect = pygame.Rect(self.top, self.left, self.width, self.width)
        # self.image = self.image.copy()
        self.image = pygame.Surface([self.width, self.width])
        self.image.fill(Config.noClick)
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), Config.borderWidth)
        self.clicked = False
        self.dead = True

    def change_color(self, color=(0, 255, 0)):
        self.image.fill(color)
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), Config.borderWidth)
        self.clicked = not self.clicked

    
    def die(self):
        self.change_color(Config.noClick)
        self.dead = True
        self.clicked = False


    def awaken(self):
        self.change_color(Config.colorClick)
        self.dead = False
        self.clicked = True


    def count_neighbors(self):
        coordinates_x = [self.top+self.width, self.top, self.top -self.width]
        coordinates_y = [self.left+self.width, self.left, self.left -self.width]
        n = 0
        for spr in self.groups[0].sprites():
            if spr.dead:
                continue
            if spr.left in coordinates_y:
                if spr.top in coordinates_x:
                    n += 1
        self.n = n


    def update(self, events):
        super().update(events)
        self.count_neighbors()
        if self.n <= 1:
            self.die()
        elif self.n >= 4:
            self.die()
        elif self.n == 3 and self.dead == True:
            self.awaken()

