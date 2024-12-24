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
    
    Return the response in the following JSON format:
    {{
        "name": "story_name",
        "opening_narrative": "introductory_text",
        "levels": [
            {{
                "level_number": 1,
                "name": "level_name",
                "description": "level_description",
                "character": {{
                    "name": "character_name",
                    "archetype": "character_type",
                    "motivation": "character_motivation"
                }},
                "challenge": {{
                    "type": "challenge_type",
                    "description": "challenge_description",
                    "victory_condition": "win_condition",
                    "defeat_condition": "lose_condition"
                }}
            }}
        ],
        "overall_arc": {{
            "main_conflict": "conflict_description",
            "resolution_paths": ["possible_ending_1", "possible_ending_2"]
        }},
        "victory_conditions": {{
            "primary": "main_victory_condition",
            "bonus": ["bonus_condition_1", "bonus_condition_2"]
        }},
        "defeat_conditions": ["defeat_condition_1", "defeat_condition_2"]
    }}
    """,
    
    "level_transition": """
    Create a transition narrative for moving from level {current_level} to level {next_level}.
    
    Consider:
    - Previous level outcome: {outcome}
    - Player's current progress: {progress}
    - Next challenger's personality: {challenger_profile}
    
    Return the response in the following JSON format:
    {{
        "transition_text": "main_narrative_text",
        "acknowledgment": {{
            "previous_outcome": "outcome_specific_text",
            "player_achievement": "achievement_recognition"
        }},
        "foreshadowing": {{
            "next_challenge": "hint_about_next_level",
            "character_intro": "new_character_teaser"
        }},
        "atmosphere": {{
            "mood": "atmospheric_description",
            "setting_changes": "environment_changes"
        }}
    }}
    """,
    
    "story_adaptation": """
    Adapt the current story based on player's performance:
    
    Current State:
    - Story Progress: {progress}
    - Player Performance: {performance}
    - Current Narrative Arc: {current_arc}
    
    Return the response in the following JSON format:
    {{
        "narrative_adjustments": {{
            "difficulty_changes": "story_based_difficulty_modifications",
            "pacing_changes": "modified_story_pacing"
        }},
        "character_adaptations": {{
            "personality_shifts": "character_behavior_changes",
            "motivation_updates": "new_character_motivations"
        }},
        "challenge_modifications": {{
            "complexity": "adjusted_challenge_level",
            "new_elements": ["added_element_1", "added_element_2"]
        }},
        "engagement_features": {{
            "new_hooks": ["engagement_element_1", "engagement_element_2"],
            "reward_adjustments": "modified_reward_structure"
        }}
    }}
    """
}

CHARACTER_PROMPTS = {
    "character_creation": """
    Create a detailed character profile for level {level_number} in a {genre} setting.
    
    Character Requirements:
    - Archetype: {archetype}
    - Difficulty Level: {difficulty}
    - Game Type: {game_type}
    
    Return the response in the following JSON format:
    {{
        "name": "character_name",
        "archetype": "character_archetype",
        "difficulty": "difficulty_level",
        "personality": {{
            "traits": ["trait_1", "trait_2", "trait_3"],
            "speaking_style": "dialogue_style_description",
            "behavior_patterns": ["pattern_1", "pattern_2"]
        }},
        "background": {{
            "origin": "character_origin",
            "motivation": "character_motivation",
            "goals": ["goal_1", "goal_2"]
        }},
        "game_specific": {{
            "challenge_style": "gameplay_approach",
            "special_moves": ["move_1", "move_2"],
            "victory_style": "win_reaction_description",
            "defeat_style": "loss_reaction_description"
        }},
        "dialogue_examples": {{
            "greeting": "sample_greeting",
            "challenge": "sample_challenge_quote",
            "victory": "sample_victory_quote",
            "defeat": "sample_defeat_quote"
        }}
    }}
    """,
    
    "dialogue_generation": {
        "greeting": """
        Generate a greeting dialogue for {character_name} meeting the player.
        
        Context:
        - Character Type: {character_type}
        - Game Progress: {progress}
        - Previous Interaction: {previous_interaction}
        
        Return the response in the following JSON format:
        {{
            "dialogue_text": "main_greeting_text",
            "tone": "emotional_tone",
            "body_language": "character_gestures",
            "hints": {{
                "challenge_type": "subtle_hint",
                "difficulty": "difficulty_indicator"
            }}
        }}
        """,
        
        "challenge": """
        Generate a challenge dialogue for {character_name}.
        
        Context:
        - Current Game State: {game_state}
        - Player Performance: {performance}
        - Difficulty Level: {difficulty}
        
        Return the response in the following JSON format:
        {{
            "dialogue_text": "main_challenge_text",
            "rules_explanation": "game_rules_description",
            "difficulty_indicators": {{
                "explicit": "stated_challenge_level",
                "implicit": "subtle_difficulty_hints"
            }},
            "character_attitude": "emotional_state"
        }}
        """,
        
        "victory": """
        Generate victory dialogue for {character_name}.
        
        Context:
        - Match Result: {result}
        - Player Strategy: {strategy}
        
        
        Return the response in the following JSON format:
        {{
            "dialogue_text": "main_victory_text",
            "acknowledgment": {{
                "player_skill": "skill_recognition",
                "specific_moves": "notable_strategies"
            }},
            "character_growth": "character_development_note",
            "next_challenge": "future_challenge_hint"
        }}
        """,
        
        "defeat": """
        Generate defeat dialogue for {character_name}.
        
        Context:
        - Match Result: {result}
        - Player Strategy: {strategy}
        
        
        Return the response in the following JSON format:
        {{
            "dialogue_text": "main_defeat_text",
            "reaction": {{
                "emotional": "character_feelings",
                "behavioral": "character_actions"
            }},
            "development": "character_growth_moment",
            "future_implications": "story_progression_hint"
        }}
        """,
        "action_response": """
            Generate a contextual response to the player's action.
            
            Current Context:
            - Player Action: {player_action}
            - Game: {current_game}
            - Character Name: {character_name}
            - Character Type: {character_type}
            
            
            Return the response in the following JSON format:
            {{
                "dialogue": {{
                    "text": "character_response_text",
                    "tone": "emotional_tone",
                    "intensity": "response_intensity_level"
                }},
                "reaction": {{
                    "immediate": {{
                        "emotion": "emotional_reaction",
                        "behavior": "physical_reaction",
                        "gameplay_adjustment": "tactical_response"
                    }},
                    "strategic": {{
                        "assessment": "action_evaluation",
                        "adaptation": "strategy_modification"
                    }}
                }},
                "character_state": {{
                    "current_attitude": "attitude_towards_player",
                    "respect_level": "respect_value",
                    "teaching_moment": "learning_opportunity"
                }},
                "game_progression": {{
                    "narrative_impact": "story_progression_effect",
                    "difficulty_suggestion": "difficulty_adjustment_hint",
                    "next_challenge_seed": "future_challenge_setup"
                }}
            }}
            """
    }
}

GAME_MASTER_PROMPTS = {
    "game_selection": """
    Select and configure a game challenge based on provided information.

    Choose from available game types as game_type:
    1. 3D Tic Tac Toe
    2. Strategic Rock Paper Scissors
    3. Number Prediction Game
    
    Player Information:
    - Skill Level: {skill_level}
    - Past Performance: {performance}
    - Preferred Style: {style}
    
    Return the response in the following JSON format:
    {{
        "selected_game": {{
            "type": "game_type_name",
            "difficulty": "difficulty_level",
            "configuration": {{
                "rules": ["rule_1", "rule_2"],
                "special_mechanics": ["mechanic_1", "mechanic_2"],
                "time_limits": "time_constraints"
            }}
        }},
        "victory_conditions": {{
            "primary": "main_win_condition",
            "bonus": ["bonus_condition_1", "bonus_condition_2"]
        }},
        "difficulty_parameters": {{
            "ai_level": "ai_difficulty",
            "complexity": "game_complexity",
            "adaptivity": "adaptation_settings"
        }}
    }}
    """,
    
    "difficulty_adjustment": """
    Analyze current game state and adjust difficulty.
    
    Current State:
    - Player Performance: {performance}
    - Current Difficulty: {difficulty}
    - Game Type: {game_type}
    
    Return the response in the following JSON format:
    {{
        "difficulty_changes": {{
            "new_level": "adjusted_difficulty",
            "parameters": {{
                "ai_behavior": "modified_ai_settings",
                "game_rules": "updated_rules",
                "time_pressure": "time_modifications"
            }}
        }},
        "adaptation_basis": {{
            "performance_metrics": ["metric_1", "metric_2"],
            "learning_curve": "learning_assessment",
            "engagement_factors": ["factor_1", "factor_2"]
        }},
        "immediate_changes": ["change_1", "change_2"],
        "gradual_changes": ["planned_change_1", "planned_change_2"]
    }}
    """
}

ADVISOR_PROMPTS = {
    "hint_generation": """
    Generate a helpful hint based on current game state.
    
    Game State:
    - Current Position: {position}
    
    - Difficulty Level: {difficulty}
    
    Return the response in the following JSON format:
    {{
        "hint": {{
            "text": "main_hint_text",
            "type": "hint_category",
            "specificity": "hint_detail_level"
        }},
        "context": {{
            "game_state": "relevant_state_info",
            "skill_level": "player_skill_assessment"
        }},
        "learning_focus": {{
            "concept": "main_learning_point",
            "application": "practical_usage"
        }}
    }}
    """,
    
    "strategy_advice": """
    Provide strategic guidance for the current situation.
    
    Current Situation:
    - Game Type: {game_type}
    - Player Position: {position}
    - Opponent Style: {opponent_style}
    
    Return the response in the following JSON format:
    {{
        "strategy": {{
            "general_approach": "overall_strategy",
            "specific_tactics": ["tactic_1", "tactic_2"]
        }},
        "learning_elements": {{
            "key_concepts": ["concept_1", "concept_2"],
            "skill_development": "skills_to_focus"
        }},
        "application": {{
            "immediate": "current_move_advice",
            "long_term": "strategic_development_path"
        }}
    }}
    """
}