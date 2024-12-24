import numpy as np
import json
from typing import Optional, Dict, Any
from enum import Enum
import time
import asyncio

from game_manager import EnhancedGameManager
from config import GAME_GENRES
from tictactoe import TicTacToe3D
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def get_player_move(game_type: str, board=None) -> dict:
    """Get and validate player move based on game type"""
    if game_type == "3D Tic Tac Toe":
        while True:
            try:
                print("\nEnter your move (x y z), each number from 0-2:")
                move = input("> ").strip().split()
                x, y, z = map(int, move)
                if 0 <= x <= 2 and 0 <= y <= 2 and 0 <= z <= 2:
                    return {"type": "move", "position": [x, y, z]}
                print("Invalid coordinates. Please use numbers 0-2.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter three numbers separated by spaces.")
                
    elif game_type == "Strategic Rock Paper Scissors":
        while True:
            choice = input("\nEnter your choice (rock/paper/scissors): ").lower().strip()
            if choice in ["rock", "paper", "scissors"]:
                return {"type": "move", "choice": choice}
            print("Invalid choice. Please choose rock, paper, or scissors.")

class DialogueResponse(Enum):
    CONTINUE = "continue"
    SKIP = "skip"
    REPEAT = "repeat"
    QUIT = "quit"

class DialogueInteractionHandler:
    def __init__(self, typing_speed: float = 0.03):
        self.typing_speed = typing_speed
        self.last_dialogue: Optional[str] = None
    
    async def print_with_typing_effect(self, text: str) -> None:
        """Print text with a typewriter effect."""
        for char in text:
            print(char, end='', flush=True)
            await asyncio.sleep(self.typing_speed)
        print()  # New line at the end
    
    def display_options(self) -> None:
        """Display the available interaction options."""
        print("\nOptions:")
        print("- Press ENTER to continue")
        print("- Type 'r' to repeat dialogue")
        print("- Type 's' to skip typing animation")
        print("- Type 'q' to quit")
        print("\nYour choice: ", end='', flush=True)
    
    async def handle_response(self, dialogue: Dict[str, Any]) -> DialogueResponse:
        """Handle displaying dialogue and getting user response."""
        try:
            self.last_dialogue = dialogue["dialogue"]["text"]
            
            # Print character name if available
            if "character_name" in dialogue:
                await self.print_with_typing_effect(f"\n{dialogue['character_name']}:")
            
            # Print the dialogue
            await self.print_with_typing_effect(self.last_dialogue)
            
            # If there's an emotion/tone, display it
            if "tone" in dialogue["dialogue"]:
                print(f"[Tone: {dialogue['dialogue']['tone']}]")
            
            while True:
                self.display_options()
                user_input = input().lower().strip()
                
                if user_input == "":
                    return DialogueResponse.CONTINUE
                elif user_input == "r":
                    return DialogueResponse.REPEAT
                elif user_input == "s":
                    return DialogueResponse.SKIP
                elif user_input == "q":
                    return DialogueResponse.QUIT
                else:
                    print("\nInvalid input. Please try again.")
        
        except KeyboardInterrupt:
            print("\nInteraction interrupted by user.")
            return DialogueResponse.QUIT
        except Exception as e:
            logger.error("str{e}",exc_info=True)
            print(f"\nError during dialogue interaction: {e}")
            return DialogueResponse.QUIT

    async def wait_for_user(self, dialogue: Dict[str, Any]) -> DialogueResponse:
        """Main method to handle dialogue display and user interaction."""
        response = await self.handle_response(dialogue)
        
        while response == DialogueResponse.REPEAT:
            # Temporarily speed up typing for repeat
            original_speed = self.typing_speed
            self.typing_speed = self.typing_speed / 2
            response = await self.handle_response(dialogue)
            self.typing_speed = original_speed
        
        return response

async def process_dialogue_interaction(game_state: Dict[str, Any], dialogue: Dict[str, Any]) -> bool:
    """Process dialogue interaction and update game state accordingly."""
    handler = DialogueInteractionHandler()
    
    while True:
        response = await handler.wait_for_user(dialogue)
        
        if response == DialogueResponse.CONTINUE:
            return True
        elif response == DialogueResponse.SKIP:
            # Update game state to skip future animations
            game_state["preferences"]["skip_animations"] = True
            return True
        elif response == DialogueResponse.QUIT:
            # Perform any necessary cleanup
            print("\nExiting dialogue...")
            return False
        elif response == DialogueResponse.REPEAT:
            continue

