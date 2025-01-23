import pygame

CARD_WIDTH, CARD_HEIGHT = 100, 150
BLACK = (0,0,0)
RED = (255,0,0)


class Card(pygame.sprite.Sprite):
    def __init__(self, image, back_image,constitution, x=20, y=250, face_up=False):
        super().__init__()
        self.x = x
        self.y = y
        self.suit = constitution['suit']
        self.rank = constitution['rank']
        self.front_image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        self.back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
        self.image = self.front_image if face_up else self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.face_up = face_up

    def flip(self, face_up=True):
        self.face_up = face_up
        self.image = self.front_image if face_up else self.back_image

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.y = self.y - 10

        else:
            self.y = self.y
        self.rect.y = self.y
    def draw(self,screen):
        self.image = self.front_image if self.face_up else self.back_image
        screen.blit(self.image,(self.x,self.y))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        if self.face_up:
            if self.suit in ('heart','diamond'):
                color = RED
            else:
                color= BLACK
            pygame.draw.rect(screen, color, self.rect, 1)
    def move_to(self,end_pos, duration, screen, clock, background_color):
        '''
        x_start, y_start = self.image.get_rect().x , self.image.get_rect().y
        x_end, y_end = end_pos
        frames = int(duration * 60)  # Assuming 60 FPS
        for frame in range(frames):
            t = frame / frames
            x = x_start + (x_end - x_start) * t
            y = y_start + (y_end - y_start) * t
            screen.fill(background_color)
            screen.blit(self.image, (x, y))  # Draw the card at the current position
            pygame.display.flip()
            clock.tick(60)
        '''

        #screen.blit(self.image, (end_pos))
        #self.rect = self.image.get_rect(topleft=(end_pos))
        self.x ,self.y = end_pos
        pygame.display.flip()
        clock.tick(60)

