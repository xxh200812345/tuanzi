
class Skill:
    def __init__(self, name):
        self.name = name

    def modify_dice(self, dango):
        return None

    def on_start_turn(self, dango, dangos, stacks):
        return 0

    def on_move(self, dango, stacks):
        return 0

    def on_top_stack(self, dango, stacks):
        return False