async def main():
    """Enhanced main function with configuration support"""
    print("\n=== Welcome to the Multi-Agent Game System ===")
    
    # Display available genres
    print("\nAvailable Genres:")
    for i, genre in enumerate(GAME_GENRES.keys(), 1):
        print(f"{i}. {genre.title()}")
        print(f"   Themes: {', '.join(GAME_GENRES[genre]['themes'])}")
        
    # Get player preferences
    genre_choice = input("\nChoose a genre (number): ").strip()
    genres = list(GAME_GENRES.keys())
    genre = genres[int(genre_choice) - 1] if genre_choice.isdigit() and \
            0 < int(genre_choice) <= len(genres) else "fantasy"
            
    print("\nChoose your play style:")
    print("1. Strategic - Careful planning and thoughtful moves")
    print("2. Aggressive - Bold moves and high-risk plays")
    print("3. Defensive - Cautious play and counter-strategies")
    style_choice = input("> ").strip()
    style_map = {"1": "strategic", "2": "aggressive", "3": "defensive"}
    play_style = style_map.get(style_choice, "strategic")
    
    player_preferences = {
        "preferred_genre": genre,
        "play_style": play_style,
        "difficulty_preference": "adaptive"
    }
    
    # Initialize enhanced game manager
    game_manager = EnhancedGameManager()
    await game_manager.initialize_game(genre, player_preferences)
    print(game_manager.game_state.state['story']['opening_narrative'])
    time.sleep(10)
    # Enhanced game loop with better feedback
    level = 0
    while level < 3:
        print(f"\n=== Level {level + 1} ===")
        # print(game_manager.game_state.state)
        # print(f"Current Score: {game_manager.game_state.state['score']}")
        # print(f"Win Streak: {game_manager.game_state.state['current_streak']}")
        
        game_type = game_manager.game_state.state["current_game"]["type"]
        print(f"\nGame Type: {game_type}")
        
        # Get character introduction with enhanced dialogue
        intro_dialogue = await game_manager.current_character.generate_dialogue(
            "greeting",
            {
                "progress": game_manager.game_state.state,
                "previous_interaction": None
            }
        )
        intro_dialogue=json.loads(intro_dialogue)
        # print(intro_dialogue)
        should_continue = await process_dialogue_interaction(
            game_manager.game_state.state,
            {"dialogue":{"text":intro_dialogue['dialogue_text'],"tone":intro_dialogue['tone']}}
        )
        
        if not should_continue:
            return {
                "status": "quit",
                "game_state": game_manager.game_state.state
            }
        

        
        # Game-specific loop with enhanced feedback
        while True:
            if game_type == "3D Tic Tac Toe":
                game_manager.game_state.state["tictactoe_game"]=TicTacToe3D()
                game_manager.game_state.state["tictactoe_game"].print_board()
                
            # Get player move
            player_action = await get_player_move(game_type)
            
            # Process turn with enhanced feedback
            result = await game_manager.process_turn(player_action)
            # should_continue = await process_dialogue_interaction(
            #     game_manager.game_state.state,
            #     json.loads(result['dialogue'])
            # )
            
            # if not should_continue:
            #     return {
            #         "status": "quit",
            #         "game_state": game_manager.game_state.state
            #     }
            # print(f"\nCharacter: {result['dialogue']}")
            if result['hint']:
                print(f"Hint: {result['hint']}")
                
            # Show score updates
            # if 'state_update' in result:
                # print(f"\nScore: {result['state_update']['score']}")
                # print(f"Streak: {result['state_update']['streak']}")
                
            if result['game_result']['status'] in ['win', 'lose', 'draw']:
                if result['game_result']['status'] == 'win':
                    victory_dialogue = await game_manager.current_character.generate_dialogue(
                        "victory",
                        {"result": "win", "strategy": player_action}
                    )
                    # print(f"\nCharacter: {victory_dialogue}")
                    victory_dialogue=json.loads(victory_dialogue)
                    should_continue = await process_dialogue_interaction(
                        game_manager.game_state.state,
                        {"dialogue":{"text":victory_dialogue['dialogue_text']}}
                    )
                    
                    if not should_continue:
                        return {
                            "status": "quit",
                            "game_state": game_manager.game_state.state
                        }
                    level += 1
                elif result['game_result']['status'] == 'lose':
                    defeat_dialogue = await game_manager.current_character.generate_dialogue(
                        "defeat",
                        {"result": "lose", "strategy": player_action}
                    )
                    # print(f"\nCharacter: {defeat_dialogue}")
                    defeat_dialogue=json.loads(defeat_dialogue)
                    should_continue = await process_dialogue_interaction(
                        game_manager.game_state.state,
                        {"dialogue":{"text":defeat_dialogue['dialogue_text']}}
                    )
                    
                    if not should_continue:
                        return {
                            "status": "quit",
                            "game_state": game_manager.game_state.state
                        }
                    
                break
                
            await asyncio.sleep(1)
            
    print("\n=== Game Complete ===")
    print(f"Final Score: {game_manager.game_state.state['score']}")
    print(f"Games Played: {game_manager.game_state.state['games_played']}")
    print("Thank you for playing!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        logger.error(f"error: {str(e)}",exc_info=True)
        print(f"\nAn error occurred: {e}")