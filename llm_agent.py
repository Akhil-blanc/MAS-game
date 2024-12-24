from agent_role import AgentRole
import json
from typing import Tuple
import google.generativeai as genai
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from prompts import (
    STORYTELLER_PROMPTS, CHARACTER_PROMPTS,
    GAME_MASTER_PROMPTS, ADVISOR_PROMPTS
)

from config import(
    model, GAME_CONFIGS, PERFORMANCE_METRICS, ERROR_MESSAGES,GAME_GENRES
)

class LLMAgent:
    """Base class for LLM-powered agents"""
    
    def __init__(self, role: AgentRole, personality: dict):
        self.role = role
        self.personality = personality
        self.conversation_history = []
        
    async def generate_response(self, prompt: str, context: dict = None) -> str:
        """Generate response using Gemini"""
        # Construct the full prompt with personality and context
        # logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        system_prompt = self._construct_system_prompt(context)
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        try:
            response = await model.generate_content_async(full_prompt,
                                                          generation_config=genai.GenerationConfig(
                                                                    response_mime_type="application/json",
                                                        ))
                                             
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response()
            
    def _construct_system_prompt(self, context: dict = None) -> str:
        """Construct system prompt based on role and context"""
        base_prompt = f"You are a {self.role.value} in an interactive game. "
        personality_prompt = f"Your personality traits are: {', '.join(self.personality['traits'])}. "
        style_prompt = f"Your communication style is {self.personality['style']}. "
        
        if context:
            context_prompt = f"\nCurrent context: {json.dumps(context)}"
        else:
            context_prompt = ""
            
        return base_prompt + personality_prompt + style_prompt + context_prompt
        
    def _get_fallback_response(self) -> str:
        """Provide fallback responses if LLM fails"""
        fallbacks = {
            AgentRole.STORYTELLER: "The story continues to unfold...",
            AgentRole.GAME_MASTER: "Your challenge awaits...",
            AgentRole.CHARACTER: "Let us proceed with the game...",
            AgentRole.ADVISOR: "Consider your next move carefully..."
        }
        return fallbacks.get(self.role, "Let's continue...")


        
    def should_adjust_difficulty(self) -> Tuple[bool, str]:
        """Check if difficulty should be adjusted"""
        if len(self.performance_history) < PERFORMANCE_METRICS['performance_window']:
            return False, "not_enough_data"
            
        win_rate = self.update_performance('dummy')  # Get current win rate
        if win_rate > PERFORMANCE_METRICS['win_rate_threshold']['increase_difficulty']:
            return True, "increase"
        elif win_rate < PERFORMANCE_METRICS['win_rate_threshold']['decrease_difficulty']:
            return True, "decrease"
        return False, "maintain"

class StorytellerAgent(LLMAgent):
    """Agent responsible for generating dynamic story and narrative"""
    
    def __init__(self):
        personality = {
            "traits": ["creative", "engaging", "adaptive"],
            "style": "narrative and descriptive"
        }
        super().__init__(AgentRole.STORYTELLER, personality)
        
    async def generate_story(self, genre: str, player_preferences: dict) -> dict:
        """Generate story using configured prompts"""
        genre_config = GAME_GENRES[genre]
        prompt = STORYTELLER_PROMPTS["story_generation"].format(
            genre=genre,
            preferences=json.dumps(player_preferences),
            style=genre_config["tone"]
        )
        
        try:
            response = await self.generate_response(prompt)
            story_structure = json.loads(response)
            return story_structure
        except Exception as e:
            print(e)
            print(response)
            print(ERROR_MESSAGES["story_generation_failed"])
            return self._get_fallback_story(genre)
            
    def _get_fallback_story(self, genre: str) -> dict:
        """Provide a basic story structure if LLM generation fails"""
        return {
            "genre": genre,
            "title": f"The {genre.title()} Challenge",
            "levels": [
                {"name": "Beginner's Trial", "difficulty": 1},
                {"name": "Expert's Challenge", "difficulty": 2},
                {"name": "Master's Test", "difficulty": 3}
            ]
        }
    
    async def generate_transition(self, current_level: int, next_level: int, 
                                outcome: str, progress: dict, challenger_profile: dict) -> str:
        """Generate level transition narrative"""
        prompt = STORYTELLER_PROMPTS["level_transition"].format(
            current_level=current_level,
            next_level=next_level,
            outcome=outcome,
            progress=json.dumps(progress),
            challenger_profile=json.dumps(challenger_profile)
        )
        
        return await self.generate_response(prompt)

class GameMasterAgent(LLMAgent):
    """Agent responsible for managing game mechanics and difficulty"""
    
    def __init__(self):
        personality = {
            "traits": ["strategic", "fair", "adaptive"],
            "style": "clear and instructive"
        }
        super().__init__(AgentRole.GAME_MASTER, personality)
    
    
    async def select_game(self, player_profile: dict, level_info: dict) -> dict:
        """Select game using configured prompts"""
        prompt = GAME_MASTER_PROMPTS["game_selection"].format(
            skill_level=player_profile.get("skill_level", "beginner"),
            performance=json.dumps(player_profile.get("performance", {})),
            style=player_profile.get("play_style", "balanced"),
            difficulty=level_info.get("difficulty", "medium"),
            theme=level_info.get("theme", "standard"),
            time_limit=level_info.get("time_limit", "none")
        )
        
        try:
            response = await self.generate_response(prompt)
            game_config = json.loads(response)
            # print(game_config)
            return self._apply_game_config(game_config)
        except Exception as e:
            logger.error(f"game selection: {str(e)}", exc_info=True)
            print(ERROR_MESSAGES["game_selection_failed"])
            return self._get_fallback_game()
            
    
        
    def _get_fallback_game(self) -> dict:
        """Provide fallback game configuration"""
        return {
            "game_type": "3D Tic Tac Toe",
            "difficulty": 2,
            "rules": "standard"
        }
    
    def _apply_game_config(self, game_config: dict) -> dict:
        """Apply configuration from GAME_CONFIGS"""
        game_type = game_config['selected_game']["type"]
        if game_type in GAME_CONFIGS:
            base_config = GAME_CONFIGS[game_type]
            # Merge configurations
            return {**base_config, **game_config}
        return game_config

