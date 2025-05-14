
import random

class Dango:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.position = 0           # 当前所在格子
        self.stack_index = 0        # 当前在该格子的堆叠位置（0 是最底）
        self.delay_next_turn = False  # 是否延后下一回合出手

    def roll_dice(self):
        val = self.skill.modify_dice(self)
        return val if val is not None else random.randint(1, 3)

    def start_turn_bonus(self, all_dangos, board):
        return self.skill.on_start_turn(self, all_dangos, board)

    def top_stack_action(self, board):
        return self.skill.on_top_stack(self, board)

    def move_bonus(self, board):
        return self.skill.on_move(self, board)
