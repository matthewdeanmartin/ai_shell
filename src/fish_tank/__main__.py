# Fish Tank Main File

import os
import random
import time


class Fish:
    def __init__(self, emoji, x, y):
        """
        Initialize a fish with emoji and position.

        Args:
            emoji (str): The emoji that represents the fish.
            x (int): The x-coordinate of the fish in the tank.
            y (int): The y-coordinate of the fish in the tank.
        """
        self.emoji = emoji
        self.x = x
        self.y = y

    def move(self, width, height):
        """
        Move the fish randomly within the boundaries of the tank.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, width - 2))  # -2 to account for emoji width
        self.y = max(0, min(self.y, height - 1))


class Tank:
    def __init__(self, width, height):
        """
        Initialize a tank with given dimensions.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.width = width
        self.height = height
        self.fish = []
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def add_fish(self, fish):
        """
        Add a fish to the tank.

        Args:
            fish (Fish): An instance of Fish to add to the tank.
        """
        self.fish.append(fish)

    def update(self):
        """
        Update the position of all fish in the tank and render them to the buffer.
        """
        # Clear buffer
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Update and draw fish
        for f in self.fish:
            f.move(self.width, self.height)
            self.buffer[f.y][f.x] = f.emoji

    def render(self):
        """
        Print the current state of the tank to the console.
        """
        for row in self.buffer:
            print("".join(row))


def main():
    """
    Main function to set up the tank and run the simulation.
    """
    os.system("cls" if os.name == "nt" else "clear")

    tank_width, tank_height = 80, 24
    tank = Tank(tank_width, tank_height)

    for _ in range(random.randint(5, 10)):
        fish = Fish(
            random.choice(["🐟", "🐠", "🦈"]), random.randint(0, tank_width - 2), random.randint(0, tank_height - 1)
        )
        tank.add_fish(fish)

    while True:
        tank.update()
        os.system("cls" if os.name == "nt" else "clear")
        tank.render()
        time.sleep(0.5)


if __name__ == "__main__":
    main()


class Fish:
    def __init__(self, emoji, x, y):
        """
        Initialize a fish with emoji and position.

        Args:
            emoji (str): The emoji that represents the fish.
            x (int): The x-coordinate of the fish in the tank.
            y (int): The y-coordinate of the fish in the tank.
        """
        self.emoji = emoji
        self.x = x
        self.y = y

    def move(self, width, height):
        """
        Move the fish randomly within the boundaries of the tank.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, width - 2))  # -2 to account for emoji width
        self.y = max(0, min(self.y, height - 1))


class Tank:
    def __init__(self, width, height):
        """
        Initialize a tank with given dimensions.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.width = width
        self.height = height
        self.fish = []
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def add_fish(self, fish):
        """
        Add a fish to the tank.

        Args:
            fish (Fish): An instance of Fish to add to the tank.
        """
        self.fish.append(fish)

    def update(self):
        """
        Update the position of all fish in the tank and render them to the buffer.
        """
        # Clear buffer
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Update and draw fish
        for f in self.fish:
            f.move(self.width, self.height)
            self.buffer[f.y][f.x] = f.emoji

    def render(self):
        """
        Print the current state of the tank to the console.
        """
        for row in self.buffer:
            print("".join(row))


def main():
    """
    Main function to set up the tank and run the simulation.
    """
    os.system("cls" if os.name == "nt" else "clear")

    tank_width, tank_height = 80, 24
    tank = Tank(tank_width, tank_height)

    for _ in range(random.randint(5, 10)):
        fish = Fish(
            random.choice(["🐟", "🐠", "🦈"]), random.randint(0, tank_width - 2), random.randint(0, tank_height - 1)
        )
        tank.add_fish(fish)

    while True:
        tank.update()
        os.system("cls" if os.name == "nt" else "clear")
        tank.render()
        time.sleep(0.5)


if __name__ == "__main__":
    main()

# Fish Tank Main File


class Fish:
    def __init__(self, emoji, x, y):
        """
        Initialize a fish with emoji and position.

        Args:
            emoji (str): The emoji that represents the fish.
            x (int): The x-coordinate of the fish in the tank.
            y (int): The y-coordinate of the fish in the tank.
        """
        self.emoji = emoji
        self.x = x
        self.y = y

    def move(self, width, height):
        """
        Move the fish randomly within the boundaries of the tank.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, width - 2))  # -2 to account for emoji width
        self.y = max(0, min(self.y, height - 1))


class Tank:
    def __init__(self, width, height):
        """
        Initialize a tank with given dimensions.

        Args:
            width (int): The width of the tank.
            height (int): The height of the tank.
        """
        self.width = width
        self.height = height
        self.fish = []
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def add_fish(self, fish):
        """
        Add a fish to the tank.

        Args:
            fish (Fish): An instance of Fish to add to the tank.
        """
        self.fish.append(fish)

    def update(self):
        """
        Update the position of all fish in the tank and render them to the buffer.
        """
        # Clear buffer
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Update and draw fish
        for f in self.fish:
            f.move(self.width, self.height)
            self.buffer[f.y][f.x] = f.emoji

    def render(self):
        """
        Print the current state of the tank to the console.
        """
        for row in self.buffer:
            print("".join(row))


def main():
    """
    Main function to set up the tank and run the simulation.
    """
    os.system("cls" if os.name == "nt" else "clear")

    tank_width, tank_height = 80, 24
    tank = Tank(tank_width, tank_height)

    for _ in range(random.randint(5, 10)):
        fish = Fish(
            random.choice(["🐟", "🐠", "🦈"]), random.randint(0, tank_width - 2), random.randint(0, tank_height - 1)
        )
        tank.add_fish(fish)

    while True:
        tank.update()
        os.system("cls" if os.name == "nt" else "clear")
        tank.render()
        time.sleep(0.5)


if __name__ == "__main__":
    main()


class Fish:
    def __init__(self, emoji, x, y):
        self.emoji = emoji
        self.x = x
        self.y = y

    def move(self, width, height):
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, width - 2))  # -2 to account for emoji width
        self.y = max(0, min(self.y, height - 1))


class Tank:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fish = []
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def add_fish(self, fish):
        self.fish.append(fish)

    def update(self):
        # Clear buffer
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Update and draw fish
        for f in self.fish:
            f.move(self.width, self.height)
            self.buffer[f.y][f.x] = f.emoji

    def render(self):
        for row in self.buffer:
            print("".join(row))


def main():
    os.system("cls" if os.name == "nt" else "clear")

    tank_width, tank_height = 80, 24
    tank = Tank(tank_width, tank_height)

    for _ in range(random.randint(5, 10)):
        fish = Fish(
            random.choice(["🐟", "🐠", "🦈"]), random.randint(0, tank_width - 2), random.randint(0, tank_height - 1)
        )
        tank.add_fish(fish)

    while True:
        tank.update()
        os.system("cls" if os.name == "nt" else "clear")
        tank.render()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
