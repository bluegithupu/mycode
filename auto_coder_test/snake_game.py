import random
import time
import pygame

pygame.init()

class SnakeGame:
    def __init__(self):
        self.difficulty = None
        self.score = 0
        self.snake_length = 1
        self.snake_position = [[100, 50]]
        self.food_position = [random.randint(0, 50) * 10, random.randint(0, 50) * 10]
        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.display = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.font = pygame.font.Font(None, 36)

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

    def draw_snake(self):
        snake_head_img = pygame.image.load('snake_head.png')
        for position in self.snake_position:
            self.display.blit(snake_head_img, (position[0], position[1]))

    def draw_food(self):
        food_img = pygame.image.load('food.png')
        self.display.blit(food_img, (self.food_position[0], self.food_position[1]))

    def play(self):
        self.selected_difficulty = 0
        while self.difficulty is None:
            self.display.fill(self.black)  # Fixed indentation
            self.display_difficulty_selection()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_difficulty = (self.selected_difficulty - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.selected_difficulty = (self.selected_difficulty + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if self.selected_difficulty == 0:
                            self.difficulty = 'easy'
                        elif self.selected_difficulty == 1:
                            self.difficulty = 'medium'
                        elif self.selected_difficulty == 2:
                            self.difficulty = 'hard'

        paused = False
        
        while True:
            if paused:
                self.display_pause_menu()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = False
            else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.change_direction('RIGHT')

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = True

                self.update_snake()
            background_img = pygame.image.load('background.png')
        self.display.blit(background_img, (0, 0))
            self.draw_snake()
            self.draw_food()
            self.display_score()
            pygame.display.update()
            self.clock.tick(15)

            if self.is_collision():
                print(f"Game Over! Your score is {self.score}")
                pygame.quit()
                quit()
    def display_pause_menu(self):
        text = self.font.render("Paused - Press 'P' to Resume", True, self.black)
        text_rect = text.get_rect(center=(250, 250))
        self.display.blit(text, text_rect)

        options = ["Easy", "Medium", "Hard"]
        for i, option in enumerate(options):
            text = self.font.render(f"{option}", True, self.black if i != self.selected_difficulty else self.red)
            text_rect = text.get_rect(center=(250, 200 + i * 50))
            self.display.blit(text, text_rect)

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.black)
        self.display.blit(score_text, (10, 10))