class CharacterAgent(LLMAgent):
    """Agent responsible for role-playing game characters"""
    
    def __init__(self, character_profile: dict, level: int, genre: str):
        super().__init__(AgentRole.CHARACTER, character_profile)
        self.level = level
        self.genre = genre
        self.profile = character_profile  # Set initial profile
        personality = {
            "traits": self.profile.get("traits",["challenging", "engaging"]),
            "style": self.profile.get("style","enigmatic")
        }
        super().__init__(AgentRole.CHARACTER, personality)
        # logger.info(f"Created CharacterAgent for level {level} in {genre} genre")
        
    async def initialize(self):
        """Initialize character with detailed profile"""
        # logger.info("Starting character initialization...")
        try:
            await self._generate_character_profile(self.profile)
            # logger.info("Character initialization completed successfully")
        except Exception as e:
            logger.error(f"Character initialization failed: {str(e)}", exc_info=True)
            logger.info("Using default character profile")

        
    async def _generate_character_profile(self, base_profile: dict):
        """Generate detailed character profile using prompts"""
        # logger.debug("Generating character profile...")
        prompt = CHARACTER_PROMPTS["character_creation"].format(
            level_number=self.level,
            genre=self.genre,
            archetype=base_profile["archetype"],
            difficulty=base_profile.get("difficulty", "medium"),
            game_type=base_profile.get("game_type", "3D Tic Tac Toe")
        )
        
        try:
            # logger.debug(f"Using prompt: {prompt[:100]}...")
            response = await self.generate_response(prompt)
            # logger.debug(f"Received response: {response[:100]}...")
            self.profile = json.loads(response)
        except Exception as e:
            logger.error(f"Character generation failed: {str(e)}", exc_info=True)
            print(ERROR_MESSAGES["character_creation_failed"])
            self.profile = base_profile
        
    async def generate_dialogue(self, dialogue_type: str, context: dict) -> str:
        """Generate dialogue using configured prompts"""
        prompt_template = CHARACTER_PROMPTS["dialogue_generation"][dialogue_type]
        with open("output.txt","w") as f:
            f.write(str(self.profile))
            f.write(str(context))
        prompt = prompt_template.format(
            character_name=self.profile["name"],
            character_type=self.profile["archetype"],
            **context
        )
        
        return await self.generate_response(prompt)

class AdvisorAgent(LLMAgent):
    """Agent responsible for providing hints and guidance"""
    
    def __init__(self):
        personality = {
            "traits": ["helpful", "wise", "encouraging"],
            "style": "supportive and instructive"
        }
        super().__init__(AgentRole.ADVISOR, personality)
        
    async def generate_hint(self, game_state: dict, difficulty: int) -> str:
        """Generate hint using configured prompts"""
        prompt = ADVISOR_PROMPTS["hint_generation"].format(
            position=json.dumps(game_state.get("current_position", {})),
            history=json.dumps(game_state.get("history", [])),
            difficulty=difficulty
        )
        
        try:
            return await self.generate_response(prompt)
        except Exception:
            print(ERROR_MESSAGES["hint_generation_failed"])
            return None
    
    async def provide_strategy(self, game_type: str, position: dict, opponent_style: str) -> str:
        """Provide strategic advice"""
        prompt = ADVISOR_PROMPTS["strategy_advice"].format(
            game_type=game_type,
            position=json.dumps(position),
            opponent_style=opponent_style
        )
        
        return await self.generate_response(prompt)

class DifficultyAdapter:
    """Handles dynamic difficulty adjustment"""
    
    def __init__(self):
        self.performance_history = []
        self.adaptation_rate = 0.1
        
    def adjust(self, game_result: dict) -> dict:
        """Adjust difficulty based on player performance"""
        self.performance_history.append(game_result)
        
        # Calculate recent performance
        recent_performance = self._calculate_recent_performance()
        
        # Adjust difficulty
        current_difficulty = game_result['difficulty']
        if recent_performance > 0.7:  # Player doing very well
            new_difficulty = min(5, current_difficulty + self.adaptation_rate)
        elif recent_performance < 0.3:  # Player struggling
            new_difficulty = max(1, current_difficulty - self.adaptation_rate)
        else:
            new_difficulty = current_difficulty
            
        return {
            "new_difficulty": new_difficulty,
            "adaptation_reason": self._get_adaptation_reason(recent_performance)
        }
        
    def _calculate_recent_performance(self) -> float:
        """Calculate performance score from recent games"""
        if not self.performance_history:
            return 0.5
            
        recent_games = self.performance_history[-5:]  # Look at last 5 games
        wins = sum(1 for game in recent_games if game['result'] == 'win')
        return wins / len(recent_games)
        
    def _get_adaptation_reason(self, performance: float) -> str:
        """Provide explanation for difficulty adjustment"""
        if performance > 0.7:
            return "Player showing mastery - increasing challenge"
        elif performance < 0.3:
            return "Player needs more practice - adjusting difficulty"
        return "Player performing well at current level"