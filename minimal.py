class Playfield():
    def __init__(self, that_list):
        self.that_list = that_list
    def handle_something(self):
        self.that_list.append(2)


class Game():
    def __init__(self):
        pass
    def run_game(self):
        self.list_of_things = list()
        self.playfield = Playfield(self.list_of_things)
        self.list_of_things.append(1)
        self.playfield.handle_something()
        print(f"list in game instance: {self.list_of_things}")
        print(f"list in game.playfield instance : {self.playfield.that_list}")

g = Game()
g.run_game()
