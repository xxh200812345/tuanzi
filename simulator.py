
import random
from collections import Counter

from dango import Dango
from skills_impl import (
    ShushudeWeilai, LingyinZhiMing, MouErHouDing,
    RuyinSuiXing, YigeRendeKahuan, RunrunJiabei,
)
from logger_util import setup_logger
from plot_result import plot_results
from board import Board

logger = setup_logger()
TRACK_LENGTH = 25
run_simulation_counter = 1 # 模拟次数计数器
SIMULATION_COUNT = 1000 # 模拟次数

def create_dangos():
    return [
        Dango("今汐", LingyinZhiMing("令尹之名")),
        Dango("守岸人", ShushudeWeilai("收束的未来")),
        Dango("长离", MouErHouDing("谋而后定")),
        Dango("卡卡罗", RuyinSuiXing("如影随形")),
        Dango("椿", YigeRendeKahuan("一个人的狂欢")),
        Dango("柯莱塔", RunrunJiabei("润润加倍")),
    ]


def simulate_game(game_id=None):
    global run_simulation_counter
    logger.info(f"---  游戏开始【{run_simulation_counter}/{SIMULATION_COUNT}】 ---")
    run_simulation_counter += 1

    dangos = create_dangos()
    board = Board(TRACK_LENGTH)
    delay_next = set()

    order = random.sample(dangos, len(dangos))
    for d in dangos:
        d.position = 0
    for d in order:
        board.place(0, d.name)

    name_to_dango = {d.name: d for d in dangos}
    round_num = 1
    board.clear()  # 清除初始堆叠，不影响第一轮技能逻辑

    while True:
        normal = [d for d in order if d.name not in delay_next]
        delayed = [d for d in order if d.name in delay_next]
        turn_order = normal + delayed
        delay_next.clear()

        logger.debug(f"--- Round {round_num} ---")
        logger.debug(f"Action Order: {[d.name for d in turn_order]}")

        for dango in turn_order:
            if dango.position >= TRACK_LENGTH:
                continue

            logger.debug(f"[{dango.name}] Position: {dango.position}")

            # 更新堆叠位置
            if round_num == 1:
                board.place(0, dango.name)
            stack = board.get_stack(dango.position)
            if dango.name in stack:
                dango.stack_index = stack.index(dango.name)
            else:
                dango.stack_index = 0

            # 技能：令尹之名
            if dango.top_stack_action(board):
                logger.debug(f"[{dango.name}] 使用技能: 令尹之名（栈顶调整）")

            bonus = dango.start_turn_bonus(dangos, board)
            if bonus > 0:
                logger.debug(f"[{dango.name}] 技能加成前移: +{bonus}")

            raw = dango.roll_dice()
            logger.debug(f"[{dango.name}] 掷骰点数: {raw}")

            move = raw + bonus + dango.move_bonus(board)
            logger.debug(f"[{dango.name}] 最终前进步数: {move}")

            from_pos = dango.position
            moving_names = board.move_dangos(from_pos, dango.name)

            if dango.delay_next_turn:
                delay_next.add(dango.name)
                dango.delay_next_turn = False
                logger.debug(f"[{dango.name}] 延后下轮行动")

            new_pos = min(from_pos + move, TRACK_LENGTH)
            for name in moving_names:
                board.place(new_pos, name)
                name_to_dango[name].position = new_pos

            logger.debug(f"[{dango.name}] 移动至 {new_pos}，新堆叠: {board.get_stack(new_pos)}")

            if any(d.position >= TRACK_LENGTH for d in dangos):
                winner = board.get_stack(TRACK_LENGTH)[-1]
                logger.debug(f"🎉 胜者: {winner}")
                logger.debug(f"---  游戏结束 ---")
                return winner

        logger.debug(f"{round_num}轮结束，各团子位置：")
        for d in dangos:
            stack_now = board.get_stack(d.position)
            d.stack_index = stack_now.index(d.name) if d.name in stack_now else -1
            logger.debug(f"  - {d.name:<8} | 位置: {d.position:>3} | 堆叠: {stack_now}")
        round_num += 1

def run_simulation():
    results = Counter(simulate_game(i) for i in range(SIMULATION_COUNT))
    for name, count in results.items():
        print(f"{name}: {count} 次胜利, 胜率: {count / SIMULATION_COUNT:.2%}")
    plot_results(results)
    return results

if __name__ == "__main__":
    run_simulation()
