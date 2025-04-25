import numpy as np
import matplotlib.pyplot as plt
import random

def get_fern_params():
    """返回巴恩斯利蕨的IFS参数"""
    return [
        [0.00, 0.00, 0.00, 0.16, 0.00, 0.00, 0.01],   # 茎干
        [0.85, 0.04, -0.04, 0.85, 0.00, 1.60, 0.85],  # 主叶
        [0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07],  # 左叶
        [-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07]   # 右叶
    ]

def get_tree_params():
    """返回概率树的IFS参数"""
    return [
        [0.00, 0.00, 0.00, 0.50, 0.00, 0.00, 0.10],   # 树干
        [0.42, -0.42, 0.42, 0.42, 0.00, 0.20, 0.45],  # 左枝
        [0.42, 0.42, -0.42, 0.42, 0.00, 0.20, 0.45]   # 右枝
    ]

def apply_transform(point, params):
    """应用仿射变换到点"""
    x, y = point
    a, b, c, d, e, f, _ = params
    x_new = a * x + b * y + e
    y_new = c * x + d * y + f
    return (x_new, y_new)

def run_ifs(ifs_params, num_points=50000, num_skip=100):
    """运行IFS迭代生成点集"""
    # 初始化点和坐标列表
    x, y = 0, 0
    x_coords = []
    y_coords = []
    
    # 提取变换参数和概率
    transforms = [t[:6] for t in ifs_params]
    probs = [t[6] for t in ifs_params]
    
    # 混沌游戏迭代
    for i in range(num_points + num_skip):
        # 随机选择变换
        chosen_idx = random.choices(range(len(ifs_params)), weights=probs)[0]
        x, y = apply_transform((x, y), ifs_params[chosen_idx])
        
        # 跳过初始不稳定点
        if i >= num_skip:
            x_coords.append(x)
            y_coords.append(y)
    
    return np.array(x_coords), np.array(y_coords)

def plot_ifs(x, y, title="IFS Fractal", filename=None):
    """绘制IFS分形"""
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=0.1, c='green', alpha=0.6, marker='o', linewidths=0)
    plt.title(title, fontsize=12)
    plt.axis('equal')
    plt.axis('off')
    
    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()

if __name__ == "__main__":
    # 生成并绘制巴恩斯利蕨
    print("生成巴恩斯利蕨...")
    fern_x, fern_y = run_ifs(get_fern_params(), num_points=50000)
    plot_ifs(fern_x, fern_y, "Barnsley Fern", "barnsley_fern.png")
    
    # 生成并绘制概率树
    print("生成概率树...")
    tree_x, tree_y = run_ifs(get_tree_params(), num_points=30000)
    plot_ifs(tree_x, tree_y, "Probability Tree", "probability_tree.png")
