# Proof of concept interface
''' Test game for elixir backend game server.
    This game is a tile based game where a randomly
    generated party is created and scattered on a board
    you can then move the party members around and have
    them attack each other.

    From a programming prospective this is mothing amazing.
    It was also writen at 4am so excuse any poor spelling
    or naming decisions.'''

from random import randint
import string
import names

SPEED_RANGE = (1, 100)
ATTACK_RANGE = (10, 60)
HEALTH_RANGE = (150, 240)
MOVABLE_DIRECTIONS = ('up', 'down', 'left', 'right')


class Game:
    def __init__(self, characters, board):
        self.characters = characters
        self.board = board

    @property
    def alive(self):
        return len(list(filter(lambda c: c.health > 0, self.characters)))

    def get_character_by_name(self, name):
        name = name.lower()
        chars = filter(lambda c: c.name.lower() == name, self.characters)
        return next(chars, None)

    def move(self, character_name, direction):
        if direction not in MOVABLE_DIRECTIONS:
            print(f'Cannot move {direction}; options are {MOVABLE_DIRECTIONS}')
            raise Exception

        character = self.get_character_by_name(character_name)
        if character is None:
            print(f'Character {character_name} was not found')
            raise Exception

        for position in self.board.positions:
            if position[0] == character:
                x, y = position[1]
                if direction == 'up' and y > 0:
                    self.board.update_position(character, (x, y - 1))
                elif direction == 'down' and y < self.board.size:
                    self.board.update_position(character, (x, y + 1))
                elif direction == 'left' and x > 0:
                    self.board.update_position(character, (x - 1, y))
                elif direction == 'right' and x < self.board.size:
                    self.board.update_position(character, (x + 1, y))
                else:
                    print(f'invalid movement {direction} from {(x, y)}')


class Board:
    '''
    (0, 0) (1, 0) (2, 0) ...
    (0, 1) (1, 1) (2, 1) ...
    (0, 2) (1, 2) (2, 2) ...
    (0, 3) (1, 3) (2, 3) ...
     ...    ...    ...'''

    def __init__(self, size, characters):
        self.size = size
        self.characters = characters
        self.positions = []
        self.initialize_character_positions()

    def initialize_character_positions(self):
        used = []

        for character in self.characters:
            position = None
            while position is None or position in used:
                position = (randint(0, self.size), randint(0, self.size))

            used.append(position)
            self.positions.append((character, position))

    def display(self):
        for (character, position) in self.positions:
            print(f'{character.name}:\t({position[0]}, {position[1]})')

    def update_position(self, character, position):
        self.positions = [
            (c, p) if (c != character) else (character, position)
            for (c, p) in self.positions
        ]


class Character:
    @classmethod
    def random(cls):
        return cls(
            names.get_first_name(),
            randint(*SPEED_RANGE),
            randint(*ATTACK_RANGE),
            randint(*HEALTH_RANGE))

    def __init__(self, name, speed, attack, health):
        self.name = name
        self.speed = speed
        self.attack = attack
        self.health = health

    def display(self):
        print(f"""{self.name}
    speed:  {self.speed}
    attack: {self.attack}
    health: {self.health}""")


def create_party(size):
    party = []
    for i in range(size):
        party.append(Character.random())

    return party


def display_party(party):
    print(' === YOUR PARTY === ')
    for character in party:
        character.display()


if __name__ == '__main__':
    party = create_party(6)
    # display_party(party)
    board = Board(4, party)
    game = Game(party, board)
    board.display()

    while game.alive > 1:
        try:
            print(f'({game.alive} alive)> ', end='')
            command = input().strip().split()
            command, args = command[0], command[1:]

            if command == 'quit':
                exit(0)
            elif command == 'help':
                print('lol this is less than 200 lines of source code.\n'
                      'Just open the code and take a look.')
            elif command == 'party':
                display_party(party)
            elif command == 'positions':
                board.display()
            elif command == 'move' and len(args) is 2:
                character_name = args[0]
                direction = args[1]
                game.move(character_name, direction)
            else:
                print('bad command, type help for help')
        except Exception as e:
            pass


