import random
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.Font(None, 22)
class Player:
    def __init__(self):
        self.hand = []

    def add_card(self, card,screen,clock,bg):
        if card:
            card.flip()
            self.hand.append(card)


            if len(self.hand)==0:
                card.move_to((50,480),1,screen,clock,bg)

            else:
                pos = 50 + (len(self.hand) * 110) ,480
                card.move_to(pos,1,screen,clock,bg)





    def play_card(self, card,center):
        if center.suit == card.suit or center.rank == card.rank:
            return True
        elif card.suit == 'joker' and card.rank == 'black':
            if center.suit in ('spades', 'club'):
                return True
        elif card.suit == 'joker' and card.rank == 'red':
            if center.suit in ('heart', 'diamond'):
                return True
        elif card.suit in ('spades', 'club') and center.suit == 'joker' and center.rank == 'black':
            return True
        elif card.suit in ('heart', 'diamond') and center.suit == 'joker' and center.rank == 'red':
            return True

    def special_card(self,card):
        if card.rank == 'A':
            return 0
        elif card.suit == 'joker':
            return 4
        elif card.rank == '7':
            return 2
        else:
            return None

    def arrange_hand(self, screen_width, card_width, card_height):
        for i, card in enumerate(self.hand):
            card.rect.topleft = (200 + i * (card_width + 10), screen_width - card_height - 20)

    def draw_hand(self, surface,pos,mouse_pos):
        num_cards = len(self.hand)

        # Calculate spacing
        if num_cards == 0:
            return  # No cards to draw

        max_spacing = 900 // (num_cards + 1)
        spacing = min(max_spacing, 110)  # Limit overlap

        # Start position (center the hand)
        start_x = (1000 - (num_cards - 1) * spacing - 100) // 2
        y = 650 - 150 - 50  # Fixed vertical position for the hand

        # Draw each card
        for i, card in enumerate(self.hand):
            card.x = start_x + i * spacing
            card.y = y
            card.update_hover(mouse_pos)
            card.draw(surface)
        hand_text = font.render("Cards in Hand : " + str(len(self.hand)), True, WHITE)
        surface.blit(hand_text, pos)
    def can_play(self,mycards,center):
        good_cards = []
        for card in mycards:
            if center.suit == card.suit or center.rank == card.rank:
                good_cards.append(card)
            elif card.suit == 'joker' and card.rank=='black':
                if center.suit in ('spades','club'):
                    good_cards.append(card)
            elif card.suit == 'joker' and card.rank=='red':
                if center.suit in ('heart','diamond'):
                    good_cards.append(card)
            elif card.suit in ('spades', 'club') and center.suit == 'joker' and center.rank=='black':
                good_cards.append(card)
            elif card.suit in ('heart','diamond') and center.suit == 'joker' and center.rank=='red':
                good_cards.append(card)
        return good_cards


class Computer(Player):
    def play_card(self,center_card):
        """Plays a card from the hand (simple AI)."""
        if self.hand:
            print((center_card.suit,center_card.rank))
            good_cards = self.can_play(self.hand,center_card)
            if len(good_cards)==0:
                return None
            else:
                return random.choice(good_cards)

        return None

    def draw_hand(self, surface,pos):
        num_cards = len(self.hand)
        if num_cards == 0:
            return

        # Card positioning logic for the computer
        max_spacing = 900 // (num_cards + 1)
        spacing = min(max_spacing, 110)

        start_x = (1000 - (num_cards - 1) * spacing - 100) // 2
        y = 30  # Fixed position at the top of the screen for computer cards

        for i, card in enumerate(self.hand):
            card.x = start_x + i * spacing
            card.y = y
            card.draw(surface)  # Draw each card on the screen
        hand_text = font.render("Cards in Hand : " + str(len(self.hand)), True, WHITE)
        surface.blit(hand_text, pos)

    def add_card(self, card,screen,clock,bg):
        if card:
            self.hand.append(card)
            card.y = 10
            if len(self.hand) == 0:
                card.x = 50
            else:
                card.x = 50 + (len(self.hand) * 110)





