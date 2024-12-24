import random
from typing import Tuple

class NumberPredictionGame:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.reset_game()
        
    def reset_game(self):
        """Initialize a new number sequence"""
        # Generate a sequence based on difficulty
        self.sequence_length = 3 + int(self.difficulty)  # Longer sequences for higher difficulty
        self.pattern_type = random.choice(['arithmetic', 'geometric', 'fibonacci'])
        
        if self.pattern_type == 'arithmetic':
            # Generate arithmetic sequence: each number differs by a constant
            start = random.randint(1, 10)
            difference = random.randint(2, 5)
            self.sequence = [start + i * difference for i in range(self.sequence_length)]
            self.next_number = start + self.sequence_length * difference
            
        elif self.pattern_type == 'geometric':
            # Generate geometric sequence: each number is multiplied by a constant
            start = random.randint(1, 5)
            ratio = random.randint(2, 3)
            self.sequence = [start * (ratio ** i) for i in range(self.sequence_length)]
            self.next_number = start * (ratio ** self.sequence_length)
            
        else:  # fibonacci-like
            # Generate Fibonacci-like sequence: each number is sum of previous two
            start1 = random.randint(1, 5)
            start2 = random.randint(6, 10)
            self.sequence = [start1, start2]
            for _ in range(self.sequence_length - 2):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
            self.next_number = self.sequence[-1] + self.sequence[-2]
            
        self.attempts = 0
        self.max_attempts = 3
        self.hints_given = 0
        
    def check_prediction(self, prediction: int) -> Tuple[bool, str]:
        """Check if the prediction matches the next number"""
        self.attempts += 1
        
        if prediction == self.next_number:
            return True, "Correct! You've found the next number in the sequence!"
            
        difference = abs(prediction - self.next_number)
        if self.attempts >= self.max_attempts:
            return False, f"Game Over! The correct number was {self.next_number}"
            
        # Provide feedback based on how close the guess was
        if difference <= 2:
            return False, "Very close! Try again."
        elif difference <= 5:
            return False, "Getting warmer! Try again."
        else:
            return False, "Not quite. Try again."
            
    def get_hint(self) -> str:
        """Generate a hint based on the pattern type and current sequence"""
        self.hints_given += 1
        
        if self.hints_given == 1:
            return f"Look at the first {min(3, len(self.sequence))} numbers: {self.sequence[:3]}"
            
        if self.pattern_type == 'arithmetic':
            return "Try finding the constant difference between consecutive numbers."
        elif self.pattern_type == 'geometric':
            return "Try finding the constant ratio between consecutive numbers."
        else:
            return "Each number is related to the two numbers before it."
            
    def get_sequence_display(self) -> str:
        """Return the current sequence for display"""
        return " → ".join(map(str, self.sequence)) + " → ?"