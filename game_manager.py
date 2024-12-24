import random

from llm_agent import StorytellerAgent, GameMasterAgent, AdvisorAgent, CharacterAgent
from tictactoe import TicTacToe3D
from number_pred import NumberPredictionGame

from config import GAME_GENRES, DEFAULT_GAME_STATE, PERFORMANCE_METRICS

class GameManager:
    """Coordinates all agents and manages game flow"""
    
    def __init__(self):
        self.storyteller = StorytellerAgent()
        self.game_master = GameMasterAgent()
        self.advisor = AdvisorAgent()
        self.current_character = None
        
    async def initialize_game(self, genre: str, player_preferences: dict):
        """Initialize game with player preferences"""
        # Generate story structure
        story = await self.storyteller.generate_story(genre, player_preferences)
        self.game_state.state.update({
            "genre":genre,
            "story": story,
            "current_level": 0,
            "player_profile": player_preferences,
            "progress": {"wins": 0, "losses": 0}
        })
        
        # Initialize first level
        print("\nStory generated! Beginning first level...")
        await self._setup_level(0)
        
    async def _setup_level(self, level_index: int):
        """Setup specific level with appropriate character and game"""
        level_info = self.game_state.state["story"]["levels"][level_index]

        print(f"\nSetting up Level {level_index + 1}: {level_info['name']}")
        
        character_profile = {
            "archetype": level_info.get("character", "mysterious challenger"),
            "traits": ["challenging", "engaging"],
            "style": "enigmatic"
        }
        # Create character agent for this level
        # character_profile = level_info["character"]
        self.current_character = CharacterAgent(character_profile, level_index, self.game_state.state['genre'])
        await self.current_character.initialize()

        
        # Select appropriate game
        game_config = await self.game_master.select_game(
            self.game_state.state["player_profile"],
            level_info
        )
        self.game_state.state["current_game"] = game_config['selected_game']
        
    async def play_turn(self, player_action: dict) -> dict:
        """Process a single turn of gameplay"""
        # Update game state with player action
        self.game_state.state["player_action"] = player_action
        
        # Generate character response
        
        
        # Check if player needs hint
        if self._should_provide_hint():
            hint = await self.advisor.generate_hint(
                self.game_state.state,
                self.game_state.state["current_game"]["difficulty"]
            )
        else:
            hint = None
            
        # Process game logic and get result
        game_result = self._process_game_logic(player_action)
        
        # Adjust difficulty if needed
        # if game_result["status"] in ["win", "lose"]:
        #     difficulty_adjustment = await self.game_master.adjust_difficulty({
        #         "result": game_result["status"],
        #         "difficulty": self.game_state.state["current_game"]["difficulty"]
        #     })
        #     self.game_state.state["current_game"]["difficulty"] = difficulty_adjustment["new_difficulty"]
            
        return {
            "hint": hint,
            "game_result": game_result,
            "game_state": self.game_state.state
        }
        
    def _should_provide_hint(self) -> bool:
        """Determine if player needs a hint"""
        recent_losses = sum(1 for result in self.game_state.state.get("recent_results", [])[-3:]
                          if result == "lose")
        return recent_losses >= 2
        
    def _process_game_logic(self, player_action: dict) -> dict:
        """Process game logic and return result"""
        
        game_type = self.game_state.state["current_game"]["type"]
        print(game_type)
        if game_type == "3D Tic Tac Toe":
            return self._process_tictactoe(player_action)
        elif game_type == "Strategic Rock Paper Scissors":
            return self._process_rps(player_action)
        else:
            return self._process_number_prediction(player_action)
            
    # def _process_tictactoe(self, action: dict) -> dict:
    #     """Process 3D Tic Tac Toe game logic
        
    #     3D Tic Tac Toe is played on a 3x3x3 cube. Players need to get three in a row
    #     in any direction (including diagonals across planes).
    #     """
    #     # Initialize the board if it doesn't exist
    #     if 'board' not in self.game_state:
    #         self.game_state['board'] = [[['' for _ in range(3)] for _ in range(3)] for _ in range(3)]
    #         self.game_state['current_player'] = 'X'  # Player is always X
            
    #     board = self.game_state['board']
    #     x, y, z = action['position']
        
    #     # Validate move
    #     if not (0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3):
    #         return {"status": "invalid", "message": "Position out of bounds"}
    #     if board[x][y][z] != '':
    #         return {"status": "invalid", "message": "Position already occupied"}
            
    #     # Make player's move
    #     board[x][y][z] = 'X'
        
    #     # Check for player win
    #     if self._check_3d_win(board, 'X'):
    #         self.game_state["progress"]["wins"] += 1
    #         return {"status": "win", "message": "Congratulations! You've won!"}
        
    #     # AI move
    #     ai_move = self._get_best_3d_move(board)
    #     if ai_move:
    #         ax, ay, az = ai_move
    #         board[ax][ay][az] = 'O'
            
    #         # Check for AI win
    #         if self._check_3d_win(board, 'O'):
    #             self.game_state["progress"]["losses"] += 1
    #             return {"status": "lose", "message": "The AI has won this round!"}
        
    #     # Check for draw
    #     if self._is_board_full(board):
    #         return {"status": "draw", "message": "It's a draw!"}
            
    #     return {"status": "continue", "message": "Your turn"}

    def _process_tictactoe(self, action: dict) -> dict:
        """Process 3D Tic Tac Toe game logic"""
        game = self.game_state.state.get("tictactoe_game")
        if not game:
            game = TicTacToe3D()
            self.game_state.state["tictactoe_game"] = game
            
        # Process player move
        x, y, z = action["position"]
        if not game.make_move(x, y, z, 1):
            return {"status": "invalid", "message": "Invalid move"}
            
        # AI move
        valid_moves = game.get_valid_moves()
        if valid_moves:
            ai_move = random.choice(valid_moves)
            game.make_move(ai_move[0], ai_move[1], ai_move[2], 2)
            
        # Check game state
        winner = game.check_win()
        if winner:
            return {
                "status": "win" if winner == 1 else "lose",
                "message": "Game Over",
                "board": game.board.tolist()
            }
        elif game.is_full():
            return {
                "status": "draw",
                "message": "Game Draw",
                "board": game.board.tolist()
            }
        else:
            return {
                "status": "continue",
                "message": "Game Continuing",
                "board": game.board.tolist()
            }

    # def _check_3d_win(self, board, player):
    #     """Check for win in 3D Tic Tac Toe"""
    #     # Check each 2D plane
    #     for i in range(3):
    #         # Check rows
    #         for j in range(3):
    #             if all(board[i][j][k] == player for k in range(3)) or \
    #             all(board[i][k][j] == player for k in range(3)) or \
    #             all(board[k][i][j] == player for k in range(3)):
    #                 return True
                    
    #         # Check diagonals in each plane
    #         if all(board[i][k][k] == player for k in range(3)) or \
    #         all(board[i][k][2-k] == player for k in range(3)) or \
    #         all(board[k][i][k] == player for k in range(3)) or \
    #         all(board[k][k][i] == player for k in range(3)):
    #             return True
        
    #     # Check main diagonals
    #     if all(board[k][k][k] == player for k in range(3)) or \
    #     all(board[k][k][2-k] == player for k in range(3)) or \
    #     all(board[k][2-k][k] == player for k in range(3)) or \
    #     all(board[2-k][k][k] == player for k in range(3)):
    #         return True
        
    #     return False

    # def _get_best_3d_move(self, board):
    #     """Get best move for AI in 3D Tic Tac Toe using simple heuristic"""
    #     # First, try to win
    #     for x in range(3):
    #         for y in range(3):
    #             for z in range(3):
    #                 if board[x][y][z] == '':
    #                     board[x][y][z] = 'O'
    #                     if self._check_3d_win(board, 'O'):
    #                         board[x][y][z] = ''
    #                         return (x, y, z)
    #                     board[x][y][z] = ''
        
    #     # Then, block player's win
    #     for x in range(3):
    #         for y in range(3):
    #             for z in range(3):
    #                 if board[x][y][z] == '':
    #                     board[x][y][z] = 'X'
    #                     if self._check_3d_win(board, 'X'):
    #                         board[x][y][z] = ''
    #                         return (x, y, z)
    #                     board[x][y][z] = ''
        
    #     # Otherwise, make a strategic move
    #     # Prioritize center and corners
    #     strategic_positions = [
    #         (1,1,1),  # center
    #         (0,0,0), (0,0,2), (0,2,0), (0,2,2),  # corners of first layer
    #         (2,0,0), (2,0,2), (2,2,0), (2,2,2),  # corners of last layer
    #     ]
        
    #     for pos in strategic_positions:
    #         if board[pos[0]][pos[1]][pos[2]] == '':
    #             return pos
                
    #     # If no strategic position is available, choose first empty spot
    #     for x in range(3):
    #         for y in range(3):
    #             for z in range(3):
    #                 if board[x][y][z] == '':
    #                     return (x, y, z)
        
    #     return None

    # def _is_board_full(self, board):
    #     """Check if the 3D board is full"""
    #     return all(board[x][y][z] != '' 
    #             for x in range(3) 
    #             for y in range(3) 
    #             for z in range(3))

    def _process_rps(self, action: dict) -> dict:
        """Process Strategic Rock Paper Scissors logic
        
        This version includes a "strategic" element where the AI adapts to player patterns
        """
        
        # Initialize game state if needed
        if 'rps_history' not in self.game_state.state:
            self.game_state.state['rps_history'] = []
            self.game_state.state['player_patterns'] = {'R': 0, 'P': 0, 'S': 0}
        
        # Validate player move
        print(action)
        player_move = action.get('choice', '').upper()[0]
        print("test",player_move)
        if player_move not in ['R', 'P', 'S']:
            return {"status": "invalid", "message": "Invalid move. Use R, P, or S"}
        
        # Update player patterns
        self.game_state.state['player_patterns'][player_move] += 1
        
        # AI move selection based on player patterns
        print("waiting for ai")
        ai_move = self._get_strategic_rps_move()

        print("character_played",ai_move)
        
        # Determine winner
        result = self._determine_rps_winner(player_move, ai_move)

        print(result['message'])
        
        # Update history
        self.game_state.state['rps_history'].append({
            'player': player_move,
            'ai': ai_move,
            'result': result['status']
        })
        
        if result['status'] == 'win':
            self.game_state.state["progress"]["wins"] += 1
        elif result['status'] == 'lose':
            self.game_state.state["progress"]["losses"] += 1
        
        return result

    def _get_strategic_rps_move(self):
        """Get AI move based on player patterns"""
        print(self.game_state.state['player_patterns'])
        patterns = self.game_state.state['player_patterns']
        total_moves = sum(patterns.values())
        print(total_moves)
        if total_moves < 3:
            # Initial random moves
            return random.choice(['R', 'P', 'S'])
        
        # Predict player's next move based on their most frequent choice
        likely_move = max(patterns, key=patterns.get)
        
        # Choose counter to predicted move
        counters = {'R': 'P', 'P': 'S', 'S': 'R'}
        print(counters[likely_move])
        return counters[likely_move]

    def _determine_rps_winner(self, player_move: str, ai_move: str) -> dict:
        """Determine winner of RPS round"""
        if player_move == ai_move:
            return {"status": "draw", "message": f"Both chose {player_move}. It's a draw!"}
        
        winning_moves = {'R': 'S', 'P': 'R', 'S': 'P'}
        if winning_moves[player_move] == ai_move:
            return {"status": "win", 
                    "message": f"You chose {player_move}, AI chose {ai_move}. You win!"}
        else:
            return {"status": "lose", 
                    "message": f"You chose {player_move}, AI chose {ai_move}. AI wins!"}

    # def _process_number_prediction(self, action: dict) -> dict:
    #     """Process Number Prediction game logic
        
    #     Players try to predict the next number in a sequence. The sequence becomes
    #     more complex at higher difficulty levels.
    #     """
    #     # Initialize game state if needed
    #     if 'sequence' not in self.game_state:
    #         difficulty = self.game_state["current_game"]["difficulty"]
    #         self.game_state['sequence'] = self._generate_sequence(difficulty)
    #         self.game_state['current_position'] = 3  # Show first 3 numbers
        
    #     # Get player's prediction
    #     player_prediction = action.get('prediction')
    #     if not isinstance(player_prediction, (int, float)):
    #         return {"status": "invalid", "message": "Please provide a numeric prediction"}
        
    #     # Get correct next number
    #     correct_number = self.game_state['sequence'][self.game_state['current_position']]
        
    #     # Calculate score based on how close the prediction was
    #     accuracy = abs(player_prediction - correct_number)
    #     tolerance = 2  # Adjust based on difficulty
        
    #     if accuracy == 0:
    #         result = {"status": "win", "message": "Perfect prediction!"}
    #         self.game_state["progress"]["wins"] += 1
    #     elif accuracy <= tolerance:
    #         result = {"status": "win", "message": f"Close enough! The number was {correct_number}"}
    #         self.game_state["progress"]["wins"] += 1
    #     else:
    #         result = {"status": "lose", "message": f"Not quite. The number was {correct_number}"}
    #         self.game_state["progress"]["losses"] += 1
        
    #     # Move to next position
    #     self.game_state['current_position'] += 1
        
    #     # Add current sequence snapshot to result
    #     visible_sequence = self.game_state['sequence'][:self.game_state['current_position']]
    #     result["current_sequence"] = visible_sequence
        
    #     return result

    # def _generate_sequence(self, difficulty: float) -> list:
    #     """Generate a number sequence based on difficulty level"""
    #     length = 10
    #     if difficulty < 2:
    #         # Simple arithmetic sequence
    #         start = random.randint(1, 10)
    #         step = random.randint(2, 5)
    #         return [start + i * step for i in range(length)]
    #     elif difficulty < 3:
    #         # Geometric sequence
    #         start = random.randint(1, 5)
    #         ratio = random.randint(2, 3)
    #         return [start * (ratio ** i) for i in range(length)]
    #     elif difficulty < 4:
    #         # Fibonacci-like sequence with random starting numbers
    #         sequence = [random.randint(1, 5), random.randint(5, 10)]
    #         for i in range(length - 2):
    #             sequence.append(sequence[-1] + sequence[-2])
    #         return sequence
    #     else:
    #         # Complex sequence (e.g., square numbers plus linear term)
    #         a = random.randint(1, 3)
    #         b = random.randint(1, 5)
    #         return [a * (i ** 2) + b * i for i in range(length)]

    def _process_number_prediction(self, action: dict) -> dict:
        """Process Number Prediction game logic"""
        game = self.game_state.state.get("number_game")
        if not game:
            difficulty = 2
            
            game = NumberPredictionGame(difficulty)
            self.game_state.state["number_game"] = game
            
        prediction = action["prediction"]
        success, message = game.check_prediction(prediction)
        
        return {
            "status": "win" if success else 
                     "lose" if game.attempts >= game.max_attempts else "continue",
            "message": message,
            "sequence": game.get_sequence_display(),
            "attempts_left": game.max_attempts - game.attempts
        }

