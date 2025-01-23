import sys

import pygame
from classes.Deck import Deck
from classes.Player import Player, Computer

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Local Card Game")
clock = pygame.time.Clock()
CARD_WIDTH, CARD_HEIGHT = 100, 150

font = pygame.font.Font(None, 20)
pfont = pygame.font.Font(None, 25)

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 168, 82)
BLACK = (0,0,0)

# Load card images
SUITS = ["spades", "diamond", "club", "heart"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
card_constitutions = [{"suit": suit, "rank": rank} for suit in SUITS for rank in RANKS]
card_constitutions += [{"suit": "joker", "rank": "black"},{"suit": "joker", "rank": "red"}]

# getting car images
card_images = [pygame.image.load(f"cardImage/{constitution['suit']}/{constitution['rank']}.png") for constitution in card_constitutions]  # Replace with actual card images
card_back = pygame.image.load("cardImage/card_background.png")

#importing sounds
game_play_sound = pygame.mixer.Sound("sounds/507749__mrthenoronha__crazy-upbeat-theme-loop.wav")
error = pygame.mixer.Sound("sounds/error.wav")
winning = pygame.mixer.Sound("sounds/winning.wav")
losing = pygame.mixer.Sound("sounds/losing.wav")
card_sound= pygame.mixer.Sound("sounds/cardmovement.mp3")
error.set_volume(1.0)


def display(turn):
    if turn == 0:
        text = "Your turn"
        turn_pos = (30, 600)
    else:
        text = "Computer's turn"
        turn_pos = (30, 50)
    turn_text = font.render(text, True, WHITE)
    screen.blit(turn_text, turn_pos)

def reset_game():
    global deck, player, computer, used_cards, center_card, turn, running,computer_waiting,player_play_time,computer_wait_time,wait_start_time
    computer_wait_time = 1000
    player_play_time = 0
    computer_waiting = False
    wait_start_time = 0

    # Initialize game elements
    deck = Deck(card_images, card_back,card_constitutions)
    player = Player()
    computer = Computer()
    used_cards = []

    # Deal initial cards to player and computer
    screen.fill(GREEN)
    for _ in range(5):
        player.add_card(deck.deal_card(used_cards),screen,clock,GREEN)
    for _ in range(5):
        computer.add_card(deck.deal_card(used_cards),screen,clock,GREEN)


    center_card = deck.deal_card(used_cards)
    center_card.x , center_card.y =WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2
    center_card.flip()



    start_pick = player.special_card(center_card)
    if start_pick:
        for _ in range(start_pick):
            player.add_card(deck.deal_card(used_cards), screen, clock, GREEN)
        turn = 1
    else:
        turn = 0

def draw_winner_popup(screen, winner):
    global is_playing
    extra = 0
    play_again_btn = pygame.image.load("cardImage/play-again-button.png")
    play_again_btn = pygame.transform.scale(play_again_btn, (200, 60))
    if winner=="Computer":
        img = pygame.image.load("cardImage/lose.png")
        sound = losing
    else:
        img = pygame.image.load("cardImage/winnerScreen-removebg-preview.png")
        sound = winning
        extra= 100
    img = pygame.transform.scale(img,(500,400))
    fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha = 0  # Start with complete transparency
    start_ticks = pygame.time.get_ticks()

    # Starting position for the transition (from left or top)
    start_x = -img.get_width()  # Image starts off-screen (from the left)
    start_y = HEIGHT // 4  # Vertical position where it will appear

    # Target position for the image (center of the screen)
    target_x = 150
    target_y = ((HEIGHT - img.get_height()) // 2 ) - 100

    button_width = 200
    button_height = 60
    button_x = (WIDTH - button_width) // 2  # Centering the button horizontally
    button_y = 400  # Vertical position of the button
    button_rect = pygame.Rect(button_x, button_y + extra, button_width, button_height)


    while alpha <= 255:
        sound.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button ==1:
                    print("Click detected")
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        is_playing= True
                        reset_game()
                        print("hello")
                        return


        # Clear the screen
        screen.fill((0,255,0))  # Background color or gameplay elements


        # Calculate how much the image has moved (smooth transition)
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        alpha = min(255, int(255 * (elapsed_time / 2)))

        # Smoothly transition the position of the image
        transition_factor = min(1, elapsed_time / 2)  # Factor that defines how far the image has moved
        current_x = start_x + (target_x - start_x) * transition_factor
        current_y = start_y + (target_y - start_y) * transition_factor

        # Apply the fade effect and draw the background box
        fade_surface.fill((0, 0, 0, alpha))  # Black overlay with variable alpha
        screen.blit(fade_surface, (0, 0))

        # Draw the rounded box with shadow

        # Draw the "You Win" image inside the box
        screen.blit(img, (current_x + 125, current_y + 30))
        if(alpha==255):
            screen.blit(play_again_btn,(button_rect.x,button_rect.y))


        pygame.display.flip()
        clock.tick(60)









reset_game()
# Main Game Loop
running = True
is_playing = True

while running:
    if is_playing:
        screen.fill(GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if turn == 0:
                        for card in player.hand:
                            if card.rect.collidepoint(mouse_pos) :
                                if player.play_card(card,center_card):
                                    player.hand.remove(card)
                                    used_cards.append(center_card)
                                    card.x = center_card.x
                                    card.y = center_card.y
                                    center_card = card
                                    card_sound.play()
                                    player_play_time = pygame.time.get_ticks()
                                    num = player.special_card(card)
                                    if num==None:
                                        turn = (turn + 1 )% 2
                                    else:
                                        for _ in range(num):
                                            computer.add_card(deck.deal_card(used_cards),screen,clock,GREEN)
                                else:
                                    error.play()
                                    print("Incorrect choice")
                        if deck.rect.collidepoint(mouse_pos):
                            player.add_card(deck.deal_card(used_cards),screen,clock,GREEN)
                            player_play_time = pygame.time.get_ticks()
                            card_sound.play()
                            turn = (turn + 1) % 2

        # draw the deck after shuffling
        mouse_pos = pygame.mouse.get_pos()

        if deck.is_empty():
            deck.refill(used_cards)
            used_cards = []

        display(turn)
        center_card.draw(screen)

        deck_text = pfont.render("Used Cards : " + str(len(used_cards)), True, WHITE)
        screen.blit(deck_text, (850, (650 // 2) + (150 // 2) + 10))


        if len(player.hand)==0 or len(computer.hand)==0:
            if len(player.hand) ==0:
                winner = "Player"
            else:
                winner = "Computer"
            is_playing = False
            draw_winner_popup(screen ,winner)
        else:
            if turn == 1 and pygame.time.get_ticks() - player_play_time >= computer_wait_time and not computer_waiting:
                choosen_card = computer.play_card(center_card)
                if choosen_card==None:
                    computer.add_card(deck.deal_card(used_cards), screen, clock, GREEN)
                    card_sound.play()
                    print("None")
                    turn = (turn + 1) % 2
                else:
                    print(choosen_card.suit, choosen_card.rank)
                    choosen_card.flip()
                    computer.hand.remove(choosen_card)
                    used_cards.append(center_card)
                    choosen_card.x = center_card.x
                    choosen_card.y = center_card.y
                    center_card = choosen_card
                    card_sound.play()
                    num = computer.special_card(choosen_card)
                    if num == None:
                        turn = (turn + 1) % 2
                    else:
                        computer_waiting = True
                        wait_start_time = pygame.time.get_ticks()
                        for _ in range(num):
                            player.add_card(deck.deal_card(used_cards), screen, clock, GREEN)

            if computer_waiting and pygame.time.get_ticks() - wait_start_time >= 1000:  # Wait for 1 second
                computer_waiting = False  # Stop waiting after the time has passed




        deck.draw_deck(screen)
        for card in used_cards:
            screen.blit(card.image,(850,center_card.y))

        computer.draw_hand(screen,(450,10))
        player.draw_hand(screen, (450, HEIGHT-20),mouse_pos)
        pygame.draw.rect(screen, BLACK, (850, 250, 100, 150), width=2)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
