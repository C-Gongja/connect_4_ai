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

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
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
		#col = self.get_best_move(env)
		col, minmax_val = self.minimax(env, 2, True)
		move[:] = [col]

	def minimax(self, env, depth, maxPlayer):
		switch = {1:2,2:1}
		player = self.position
		possible_col_indices = [i for i, p in enumerate(env.topPosition >= 0) if p]
		board = env.board
		is_terminal = self.is_terminal_node(board, possible_col_indices)
		if depth == 0 or is_terminal:
			#print("depth is 0")
			if is_terminal:
				if self.winning_move(board, player):
					return (None, 100000000000000)
				elif self.winning_move(board, switch[player]):
					return (None, -10000000000000)
				else: # draw
					return (None, 0)
			else: # Depth is zero
				return (None, self.score_position(board, player))

		if maxPlayer:
			value = -math.inf
			max_col = random.choice(possible_col_indices)
			for col in possible_col_indices:
				row = env.topPosition[col]
				#print("max board")
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, player) #player 2
				temp_board = temp_env.getBoard()
				#print(temp_board)
				new_score = self.minimax(temp_env, depth-1, False)[1] #first index
				if new_score > value:
					value = new_score
					max_col = col
			return max_col, value

		else: # min
			value = math.inf
			min_col = random.choice(possible_col_indices)
			for col in possible_col_indices:
				row = env.topPosition[col]
				#print("min board")
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, switch[player]) #player 1
				temp_board = temp_env.getBoard()
				#print(temp_board)
				new_score = self.minimax(temp_env, depth-1, True)[1]#first index
				if new_score < value:
					value = new_score
					min_col = col
			return min_col, value

	def is_terminal_node(self, board, valid_location):
		switch = {1:2,2:1}
		return self.winning_move(board, self.position) or self.winning_move(board, switch[self.position]) or len(valid_location) == 0
	
	def winning_move(self, board, piece):
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
					return True

	def get_best_move(self, env):
		temp_env = env.getEnv()
		player = self.position
		best_score = float('-inf')
		# get valid location
		possible_col_indices = [i for i, p in enumerate(temp_env.topPosition >= 0) if p]
		best_col = random.choice(possible_col_indices)
		
		for col in possible_col_indices:
			temp_env = env.getEnv()
			row = temp_env.topPosition[col]
			#print("col: ", col)
			#print("row: ", row)
			self.simulate_move(temp_env, row, col, player)
			#print("after simulation temp board")
			temp_board = temp_env.getBoard()
			#print(temp_board)
			score = self.score_position(temp_board, player)
			#print("score: ", score)
			if score > best_score:
				best_score = score
				best_col = col
				#print("best col: ", best_col)

		return best_col
	
	def simulate_move(self, env, row, col, player):
		#print("env.topPosition[col]: ", env.topPosition[col])
		env.board[row][col] = player
		#print("board[row][col]: ", env.board[row][col])
		env.topPosition[col] -= 1
		#print("top pos: ", env.topPosition)
		env.history[0].append(col)

	def score_position(self, board, player):
		score = 0

		# Score centre column
		center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
		center_count = center_array.count(player)
		#play around with
		score += center_count * 3
		
		# Score horizontal positions
		for r in range(self.ROW_COUNT):
			row_array = [int(i) for i in list(board[r, :])]
			for c in range(self.COLUMN_COUNT - 3):
				window = row_array[c:c + self.WINDOW_SIZE]
				score += self.evaluate_window(window, player)
		
		# Score vertical positions
		for c in range(self.COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:, c])]
			for r in range(self.ROW_COUNT - 3):
				# Create a vertical window of 4
				window = col_array[r:r + self.WINDOW_SIZE]
				score += self.evaluate_window(window, player)
		
		# Score positive diagonals
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				# Create a positive diagonal window of 4
				window = [board[r + i][c + i] for i in range(self.WINDOW_SIZE)]
				score += self.evaluate_window(window, player)

		# Score negative diagonals
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				# Create a negative diagonal window of 4
				window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_SIZE)]
				score += self.evaluate_window(window, player)
		
		return score
	
	def evaluate_window(self, window, player):
		score = 0
		switch = {1:2,2:1}
		opp_player = 1
		if player == self.position:
			opp_player = switch[self.position]

		if window.count(player) == 4:
			score += 100
		elif window.count(player) == 3 and window.count(0) == 1:
			score += 5
		elif window.count(player) == 2 and window.count(0) == 2:
			score += 2

		if window.count(opp_player) == 3 and window.count(0) == 1:
			score -= 4

		return score