class GameState:
    """Manages the current state of the game"""
    def __init__(self):
        self.state = DEFAULT_GAME_STATE.copy()
        self.performance_history = []
        
    def update_performance(self, result: str):
        """Update performance metrics"""
        self.performance_history.append(result)
        recent_games = self.performance_history[-PERFORMANCE_METRICS['performance_window']:]
        win_rate = sum(1 for x in recent_games if x == 'win') / len(recent_games)
        
        # Update state
        self.state['games_played'] += 1
        if result == 'win':
            self.state['current_streak'] += 1
            self.state['score'] += 100 * (self.state['current_streak'])
        else:
            self.state['current_streak'] = 0
            
        return win_rate

class EnhancedGameManager(GameManager):
    """Enhanced Game Manager with configuration support"""
    
    def __init__(self):
        super().__init__()
        self.game_state = GameState()
        
    async def initialize_game(self, genre: str, player_preferences: dict):
        """Initialize game with enhanced configuration"""
        if genre not in GAME_GENRES:
            genre = "fantasy"  # Default to fantasy if invalid genre
            
        genre_config = GAME_GENRES[genre]
        # Enhance player preferences with genre-specific elements
        enhanced_preferences = {
            **player_preferences,
            "genre_elements": genre_config["themes"],
            "character_preferences": genre_config["character_archetypes"]
        }
        
        await super().initialize_game(genre, enhanced_preferences)
        
    async def process_turn(self, player_action: dict) -> dict:
        """Process turn with enhanced feedback and state management"""
        result = await super().play_turn(player_action)
        
        # Update game state and check for difficulty adjustment
        # should_adjust, adjustment_type = self.game_state.should_adjust_difficulty()
        # if should_adjust:
        #     difficulty_adjustment = await self.game_master.adjust_difficulty({
        #         "result": result["game_result"]["status"],
        #         "difficulty": self.game_state.state["difficulty"],
        #         "adjustment_type": adjustment_type
        #     })
        #     self.game_state.state["difficulty"] = difficulty_adjustment["new_difficulty"]
            
        return {
            **result,
            "state_update": {
                "score": self.game_state.state["score"],
                "streak": self.game_state.state["current_streak"]
            }
        }