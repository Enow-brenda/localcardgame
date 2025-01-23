import pygame
import random
from classes.Card import Card


pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.Font(None, 25)
shuffle = pygame.mixer.Sound("A:\education\pygame\LocalCardsGame\sounds\game_sound.wav")
class Deck:
    # creating a deck with a set of images and back images so that i can use the deck to have my cards
    def __init__(self, card_images, back_image,constitution):
        self.image = pygame.transform.scale(back_image,(100,150))
        self.rect = self.image.get_rect(topleft=(20,250 ))
        self.cards = [Card(image, back_image,constitution[i]) for i,image in enumerate(card_images)]
        random.shuffle(self.cards)

    def deal_card(self,used_cards):
        # this is to draw a card from the deck
        if self.cards:
            return self.cards.pop()


    def refill(self,used_cards):
        self.cards = used_cards
        for card in self.cards:
            card.flip(face_up=False)
        random.shuffle(self.cards)
        shuffle.play()

    def is_empty(self):
        return len(self.cards) == 0

    def draw_deck(self,screen):
        screen.blit(self.image,(20,250))
        deck_text = font.render("Deck : " + str(len(self.cards)), True, WHITE)
        screen.blit(deck_text, (30, ( 650// 2) + (150// 2) + 10))

