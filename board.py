# 新建文件：board.py（棋盘管理类，支持堆叠与查询）

class Board:
    def __init__(self, length):
        # 初始化格子，每格子对应一个从底到顶的团子名字列表
        self.length = length
        self.cells = [[] for _ in range(length + 1)]  # 格子编号 0 ~ length

    def place(self, position, dango_name):
        """将团子加入到指定格子顶部"""
        self.cells[position].append(dango_name)

    def remove(self, position, dango_name):
        """从指定格子移除团子"""
        self.cells[position].remove(dango_name)

    def get_stack(self, position):
        """获取当前格子上堆叠（从底到顶）"""
        return self.cells[position]

    def clear(self):
        """清空所有格子"""
        for cell in self.cells:
            cell.clear()

    def move_dangos(self, from_pos, dango_name):
        """
        将某个团子及其上方所有团子从一个格子移动出来（不改变位置），返回这些团子名称列表。
        若该团子当前不在格子中，则只移动自己。
        """
        stack = self.cells[from_pos]
        if dango_name in stack:
            idx = stack.index(dango_name)
            moving = stack[idx:]
            self.cells[from_pos] = stack[:idx]
        else:
            moving = [dango_name]
        return moving

    def print_board(self):
        """打印所有格子的团子堆叠（调试用）"""
        for idx, stack in enumerate(self.cells):
            if stack:
                print(f"格子 {idx}: {stack}")

