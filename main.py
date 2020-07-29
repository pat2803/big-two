import pygame
import random


from test_hand import test_hand


class Hand:

    player_names = []

    def __init__(self, card_list, pos, separation=20, player=False, playing_hand=True, show_outline=True, name=""):
        self.card_list = card_list
        self.pos = pos
        self.separation = separation
        self.player = player
        self.playing_hand = False
        self.show_outline = show_outline
        self.playing_hand = playing_hand
        self.name = name

        # self.play_hand_time = 0
        # self.play_hand_bool = False

        self.select_card = []
        self.selected_cards = []
        self.skip_list = []

        self.lift = 20  # The amount each card is lifted when it is being selected by the player

        self.sorted_card_list = []

        self.pass_round = False  # Whether the player has passed the round

        self.my_turn = False  # Whether it is currently the player's turn

        # The outline of the box around the player's hand
        self.outline_colour = (255, 255, 255) if player else (255, 150, 150)

        self.score = 0  # The player's score

        # Give each player a string name that can be used for visuals
        if self.playing_hand:
            self.str_name = 'Player '+str(len(Hand.player_names)+1) if not self.name else self.name
            Hand.player_names.append(self.str_name)

    def convert_hand(self):
        pass

    # def play(self, play_hand):
    #     iterations = 20
    #     self.play_hand_bool = True
    #
    #     for index in play_hand:
    #         pos1 = (self.pos[0]+self.card_list.index(play_hand[index])*self.separation, self.pos[1])
    #         pos_now = move_cards(pos1, play_pos, self.play_hand_time, iterations)
    #     self.play_hand_time += 1
    #
    #     if self.play_hand_time >= iterations:
    #         self.play_hand_time = 0
    #         # Remove the cards from the hand

    def show_cards(self):

        # Draw outline around player's hand

        # current_outline = self.outline_colour if
        if self.show_outline:
            if self.my_turn:
                current_outline = (100, 255, 100)
            elif self.pass_round:
                current_outline = (100, 100, 100)
            else:
                current_outline = self.outline_colour
            pygame.draw.rect(win, current_outline, (self.pos[0]-buffer, self.pos[1]-buffer,
                                                        2*buffer+self.separation*12+card_width*SCALE,
                                                        2*buffer+card_height*SCALE), 5)

        # Draw outline around the selected cards
        for card in self.selected_cards:
            if card not in self.skip_list:
                pygame.draw.rect(win, (50, 100, 200, 0.1),
                                 (self.pos[0] + self.separation*self.card_list.index(card), self.pos[1] - self.lift,
                                  card_width*SCALE,
                                  card_height*SCALE), 5)

        select_list = [card_sprites[x] for x in self.select_card+self.selected_cards]
        skip_list = [card_sprites[x] for x in self.skip_list]

        if self.player:
            show_cards_sprites = [card_sprites[x] for x in self.card_list]
        else:
            show_cards_sprites = [card_back]*len(self.card_list)

        display_cards(show_cards_sprites, self.pos, skip_list=skip_list,
                      select_list=select_list, separation=self.separation)


# ---------------------------------------------------------------------------------------------------------------------


# Function to show the cards on the screen
# Parameters: card_list (list, of sprites), pos (tuple, (x, y)), separation (int)
def display_cards(card_list, pos, skip_list=[], select_list=[], separation=20, lift=20):
    for card in range(len(card_list)):
        if card_list[card] in skip_list:
            continue
        # Blits each card, left to right, at a specified separation
        elif card_list[card] in select_list:
            win.blit(card_list[card], (pos[0]+card*separation, pos[1]-lift))
        else:
            win.blit(card_list[card], (pos[0]+card*separation, pos[1]))


# Returns new position from movement from one spot to another
def move_cards(pos1, pos2, time, iterations):
    speed_x = (pos2[0] - pos1[0]) / iterations
    speed_y = (pos2[1] - pos1[1]) / iterations
    return pos1[0]+time*speed_x, pos1[1]+time*speed_y


# Define redraw function
def redraw_window():

    # Display players hands
    for player in players:
        player.show_cards()

    deck.show_cards()
    played_pile.show_cards()

    pygame.display.update()
    clock.tick(FRAMERATE)


# ---------------------------------------------------------------------------------------------------------------------


# Constants
WINWIDTH = 1200
WINHEIGHT = 600
CAPTION = 'Card Games'
ICON = 0
FRAMERATE = 60
SCALE = 0.5

# Variables
card_width = 140
card_height = 190
play_pos = (WINWIDTH/2 - card_width * SCALE * 2, WINHEIGHT/2 - card_width * SCALE * 0.5)
buffer = 10

