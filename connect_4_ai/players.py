import random
import time
import pygame
import math
from connect4 import connect4

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class humantxt(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human(connect4Player):
	
	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					# Clearing Previous Draw
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE + 100))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2 + 100)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2 + 100)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	ROW_COUNT = 6
	COLUMN_COUNT = 7
	WINDOW_SIZE = 4

	# Set move value as a move list
	def play(self, env: connect4, move: list) -> None:
		col, minmax_val = self.minimax(env, 5, True)
		move[:] = [col]

	def minimax(self, env, depth, maxPlayer):
		if self.is_winner(env.board, self.position):
			return (None, 1000000000)
		elif self.is_winner(env.board, self.opponent.position):
			return (None, -1000000000)
		elif self.draw(env):
			return (None, 0)
		
		if depth == 0 :
			return (None, self.get_score(env.board, self.position))
		
		if maxPlayer:
			value = -math.inf
			best_col = 0
			n=0
			for col in [i for i, p in enumerate(env.topPosition >= 0) if p]:
				n+=1
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, self.position)
				
				new_score = self.minimax(temp_env, depth - 1, False)[1]
				print(temp_env.board)
				print("max depth: ", depth, " #: ", n, " score: ", new_score)
				print("max New Score: ", new_score, " value: ", value)
				if new_score > value:
					value = new_score
					best_col = col

			return best_col, value
		else:
			value = math.inf
			best_col = 0
			n=0
			for col in [i for i, p in enumerate(env.topPosition >= 0) if p]:
				n+=1
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, self.opponent.position)
				
				new_score = self.minimax(temp_env, depth - 1, True)[1]
				print(temp_env.board)
				print("min depth: ", depth, " #: ", n, " score: ", new_score)
				print("min New Score: ", new_score, " value: ", value)
				if new_score < value:
					value = new_score
					best_col = col

			return best_col, value
		
	def simulate_move(self, env, row, col, player):
		env.board[row][col] = player
		env.topPosition[col] -= 1
		env.history[0].append(col)

	def get_section(self, board):
		sections = []
		
		for r in range(self.ROW_COUNT):
			row_array = [int(i) for i in list(board[r, :])]
			for c in range(self.COLUMN_COUNT - 3):
				window = row_array[c:c + self.WINDOW_SIZE]
				sections.append(window)
		
		for c in range(self.COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:, c])]
			for r in range(self.ROW_COUNT - 3):
				window = col_array[r:r + self.WINDOW_SIZE]
				sections.append(window)
		
		# Diagonal up
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				window = [board[r + i][c + i] for i in range(self.WINDOW_SIZE)]
				sections.append(window)

		# Diagonal down
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_SIZE)]
				sections.append(window)
		
		print("sections nums: ", len(sections))
		return sections

	def get_score(self, board, player):
		score = 0
		sections = self.get_section(board)
		for section in sections:
			score += self.evaluate_window(section, player)

		center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
		center_count = center_array.count(player)
		score += center_count * 3

		return score
	
	def evaluate_window(self, window, player):
		score = 0
		if window.count(player) == 4:
			score += 100
		elif window.count(player) == 3 and window.count(0) == 1:
			score += 5
		elif window.count(player) == 2 and window.count(0) == 2:
			score += 2
		# elif window.count(player) == 1 and window.count(0) == 3:
		# 	score += 1
		
		if window.count(self.opponent) == 3 and window.count(0) == 1:
			score -= 4

		return score
	
	def is_winner(self, board, player):
		#Check if player wins
		sections = self.get_section(board)
		for section in sections:
			if section.count(player) == 4:
				return True
			
		return False
	
	def draw(self, env):
		# if the board is full == draw
		if len(env.history[0]) + len(env.history[1]) == self.ROW_COUNT * self.COLUMN_COUNT:
			return True
		return False

class alphaBetaAI(connect4Player):
	ROW_COUNT = 6
	COLUMN_COUNT = 7
	WINDOW_SIZE = 4

	# Using caches to store the score of the board
	score_cache = {}
	
	def get_board_key(self, board):
		return tuple(map(tuple, board))
	
	def play(self, env: connect4, move: list) -> None:
		col, minmax_val = self.minimax(env, 5, -math.inf, math.inf, True)
		move[:] = [col]

	def minimax(self, env, depth, alpha, beta, maxPlayer):
		if self.is_winner(env.board, self.position):
			return (None, 1000000000)
		elif self.is_winner(env.board, self.opponent.position):
			return (None, -1000000000)
		elif self.draw(env):
			return (None, 0)
		
		if depth == 0:
			return (None, self.get_score(env.board, self.position))
		
		best_col = None
		if maxPlayer:
			value = -math.inf
			for col in [i for i, p in enumerate(env.topPosition >= 0) if p]:
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, self.position)
				new_score = self.minimax(temp_env, depth - 1, alpha, beta, False)[1]
				if new_score > value:
					value = new_score
					best_col = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return best_col, value
		else:
			value = math.inf
			for col in [i for i, p in enumerate(env.topPosition >= 0) if p]:
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, self.opponent.position)
				new_score = self.minimax(temp_env, depth - 1, alpha, beta, True)[1]
				if new_score < value:
					value = new_score
					best_col = col
				beta = min(beta, value)
				if alpha >= beta:
					break
			return best_col, value

	def simulate_move(self, env, row, col, player):
		env.board[row][col] = player
		env.topPosition[col] -= 1
		env.history[0].append(col)

	def get_section(self, board):
		sections = []
		
		for r in range(self.ROW_COUNT):
			row_array = [int(i) for i in list(board[r, :])]
			for c in range(self.COLUMN_COUNT - 3):
				window = row_array[c:c + self.WINDOW_SIZE]
				sections.append(window)
		
		for c in range(self.COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:, c])]
			for r in range(self.ROW_COUNT - 3):
				window = col_array[r:r + self.WINDOW_SIZE]
				sections.append(window)
		
		# Diagonal up
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				window = [board[r + i][c + i] for i in range(self.WINDOW_SIZE)]
				sections.append(window)

		# Diagonal down
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_SIZE)]
				sections.append(window)
		
		return sections

	def get_score(self, board, player):
		key = self.get_board_key(board)
		if key in self.score_cache:
			return self.score_cache[key]
		
		score = 0
		sections = self.get_section(board)
		for section in sections:
			score += self.evaluate_window(section, player)

		center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
		center_count = center_array.count(player)
		score += center_count * 3

		self.score_cache[key] = score
		return score
	
	def evaluate_window(self, window, player):
		score = 0
		if window.count(player) == 4:
			score += 100
		elif window.count(player) == 3 and window.count(0) == 1:
			score += 5
		elif window.count(player) == 2 and window.count(0) == 2:
			score += 2
		# elif window.count(player) == 1 and window.count(0) == 3:
		# 	score += 1
		
		if window.count(self.opponent) == 3 and window.count(0) == 1:
			score -= 4

		return score

	def is_winner(self, board, player):
		sections = self.get_section(board)
		for section in sections:
			if section.count(player) == 4:
				return True
		return False

	def draw(self, env):
		return len(env.history[0]) + len(env.history[1]) == self.ROW_COUNT * self.COLUMN_COUNT


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE + 100

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




