import matplotlib.pyplot as plt
import math

def apply_rules(axiom, rules, iterations):
    """
    生成L-System字符串
    :param axiom: 初始字符串（如"F"或"0"）
    :param rules: 规则字典，如{"F": "F+F--F+F"} 或 {"1": "11", "0": "1[0]0"}
    :param iterations: 迭代次数
    :return: 经过多轮迭代后的最终字符串
    """
    current = axiom
    for _ in range(iterations):
        next_str = []
        for char in current:
            if char in rules:
                next_str.append(rules[char])
            else:
                next_str.append(char)
        current = "".join(next_str)
    return current

def draw_l_system(instructions, angle, step, start_pos=(0,0), start_angle=90, savefile=None):
    """
    根据L-System指令绘图
    :param instructions: 指令字符串（如"F+F--F+F"）
    :param angle: 每次转向的角度（度）
    :param step: 每步前进的长度
    :param start_pos: 起始坐标 (x, y)
    :param start_angle: 起始角度（0表示向右，90表示向上）
    :param savefile: 若指定则保存为图片文件，否则直接显示
    """
    pos_stack = []
    x, y = start_pos
    current_angle = start_angle
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    for cmd in instructions:
        if cmd == 'F' or cmd == '0' or cmd == '1':  # 向前绘制
            rad = math.radians(current_angle)
            nx = x + step * math.cos(rad)
            ny = y + step * math.sin(rad)
            ax.plot([x, nx], [y, ny], 'k-', lw=1)
            x, y = nx, ny
        elif cmd == '+':  # 左转
            current_angle += angle
        elif cmd == '-':  # 右转
            current_angle -= angle
        elif cmd == '[':  # 压栈（保存状态）
            pos_stack.append((x, y, current_angle))
            current_angle += angle  # 对于树规则，压栈时左转
        elif cmd == ']':  # 出栈（恢复状态）
            if pos_stack:
                x, y, current_angle = pos_stack.pop()
                current_angle -= angle  # 对于树规则，出栈时右转
    
    ax.set_aspect('equal')
    ax.axis('off')
    if savefile:
        plt.savefig(savefile, bbox_inches='tight', dpi=150)
    plt.show()

if __name__ == "__main__":
    # 1. 生成并绘制科赫曲线
    axiom = "F"  # 公理
    rules = {"F": "F+F--F+F"}  # 规则
    iterations = 4  # 迭代次数
    angle = 60  # 每次转角
    step = 5  # 步长
    instr = apply_rules(axiom, rules, iterations)  # 生成指令字符串
    draw_l_system(instr, angle, step, start_pos=(0, 0), savefile="l_system_koch.png")  # 绘图并保存

    # 2. 生成并绘制分形二叉树
    axiom = "0"
    rules = {"1": "11", "0": "1[0]0"}
    iterations = 6
    angle = 45
    step = 3
    instr = apply_rules(axiom, rules, iterations)
    draw_l_system(instr, angle, step, start_pos=(0, -100), savefile="fractal_tree.png")
