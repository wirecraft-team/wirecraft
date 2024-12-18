from src.client import Camera, Game


def main():
    game = Game("menu", Camera(0, 0, 1))
    game.start()


if __name__ == "__main__":
    main()
