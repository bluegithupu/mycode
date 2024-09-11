from snake_game import SnakeGame

def main():
    print("Welcome to Snake Game!")
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    game = SnakeGame(difficulty)
    game.play()

if __name__ == "__main__":
    main()