run = True  # Variable to keep main game loop running
frame = 0  # Keeps track of which frame; can be used for animations
turn = -1  # Keeps track of which turn it is; -1 is dealing cards
player_num = 0  # Player number for dealing out cards
deal_card_pos_count = 0  # Animation count for animation of card dealing in progress
deal_hand_animation_steps = 10  # Total animation steps for dealing cards
first_round = True  # Whether it is the first round or not (check if 3 of diamonds must be played)
mouse_left_count = 0
mouse_left_limit = FRAMERATE/6  # Limits the possible frequency of mouse presses (prevents accidental double clicking)
key_press_count = 0
key_press_limit = FRAMERATE/4  # Limits the possible frequency of key presses
previous_hand = []  # Stores the previous hand played in the round
# previous_player = 0  # Stores the index of the last player to play some cards (used to determine who starts next round
wrong_hand = ""  # Stores the wrong hand message
wrong_hand_text_count = 0
wrong_hand_text_limit = FRAMERATE * 2  # Controls how long the wrong hand message stays on screen
play_card_animation_steps = 15  # Total animation steps for playing cards to the center
play_card_pos_count = 0
cards_played = False  # Whether cards are currently being played now
game_winner = -1

# Load images
background = pygame.image.load("background.png")  # Colour = (30, 125, 50)
card_back = pygame.image.load("Cards/cardBack_red2.png")
card_back = pygame.transform.rotozoom(card_back, 0, SCALE)
card_sprites = []
for number in [str(x+2) for x in range(9)] + ['J', 'Q', 'K', 'A']:
    for suit in ['Diamonds', 'Clubs', 'Hearts', 'Spades']:
        card_sprite = pygame.image.load(f'Cards/card{suit}{number}.png')
        card_sprite = pygame.transform.rotozoom(card_sprite, 0, SCALE)
        card_sprites.append(card_sprite)

# Initiate pygame
pygame.init()
win = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('calibri', 24)


# ---------------------------------------------------------------------------------------------------------------------


# Create deck to draw from
deck_indices = list(range(52))
random.shuffle(deck_indices)
deck = Hand(deck_indices, (50, 50), separation=0.25, show_outline=False, playing_hand=False)

# Create playing area
played_pile = Hand([], play_pos, 30, player=True, show_outline=False, playing_hand=False)

# Initiate player instances of Hand class
player_1 = Hand([], (450, 490), player=True)
player_2 = Hand([], (850, 250), player=True)
player_3 = Hand([], (450, 20), player=True)
player_4 = Hand([], (20, 250), player=True)
players = (player_1, player_2, player_3, player_4)


# ---------------------------------------------------------------------------------------------------------------------


