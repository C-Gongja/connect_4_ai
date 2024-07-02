import argparse
from connect4 import connect4
from players import humantxt, stupidAI, randomAI, human, minimaxAI, alphaBetaAI
from montecarlo import monteCarloAI
import pygame
import sys

parser = argparse.ArgumentParser(description='Run programming assignment 1')
parser.add_argument('-w', default=6, type=int, help='Rows of game')
parser.add_argument('-l', default=7, type=int, help='Columns of game')
parser.add_argument('-p1', default='human', type=str, help='Player 1 agent. Use any of the following: [human, humanTxt, stupidAI, randomAI, monteCarloAI, minimaxAI, alphaBetaAI]')
parser.add_argument('-p2', default='human', type=str, help='Player 2 agent. Use any of the following: [human, humanTxt, stupidAI, randomAI, monteCarloAI, minimaxAI, alphaBetaAI]')
parser.add_argument('-seed', default=0, type=int, help='Seed for random algorithms')
parser.add_argument('-visualize', default='True', type=str, help='Use GUI')
parser.add_argument('-verbose', default='True', type=str, help='Print boards to shell')
parser.add_argument('-limit_players', default='1,2', type=str, help='Players to limit time for. List players as numbers eg [1,2]')
parser.add_argument('-time_limit', default='0.5,0.5', type=str, help='Time limits for each player. Must be list of 2 elements > 0. Not used if player is not listed')
parser.add_argument('-cvd_mode', default='False', type=str, help='Uses colorblind-friendly palette')

# Bools and argparse are not friends
bool_dict = {'True': True, 'False': False}

args = parser.parse_args()

w = args.w
l = args.l

seed = args.seed
visualize = bool_dict[args.visualize]
verbose = bool_dict[args.verbose]
limit_players = args.limit_players.split(',')
for i, v in enumerate(limit_players):
	limit_players[i] = int(v)
time_limit = args.time_limit.split(',')
for i, v in enumerate(time_limit):
	time_limit[i] = float(v)
cvd_mode = bool_dict[args.cvd_mode]

agents = {'human': human, 'humanTxt': humantxt, 'stupidAI': stupidAI, 'randomAI': randomAI, 'monteCarloAI': monteCarloAI, 'minimaxAI': minimaxAI, 'alphaBetaAI': alphaBetaAI}

# Constants and setup for Pygame
SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
P1COLOR = (255, 0, 0)
P2COLOR = (255, 255, 0)
WHITE = (255, 255, 255)

# Assume these are the dimensions of your board
ROW_COUNT = 6
COLUMN_COUNT = 7

RADIUS = int(SQUARESIZE / 2 - 5)

def popup(screen, message):
    # Set up the font and colors
    font = pygame.font.Font(None, 36)
    bg_color = (30, 30, 30)
    text_color = (255, 255, 255)
    button_color = (70, 70, 70)
    button_hover_color = (100, 100, 100)

    # Create a surface for the popup
    popup_width, popup_height = 300, 200
    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_surface.fill(bg_color)

    # Render the message
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(popup_width // 2, popup_height // 3))

    # Create buttons
    button_width, button_height = 100, 50
    yes_button_rect = pygame.Rect((popup_width // 4 - button_width // 2, popup_height * 2 // 3 - button_height // 2), (button_width, button_height))
    no_button_rect = pygame.Rect((popup_width * 3 // 4 - button_width // 2, popup_height * 2 // 3 - button_height // 2), (button_width, button_height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos  # Use event.pos for correct position
                    # Calculate actual position of the buttons on the screen !! This is important to get the correct position of the buttons and mouse click
                    popup_x = (screen.get_width() - popup_width) // 2
                    popup_y = 10
                    actual_yes_button_rect = yes_button_rect.move(popup_x, popup_y)
                    actual_no_button_rect = no_button_rect.move(popup_x, popup_y)
                    if actual_yes_button_rect.collidepoint(mouse_pos):
                        return True
                    elif actual_no_button_rect.collidepoint(mouse_pos):
                        return False

        # Update the popup
        popup_surface.fill(bg_color)
        popup_surface.blit(text_surface, text_rect)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = 10 
        actual_yes_button_rect = yes_button_rect.move(popup_x, popup_y)
        actual_no_button_rect = no_button_rect.move(popup_x, popup_y)
        yes_button_color = button_hover_color if actual_yes_button_rect.collidepoint(mouse_pos) else button_color
        no_button_color = button_hover_color if actual_no_button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(popup_surface, yes_button_color, yes_button_rect)
        pygame.draw.rect(popup_surface, no_button_color, no_button_rect)

        yes_text_surface = font.render("Yes", True, text_color)
        no_text_surface = font.render("No", True, text_color)
        popup_surface.blit(yes_text_surface, yes_text_surface.get_rect(center=yes_button_rect.center))
        popup_surface.blit(no_text_surface, no_text_surface.get_rect(center=no_button_rect.center))

        # Blit the popup to the main screen
        screen.blit(popup_surface, (popup_x, popup_y))
        pygame.display.flip()


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((800, 600))

	continue_game = True
	player1 = agents[args.p1](1, seed, cvd_mode)
	player2 = agents[args.p2](2, seed, cvd_mode)
	c4 = connect4(player1, player2, board_shape=(w, l), visualize=visualize, limit_players=limit_players, time_limit=time_limit, verbose=verbose, CVDMode=cvd_mode)

	while continue_game:
		print("Starting game")
		c4.play()

		continue_game = popup(screen, "Play again?")

		if continue_game:
			c4.reset()
		else:
			print("Exiting game.")

	pygame.quit()
	sys.exit()
