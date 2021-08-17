import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, unit_size, pos, type):
        pygame.sprite.Sprite.__init__(self)

        self.unit_size = unit_size
        self.posx, self.posy = self.pos = pos
        self.is_hidden = True
        self.type = type
        self.sprite = None
        self.number = 0
        self.is_flagged = False
        self.set_sprite()
        self.rect = self.sprite.get_rect(topleft=self.pos)

    # This function sets the sprite based on the member variable "type"
    def set_sprite(self):
        if self.type == "0":
            self.sprite = pygame.image.load("img\\empty.png").convert()
        elif self.type == "mine":
            self.sprite = pygame.image.load("img\\mine.png").convert()
        elif self.type == "1":
            self.sprite = pygame.image.load("img\\one.png").convert()
        elif self.type == "2":
            self.sprite = pygame.image.load("img\\two.png").convert()
        elif self.type == "3":
            self.sprite = pygame.image.load("img\\three.png").convert()
        elif self.type == "4":
            self.sprite = pygame.image.load("img\\four.png").convert()
        elif self.type == "5":
            self.sprite = pygame.image.load("img\\five.png").convert()
        elif self.type == "6":
            self.sprite = pygame.image.load("img\\six.png").convert()
        elif self.type == "7":
            self.sprite = pygame.image.load("img\\seven.png").convert()
        elif self.type == "8":
            self.sprite = pygame.image.load("img\\eight.png").convert()

    def reveal(self):
        self.is_hidden = False

    def update(self):
        pass

    def render(self, screen):
        if self.is_hidden and not self.is_flagged:
            screen.blit(pygame.image.load("img\\metal_block.png").convert(), self.pos)
        elif self.is_flagged:
            screen.blit(pygame.image.load("img\\flag.png").convert(), self.pos)
        else:
            screen.blit(self.sprite, self.pos)
