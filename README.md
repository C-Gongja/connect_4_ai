# :robot: Conncet 4 AI

## Part I: Evaluation Function
Please explicitly state your evaluation function for terminal nodes. Your report must cover the following:
An explicit mathematical function to find the evaluation function from a given board
A brief motivation for the evaluation function (a couple of sentences to one paragraph)
A worked example of a midgame board showing the evaluation function score

## Part II: Coding the Agent
You will implement two algorithms for this competition, one using minimax alone (2 pts), and the other using minimax with alpha-beta pruning (3 pts), code your algorithm to play the game. These must inherit from the ‘Connect4Player’ class. Include a sentence or two describing your alpha-beta pruning agent’s successor function (1 pt).

## Part III: Testing 
Evaluate your agent against the benchmark agents.
<YourAgent> vs StupidAI 5 times
<YourAgent> vs RandomAI 5 times
<YourAgent> vs MonteCarloAI 10 times
As player 1 AND as player 2, for a total of 40 games. Report your results in a table. For RandomAI and MonteCarloAI, set the seeds 1-5 and 1-10 respectively for reproducibility. Note that while RandomAI and StupidAI can be seen as “sanity checks” that your algorithm is working, MCAI is a much more competitive player, but certainly beatable. Winners of previous contests beat MCAI all 20 times. Each win earns 0.5 pts, every tie earns 0.25 pts, and losses gain no points.

## Important Functions & Calls
### Commandline Interface
Command | Description | Datatype | Example | Default|
--------|-------------|----------|---------|----------|
-p1 | Agent who will be acting as player 1. Name of agent eg minimaxAI | Stirng| -p1 minimaxAI, -p1 monteCarloAI | human |
-p2 | Agent who will be acting as player 2. Name of agent eg minimaxAI | String | -p1 minimaxAI, -p1 monteCarloAI | human |
-seed | Seed for AI’s with stochastic elements | int | -seed 0 | 0
-w | Rows of gamebaord | int | -w 6 | 6
-l | Columns of gameboard | int | -l 7 | 7
-visualize | Bool to use or not use GUI | bool | -visualize True\ -visualize False | True
-verbose | Sends move-by-move game history to shell | bool | -verbose True\ -verbose False | False
-limit_players | Which agents should have time limits. Useful if you want to play an AI but don’t want to have the same time limit. In the format “x,y” where x and y are players. Values that are not 1 or 2 can be used in place of 1 or 2 if the player should not be limited | Stirng | -limit_players 1,2\ -limit_players -1,2 (player 1 is not limited)\ -limit_players 1,-1(player 2 is not limited) | 1,2
-time_limit | Time limit for each player. No effect if a player is not limited. In the format “x,y” where x and y are floating point numbers. | Stirng | -time_limit 0.5,0.5 | 0.5,0.5
-cvd_mode | Swaps existing color scheme for colorblind- friendly palette | bool | -cvd_mode True/ -cvd_mode False | False

### Commands
$python main.py -p1 alphaBetaAI -p2 stupidAI -limit_players 1,2 -verbose True -seed 0\
$python main.py -p1 stupidAI -p2 alphaBetaAI -limit_players 1,2 -verbose True -seed 0\
$python main.py -p1 alphaBetaAI -p2 randomAI -limit_players 1,2 -verbose True -seed 0\
$python main.py -p1 randomAI -p2 alphaBetaAI -limit_players 1,2 -verbose True -seed 0\
$python main.py -p1 alphaBetaAI -p2 monteCarloAI -limit_players 1,2 -verbose True -seed 0\
$python main.py -p1 monteCarloAI -p2 alphaBetaAI -limit_players 1,2 verbose True -seed 0\

#### AI vs Player cmd
$python3 main.py -p1 human -p2 alphaBetaAI -limit_players 2 (do not set limit to human player)\ 


