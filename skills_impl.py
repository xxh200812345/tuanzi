
import random
from skill_base import Skill

class ShushudeWeilai(Skill):
    def __init__(self, name): super().__init__(name)

    def modify_dice(self, dango):
        # 技能：收束的未来（守岸人）
        return random.choice([2, 3])


class LingyinZhiMing(Skill):
    def __init__(self, name): super().__init__(name)

    def on_top_stack(self, dango, board):
        if dango.position == 0:
            return False
        # 技能：令尹之名（今汐）
        stack = board.get_stack(dango.position)
        if stack and stack[-1] != dango.name and random.random() < 0.4:
            stack.remove(dango.name)
            stack.append(dango.name)
            return True
        return False


class MouErHouDing(Skill):
    def __init__(self, name): super().__init__(name)

    def on_start_turn(self, dango, dangos, board):
        # 技能：谋而后定（长离）
        stack = board.get_stack(dango.position)
        if stack.index(dango.name) < len(stack) - 1 and random.random() < 0.65:
            dango.delay_next_turn = True
        return 0


class RuyinSuiXing(Skill):
    def __init__(self, name): super().__init__(name)

    def on_start_turn(self, dango, dangos, board):
        # 技能：如影随形（卡卡罗）
        if dango.position == 0:
            return 0
        if all(dango.position <= other.position for other in dangos if other.name != dango.name):
            return 3
        return 0


class YigeRendeKahuan(Skill):
    def __init__(self, name): super().__init__(name)

    def on_move(self, dango, board):
        # 技能：一个人的狂欢（椿）
        if random.random() < 0.5:
            return len(board.get_stack(dango.position)) - 1
        return 0


class RunrunJiabei(Skill):
    def __init__(self, name): super().__init__(name)

    def modify_dice(self, dango):
        # 技能：润润加倍（柯莱塔）
        base = random.randint(1, 3)
        if random.random() < 0.28:
            return base * 2
        return base
