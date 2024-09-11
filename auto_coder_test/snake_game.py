import random
import time

class SnakeGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.snake_length = 1
        self.snake_position = [[100, 50]]
        self.food_position = [random.randint(0, 50) * 10, random.randint(0, 50) * 10]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def update_snake(self):
        current_position = self.snake_position[0].copy()

        if self.direction == 'UP':
            current_position[1] -= 10
        if self.direction == 'DOWN':
            current_position[1] += 10
        if self.direction == 'LEFT':
            current_position[0] -= 10
        if self.direction == 'RIGHT':
            current_position[0] += 10

        self.snake_position.insert(0, current_position)

        if current_position == self.food_position:
            self.score += self.get_score_increment()
            self.snake_length += 1
            self.food_position = [random.randint(0, 50) * 10, random.randint(0, 50) * 10]
        else:
            self.snake_position.pop()

    def get_score_increment(self):
        if self.difficulty == 'easy':
            return 1
        elif self.difficulty == 'medium':
            return 2
        elif self.difficulty == 'hard':
            return 3
        return 0

    def change_direction(self, new_direction):
        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def is_collision(self):
        if self.snake_position[0][0] >= 500 or self.snake_position[0][0] < 0:
            return True
        if self.snake_position[0][1] >= 500 or self.snake_position[0][1] < 0:
            return True
        if self.snake_position[0] in self.snake_position[1:]:
            return True
        return False

    def play(self):
        while True:
            self.update_snake()
            if self.is_collision():
                print(f"Game Over! Your score is {self.score}")
                break
            time.sleep(0.1)