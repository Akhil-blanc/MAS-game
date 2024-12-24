"""
Configuration file for the multi-agent game system containing prompts,
system messages, and game configurations.
"""

import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-1.5-flash')

# Game Genres Configuration
GAME_GENRES = {
    "fantasy": {
        "themes": ["magic", "medieval", "mythical creatures"],
        "character_archetypes": ["wizard", "knight", "dragon", "mystic"],
        "setting_elements": ["castles", "enchanted forests", "magical realms"],
        "tone": "mystical and adventurous"
    },
    "sci_fi": {
        "themes": ["technology", "space exploration", "artificial intelligence"],
        "character_archetypes": ["android", "space captain", "alien", "scientist"],
        "setting_elements": ["spaceships", "distant planets", "futuristic cities"],
        "tone": "technological and mysterious"
    },
    "mystery": {
        "themes": ["investigation", "deduction", "secrets"],
        "character_archetypes": ["detective", "suspect", "witness", "mastermind"],
        "setting_elements": ["dark alleys", "hidden rooms", "crime scenes"],
        "tone": "suspenseful and intriguing"
    }
}

# Agent Prompt Templates
STORYTELLER_PROMPTS = {
    "story_generation": """
    As a creative storyteller, craft an engaging {genre} story with the following elements:
    
    Story Requirements:
    - Genre: {genre}
    - Player Preferences: {preferences}
    - Narrative Style: {style}
    
    Create a complete story structure including:
    1. An overarching narrative that spans three distinct levels
    2. Unique characters for each level that match the {genre} theme
    3. Progressive difficulty increase across levels
    4. Compelling motivations for each character
    5. Clear victory and defeat conditions
    
    The story should incorporate these specific elements:
    - Opening Setup: Introduce the world and initial challenge
    - Level Progression: Each level should build upon previous revelations
    - Character Depth: Each opponent should have clear motivations and personality
    - Plot Twists: Include surprising but logical story developments
    - Resolution Paths: Multiple possible endings based on player performance
    
    Format the response as a detailed JSON structure with the following keys:
    - name
    - opening_narrative
    - levels (array of 3 levels with characters and challenges)
    - overall_arc
    - victory_conditions
    - defeat_conditions
    """,
    
    "level_transition": """
    Create a transition narrative for moving from level {current_level} to level {next_level}.
    
    Consider:
    - Previous level outcome: {outcome}
    - Player's current progress: {progress}
    - Next challenger's personality: {challenger_profile}
    
    The transition should:
    1. Acknowledge the player's previous victory/defeat
    2. Foreshadow the next challenge
    3. Maintain the {genre} atmosphere
    4. Include character development
    """,
    
    "story_adaptation": """
    Adapt the current story based on player's performance:
    
    Current State:
    - Story Progress: {progress}
    - Player Performance: {performance}
    - Current Narrative Arc: {current_arc}
    
    Generate modifications that:
    1. Adjust difficulty naturally through story elements
    2. Maintain narrative consistency
    3. Keep player engagement high
    4. Provide appropriate challenge level
    """
}

CHARACTER_PROMPTS = {
    "character_creation": """
    Create a detailed character profile for level {level_number} in a {genre} setting.
    
    Character Requirements:
    - Archetype: {archetype}
    - Difficulty Level: {difficulty}
    - Game Type: {game_type}
    
    Include:
    1. Personality traits
    2. Background story
    3. Motivation for challenging player
    4. Unique dialogue style
    5. Victory and defeat reactions
    
    The character should:
    - Match the {genre} theme
    - Present appropriate challenge for level {level_number}
    - Have clear personality traits
    - Maintain consistent dialogue style
    """,
    
    "dialogue_generation": {
        "greeting": """
        Generate a greeting dialogue for {character_name} meeting the player.
        
        Context:
        - Character Type: {character_type}
        - Game Progress: {progress}
        - Previous Interaction: {previous_interaction}
        
        The greeting should:
        1. Reflect character personality
        2. Hint at upcoming challenge
        3. Match game atmosphere
        """,
        
        "challenge": """
        Generate a challenge dialogue for {character_name}.
        
        Context:
        - Current Game State: {game_state}
        - Player Performance: {performance}
        - Difficulty Level: {difficulty}
        
        The challenge should:
        1. Be appropriate for difficulty level
        2. Maintain character voice
        3. Include game-specific elements
        """,
        
        "victory": """
        Generate victory dialogue for {character_name}.
        
        Context:
        - Match Result: {result}
        - Player Strategy: {strategy}
        - Game History: {history}
        
        Include:
        1. Recognition of player's effort
        2. Character-appropriate reaction
        3. Hook for next challenge
        """,
        
        "defeat": """
        Generate defeat dialogue for {character_name}.
        
        Context:
        - Match Result: {result}
        - Player Strategy: {strategy}
        - Game History: {history}
        
        Include:
        1. Graceful acknowledgment
        2. Character development
        3. Forward progression element
        """
    }
}

