
import matplotlib.pyplot as plt


def plot_results(results, output_path="logs/dango_result_chart.png"):
    names = list(results.keys())
    counts = list(results.values())

    # 设置中文字体（推荐使用 SimHei）
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑（通常 Windows 默认有）

    plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, counts)

    plt.xlabel("团子名字")
    plt.ylabel("胜利次数")
    plt.title("团子胜率统计图（模拟结果）")
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom')

    plt.savefig(output_path)
    plt.close()