class alphaBetaAI(connect4Player):
	ROW_COUNT = 6
	COLUMN_COUNT = 7
	WINDOW_SIZE = 4

	def play(self, env: connect4, move: list) -> None:
		col, _ = self.minimax(env, 2, -math.inf, math.inf, True)
		move[:] = [col]

	def minimax(self, env, depth, alpha, beta, maxPlayer):
		switch = {1: 2, 2: 1}
		player = self.position
		possible_col_indices = [i for i, p in enumerate(env.topPosition >= 0) if p]
		board = env.board

		is_terminal = self.is_terminal_node(board, possible_col_indices)
		if depth == 0 or is_terminal:
			if is_terminal:
				if self.winning_move(board, player):
					return (None, 100000000000000)
				elif self.winning_move(board, switch[player]):
					return (None, -10000000000000)
				else:  # draw
					return (None, 0)
			else:  # Depth is zero
				return (None, self.score_position(board, player))

		if maxPlayer:
			value = -math.inf
			best_col = random.choice(possible_col_indices)
			for col in possible_col_indices:
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, player)
				new_score = self.minimax(temp_env, depth - 1, alpha, beta, False)[1]
				if new_score > value:
					value = new_score
					best_col = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return best_col, value

		else:  # minPlayer
			value = math.inf
			best_col = random.choice(possible_col_indices)
			for col in possible_col_indices:
				row = env.topPosition[col]
				temp_env = env.getEnv()
				self.simulate_move(temp_env, row, col, switch[player])
				new_score = self.minimax(temp_env, depth - 1, alpha, beta, True)[1]
				if new_score < value:
					value = new_score
					best_col = col
				beta = min(beta, value)
				if alpha >= beta:
					break
			return best_col, value

	def is_terminal_node(self, board, valid_location):
		switch = {1:2,2:1}
		return self.winning_move(board, self.position) or self.winning_move(board, switch[self.position]) or len(valid_location) == 0
	
	def winning_move(self, board, piece):
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
					return True
	
	def simulate_move(self, env, row, col, player):
		#print("env.topPosition[col]: ", env.topPosition[col])
		env.board[row][col] = player
		#print("board[row][col]: ", env.board[row][col])
		env.topPosition[col] -= 1
		#print("top pos: ", env.topPosition)
		env.history[0].append(col)

	def score_position(self, board, player):
		score = 0

		# Score centre column
		center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
		center_count = center_array.count(player)
		# play around with
		score += center_count * 6
		
		# Score horizontal positions
		for r in range(self.ROW_COUNT):
			row_array = [int(i) for i in list(board[r, :])]
			for c in range(self.COLUMN_COUNT - 3):
				window = row_array[c:c + self.WINDOW_SIZE]
				score += self.evaluate_window(window, player)
		
		# Score vertical positions
		for c in range(self.COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:, c])]
			for r in range(self.ROW_COUNT - 3):
				# Create a vertical window of 4
				window = col_array[r:r + self.WINDOW_SIZE]
				score += self.evaluate_window(window, player)
		
		# Score positive diagonals
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				# Create a positive diagonal window of 4
				window = [board[r + i][c + i] for i in range(self.WINDOW_SIZE)]
				score += self.evaluate_window(window, player)

		# Score negative diagonals
		for r in range(self.ROW_COUNT - 3):
			for c in range(self.COLUMN_COUNT - 3):
				# Create a negative diagonal window of 4
				window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_SIZE)]
				score += self.evaluate_window(window, player)
		
		return score
	
	def evaluate_window(self, window, player):
		score = 0
		switch = {1:2,2:1}
		opp_player = 1
		if player == self.position:
			opp_player = switch[self.position]

		if window.count(player) == 4:
			score += 100
		elif window.count(player) == 3 and window.count(0) == 1:
			score += 5
		elif window.count(player) == 2 and window.count(0) == 2:
			score += 2

		if window.count(opp_player) == 3 and window.count(0) == 1:
			score -= 4

		return score


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
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