# Main game loop
while run:

    # Pygame quit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Iterate frame count
    frame += 1

    # Blit background underneath other sprites
    win.blit(background, (0, 0))

    # Dealing hands
    # -----------------------------------------------------------------------------------------------------------------

    # Deal cards, then make turn = 0
    if turn == -1:
        # Set current card position based on initial position at deck to final position at end of player's hand
        card_pos = move_cards(deck.pos,
                              (players[player_num].pos[0]+len(players[player_num].card_list)*players[player_num].separation,
                               players[player_num].pos[1]), deal_card_pos_count, deal_hand_animation_steps)
        # Display the cards and iterate deal_card_pos_count
        display_cards([card_back], card_pos)
        deal_card_pos_count += 1
        # Deal to next player once animation stops and add the card to player's hand
        if deal_card_pos_count > deal_hand_animation_steps:
            players[player_num].card_list.append(deck.card_list.pop(0))
            deal_card_pos_count = 0
            player_num = player_num + 1 if player_num < 3 else 0

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for player in players:
                while len(player.card_list) < 13:
                    player.card_list.append(deck.card_list.pop(0))

        # Turn = 1 after deck is empty
        if len(deck.card_list) == 0:
            turn = 0
            for player in players:
                if 4 in player.card_list:
                    turn = players.index(player)

    # Playing rounds
    # -----------------------------------------------------------------------------------------------------------------

    # Turns between 0 and 3 are each players' turns
    if 0 <= turn <= 3:
        pnow = players[turn]  # pnow is the current player (shortened to prevent headache)
        pnow.my_turn = True

        # If it is a human player and they haven't played cards yet
        if pnow.player and not cards_played:
            # Get current mouse x, y nd if mouse pressed
            mouse = pygame.mouse.get_pos()
            mouse_left = pygame.mouse.get_pressed()[0]
            # If mouse over the last card (since it has larger hitbox)
            if pnow.pos[0] + pnow.separation*(len(pnow.card_list)-1) <= mouse[0] <=\
                    pnow.pos[0] + pnow.separation*(len(pnow.card_list)-1) + card_width * SCALE and\
                    pnow.pos[1] <= mouse[1] <= pnow.pos[1] + card_height * SCALE:
                pnow.select_card = [pnow.card_list[-1]]
                # If mouse pressed, remove or add card to the selected cards list of current player
                if mouse_left and mouse_left_count <= 0:
                    mouse_left_count = mouse_left_limit
                    if pnow.card_list[-1] in pnow.selected_cards:
                        pnow.selected_cards.remove(pnow.card_list[-1])
                    else:
                        pnow.selected_cards.append(pnow.card_list[-1])
            # If mouse over all but last card
            elif pnow.pos[0] <= mouse[0] <= pnow.pos[0] + pnow.separation * (len(pnow.card_list) - 1) and \
                    pnow.pos[1] <= mouse[1] <= pnow.pos[1] + card_height * SCALE:
                pnow.select_card = [pnow.card_list[(mouse[0]-pnow.pos[0])//pnow.separation]]
                # If mouse pressed, remove or add card to the selected cards list of current player
                if mouse_left and mouse_left_count <= 0:
                    mouse_left_count = mouse_left_limit
                    if pnow.card_list[(mouse[0]-pnow.pos[0])//pnow.separation] in pnow.selected_cards:
                        pnow.selected_cards.remove(pnow.card_list[(mouse[0]-pnow.pos[0])//pnow.separation])
                    else:
                        pnow.selected_cards.append(pnow.card_list[(mouse[0]-pnow.pos[0])//pnow.separation])
            else:
                pnow.select_card = []  # Select card should be empty if no non-selected card is being moused over

            # If enter is pressed try to play the current selected cards
            # ADD A PLAY HAND BUTTON TO PLAY THESE CARDS
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN] and key_press_count <= 0:
                key_press_count = key_press_limit
                play_this_hand = test_hand(pnow.selected_cards, previous_hand)
                if 4 not in pnow.selected_cards and first_round:
                    wrong_hand = "You must play the 3 of diamonds"
                    wrong_hand_text_count = wrong_hand_text_limit
                elif type(play_this_hand) == str:
                    wrong_hand = play_this_hand
                    wrong_hand_text_count = wrong_hand_text_limit
                    pnow.selected_cards = []
                else:
                    pnow.skip_list = pnow.selected_cards
                    cards_played = True

            # Press 'p' to pass the round
            if pressed[pygame.K_p] and key_press_count <= 0:
                key_press_count = key_press_limit
                # Round can't be passed if you are starting the round
                if not previous_hand:
                    wrong_hand = "You can't pass on the first hand"
                    wrong_hand_text_count = wrong_hand_text_limit
                else:
                    pnow.pass_round = True
                    pnow.selected_cards = []
                    pnow.select_card = []

            if pressed[pygame.K_s] and key_press_count <= 0:
                key_press_count = key_press_limit
                pnow.card_list = sorted(pnow.card_list)

        # If it is a bot and they haven't played cards yet
        elif not (pnow.player or cards_played):
            pass

        # If cards are being played
        if cards_played:
            # Animate each selected card moving to the play pile
            for card in pnow.selected_cards:
                current_pos = move_cards((pnow.card_list.index(card) * pnow.separation + pnow.pos[0], pnow.pos[1]),
                                         play_pos, play_card_pos_count, play_card_animation_steps)
                current_card_sprite = card_sprites[card]
                display_cards([current_card_sprite], current_pos)
            play_card_pos_count += 1
            # If animation is done
            if play_card_pos_count >= play_card_animation_steps:
                # Set cards in the play pile and the previous hand to cards that were just played
                played_pile.card_list = sorted(pnow.selected_cards)
                previous_hand = played_pile.card_list
                # previous_player = turn
                # Remove played cards from players hand
                for card in pnow.selected_cards:
                    pnow.card_list.remove(card)
                # Set these card lists to empty
                pnow.selected_cards = []
                pnow.select_card = []
                pnow.skip_cards = []
                # Set players turn bool to false
                pnow.my_turn = False
                # Set first_round to False
                first_round = False
                # Reset variables for cards being played
                cards_played = False
                play_card_pos_count = 0
                # Rotate through each turn
                turn = turn + 1 if turn < 3 else 0

        if pnow.pass_round:
            pnow.my_turn = False
            turn = turn + 1 if turn < 3 else 0

        player_pass_list = [player.pass_round for player in players]
        if sum(player_pass_list) == 3:
            turn = player_pass_list.index(False)
            played_pile.card_list = []
            previous_hand = []
            for player in players:
                player.pass_round = False

        player_len_hand = [len(player.card_list) for player in players]
        if 0 in player_len_hand:
            game_winner = player_len_hand.index(0)
            played_pile.card_list = []
            turn = 4

    # -----------------------------------------------------------------------------------------------------------------

    if turn == 4:
        print(f'The winner is player {game_winner + 1}!')
        players[game_winner].score += 1
        win_message_count = FRAMERATE*5
        turn = 5

    # -----------------------------------------------------------------------------------------------------------------

    if turn == 5:
        large_font = pygame.font.SysFont('calibri', 48)
        win_message_font = large_font.render(f'The winner is {players[game_winner].str_name}!', True, (255, 255, 255))
        win.blit(win_message_font, (600-win_message_font.get_width()//2, 300-win_message_font.get_height()//2))
        win_message_count -= 1
        if win_message_count <= 0:
            run = False


    # Updating counters, showing messages, redrawing rest of window
    # -----------------------------------------------------------------------------------------------------------------

    # Print message from a wrong hand being played
    if wrong_hand and wrong_hand_text_count > 0:
        wrong_hand_font = my_font.render(wrong_hand, True, (255, 255, 255))
        win.blit(wrong_hand_font, (50, 500))

    if key_press_count > 0:
        key_press_count -= 1
    if mouse_left_count > 0:
        mouse_left_count -= 1
    if wrong_hand_text_count > 0:
        wrong_hand_text_count -= 1
    else:
        wrong_hand = ""

    redraw_window()

pygame.quit()
