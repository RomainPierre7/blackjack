import pygame
import time
import deck

# Settings
player_bankroll = 50
bet_min = 2
font_sys = "impact"

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((500, 1000))
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("BlackJack")
screen.fill((20, 100, 0))
pygame.display.update()

# Functions
def update_screen(commands):
    screen.fill((20, 100, 0))
    font = pygame.font.SysFont(font_sys, 50)
    text = font.render(f"Bankroll: ${player_bankroll}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    font = pygame.font.SysFont(font_sys, 75)
    text = font.render(f"Bet: ${player_bet}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, 10))
    font = pygame.font.SysFont(font_sys, 50)
    text = font.render(f"Minimal bet: ${bet_min}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width - len - 10, 10))
    text = font.render(f"Dealer's Hand: {dealer_hand.value()}", True, (255, 255, 255))
    screen.blit(text, (10, height * 0.1))
    text = font.render(f"Player's Hand: {player_hand.value()}", True, (255, 255, 255))
    screen.blit(text, (10, height * 0.4))
    for i, card in enumerate(dealer_hand.get_cards()):
        image = card.get_image()
        image = pygame.transform.scale(image, (int((image.get_width() / image.get_height()) * height * 0.2), int(height * 0.2)))
        screen.blit(image, (150 + i * (image.get_width() + 30),  height * 0.17))
    for i, card in enumerate(player_hand.get_cards()):
        image = card.get_image()
        image = pygame.transform.scale(image, (int((image.get_width() / image.get_height()) * height * 0.2), int(height * 0.2)))
        screen.blit(image, (150 + i * (image.get_width() + 30), height * 0.47))
    size = 50
    font = pygame.font.SysFont(font_sys, size)
    text = font.render(commands, True, (0, 0, 0))
    len = text.get_width()
    while len > width * 0.9:
        size -= 1
        font = pygame.font.SysFont(font_sys, size)
        text = font.render(commands, True, (0, 0, 0))
        len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.8))
    pygame.display.update()

def bet():
    global player_bankroll, player_bet
    betting = True
    while betting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player_bankroll > player_bet:
                        player_bet += 1
                if event.key == pygame.K_RIGHT:
                    if player_bankroll >= player_bet + 10:
                        player_bet += 10
                    else:
                        player_bet = player_bankroll
                if event.key == pygame.K_DOWN:
                    if player_bet > bet_min:
                        player_bet -= 1
                if event.key == pygame.K_LEFT:
                    if player_bet - 10 > bet_min:
                        player_bet -= 10
                    else:
                        player_bet = bet_min
                if event.key == pygame.K_RETURN:
                    if player_bet >= bet_min:
                        player_bankroll -= player_bet
                        betting = False
        update_screen("Use arrow keys to bet, press enter to confirm")
    

def deal():
    card = main_deck.draw_card()
    player_hand.add_card(card)
    update_screen("")
    time.sleep(1)
    card = main_deck.draw_card()
    dealer_hand.add_card(card)
    update_screen("")
    time.sleep(1)
    card = main_deck.draw_card()
    player_hand.add_card(card)
    update_screen("")
    time.sleep(1)

def player_turn():
    global player_bankroll, player_bet
    playing = True
    double = False
    new_card = False
    over_21 = False
    black_jack = False
    if player_hand.best_value() == 21:
        black_jack = True
    if player_bet > player_bankroll:
        double = True
    while playing:
        if player_hand.best_value() == 0:
            over_21 = True
        if player_hand.best_value() == 21:
            double = True
            new_card = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and not (double and new_card) and not over_21 and not black_jack:
                    card = main_deck.draw_card()
                    player_hand.add_card(card)
                    new_card = True
                if event.key == pygame.K_d and not double and not new_card and not over_21:
                    if player_bankroll >= player_bet:
                        player_bankroll -= player_bet
                        player_bet *= 2
                        double = True
                if event.key == pygame.K_RETURN:
                    playing = False
        if black_jack and not new_card and not double:
            update_screen("Black Jack! Press Enter to stand or D to double your bet")
        elif black_jack and not new_card and double:
            update_screen("Black Jack! Press Enter to stand")
        elif over_21:
            update_screen("You went over 21, press Enter to stand")
        elif double and not new_card:
            update_screen("Press C to get one more card, press Enter to stand")
        elif double and new_card:
            update_screen("Press Enter to stand")
        elif not double and not new_card:
            update_screen("Press D to double your bet (max one more card), C to get one more card, Enter to stand")
        elif not double and new_card:
            update_screen("Press C to get one more card, press Enter to stand")

def dealer_turn():
    dealer_hand_value = dealer_hand.best_value()
    while ((dealer_hand_value < 17) and (dealer_hand_value != 0)):
        card = main_deck.draw_card()
        dealer_hand.add_card(card)
        dealer_hand_value = dealer_hand.best_value()
        update_screen("")
        time.sleep(1)

def result_screen(text_to_display):
    screen.fill((20, 100, 0))
    font = pygame.font.SysFont(font_sys, 50)
    text = font.render(f"Dealer's Hand: {dealer_hand.value()}", True, (255, 255, 255))
    screen.blit(text, (10, height * 0.05))
    text = font.render(f"Player's Hand: {player_hand.value()}", True, (255, 255, 255))
    screen.blit(text, (10, height * 0.1))
    font = pygame.font.SysFont(font_sys, 200)
    text = font.render(text_to_display, True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.2))
    font = pygame.font.SysFont(font_sys, 100)
    text = font.render(f"Your bankroll is now ${player_bankroll}", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.5))
    font = pygame.font.SysFont(font_sys, 50)
    text = font.render(f"Press Enter to continue", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.8))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def result():
    global player_bankroll, player_bet
    dealer = dealer_hand.best_value()
    player = player_hand.best_value()
    if player == 0:
        result_screen("You busted!")
    elif dealer == 0:
        player_bankroll += player_bet * 2
        result_screen("Dealer busted!")
    elif dealer > player:
        result_screen("Dealer wins!")
    elif dealer < player:
        player_bankroll += player_bet * 2
        result_screen("You win!")
    else:
        player_bankroll += player_bet
        result_screen("Push!")

def game_over():
    screen.fill((20, 100, 0))
    font = pygame.font.SysFont(font_sys, 200)
    text = font.render(f"You are out of money !", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.2))
    font = pygame.font.SysFont(font_sys, 100)
    text = font.render(f"Press enter to quit", True, (255, 255, 255))
    len = text.get_width()
    screen.blit(text, (width // 2 - len // 2, height * 0.5))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                pygame.quit()
    exit()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    main_deck = deck.Deck()
    main_deck.build()
    main_deck.shuffle()
    player_hand = deck.Deck()
    dealer_hand = deck.Deck()
    player_bet = bet_min
    bet()
    deal()
    player_turn()
    dealer_turn()
    result()
    if player_bankroll < bet_min:
        game_over()
        break