GAME_MASTER_PROMPTS = {
    "game_selection": """
    Select and configure a game challenge based on:
    
    Player Information:
    - Skill Level: {skill_level}
    - Past Performance: {performance}
    - Preferred Style: {style}
    
    Level Requirements:
    - Difficulty Target: {difficulty}
    - Theme Consistency: {theme}
    - Time Constraints: {time_limit}
    
    Choose from available game types as game_type:
    1. 3D Tic Tac Toe
    2. Strategic Rock Paper Scissors
    3. Number Prediction Game
    
    
    Configure:
    - Specific rules and variations
    - Difficulty parameters
    - Victory conditions
    - Special mechanics
    """,
    
    "difficulty_adjustment": """
    Analyze current game state and adjust difficulty:
    
    Current State:
    - Player Performance: {performance}
    - Current Difficulty: {difficulty}
    - Game Type: {game_type}
    
    Consider:
    1. Recent win/loss ratio
    2. Play style adaptation
    3. Learning curve progression
    4. Engagement maintenance
    """
}

ADVISOR_PROMPTS = {
    "hint_generation": """
    Generate a helpful hint based on:
    
    Game State:
    - Current Position: {position}
    - Player History: {history}
    - Difficulty Level: {difficulty}
    
    Requirements:
    1. Maintain difficulty appropriate clarity
    2. Avoid direct solutions
    3. Guide rather than solve
    4. Consider player skill level
    """,
    
    "strategy_advice": """
    Provide strategic guidance for:
    
    Current Situation:
    - Game Type: {game_type}
    - Player Position: {position}
    - Opponent Style: {opponent_style}
    
    Advice should:
    1. Be level-appropriate
    2. Encourage learning
    3. Highlight key concepts
    4. Build long-term skill
    """
}

# Game Configurations
GAME_CONFIGS = {
    "3D_tic_tac_toe": {
        "grid_size": 4,
        "dimensions": 3,
        "win_length": 4,
        "difficulty_levels": {
            "easy": {
                "ai_depth": 2,
                "mistake_probability": 0.2
            },
            "medium": {
                "ai_depth": 3,
                "mistake_probability": 0.1
            },
            "hard": {
                "ai_depth": 4,
                "mistake_probability": 0.05
            }
        },
        "special_rules": {
            "gravity_enabled": False,
            "power_ups_allowed": True,
            "time_limited": False
        }
    },
    
    "strategic_rps": {
        "rounds_per_match": 5,
        "power_moves_allowed": True,
        "difficulty_levels": {
            "easy": {
                "pattern_recognition": False,
                "counter_probability": 0.3
            },
            "medium": {
                "pattern_recognition": True,
                "counter_probability": 0.5
            },
            "hard": {
                "pattern_recognition": True,
                "counter_probability": 0.7,
                "adaptive_strategy": True
            }
        },
        "special_rules": {
            "elemental_powers": True,
            "combo_moves": True,
            "power_meter": True
        }
    },
    
    "number_prediction": {
        "range": (1, 100),
        "rounds_per_match": 7,
        "difficulty_levels": {
            "easy": {
                "hint_frequency": 3,
                "pattern_complexity": 1
            },
            "medium": {
                "hint_frequency": 2,
                "pattern_complexity": 2
            },
            "hard": {
                "hint_frequency": 1,
                "pattern_complexity": 3,
                "dynamic_patterns": True
            }
        },
        "special_rules": {
            "pattern_based": True,
            "multi_number": False,
            "time_pressure": True
        }
    }
}

# Performance Tracking Configuration
PERFORMANCE_METRICS = {
    "win_rate_threshold": {
        "increase_difficulty": 0.7,
        "decrease_difficulty": 0.3
    },
    "adaptation_rates": {
        "quick": 0.2,
        "normal": 0.1,
        "slow": 0.05
    },
    "performance_window": 5,  # Number of recent games to consider
    "skill_categories": [
        "novice",
        "intermediate",
        "advanced",
        "expert",
        "master"
    ],
    "progression_thresholds": {
        "level_completion": 0.6,  # Win rate needed to progress
        "mastery": 0.8  # Win rate indicating level mastery
    }
}

# Error Messages and Fallbacks
ERROR_MESSAGES = {
    "story_generation_failed": "Unable to generate story. Using backup narrative...",
    "character_creation_failed": "Character creation failed. Using default character...",
    "game_selection_failed": "Game selection failed. Defaulting to basic game mode...",
    "hint_generation_failed": "Hint unavailable. Try exploring different strategies.",
    "difficulty_adjustment_failed": "Keeping current difficulty level..."
}

# Default Game State
DEFAULT_GAME_STATE = {
    "current_level": 0,
    "difficulty": "medium",
    "score": 0,
    "games_played": 0,
    "current_streak": 0,
    "inventory": [],
    "unlocked_features": set(),
    "tutorial_completed": False
}