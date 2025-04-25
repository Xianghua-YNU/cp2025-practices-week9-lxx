import numpy as np
import matplotlib.pyplot as plt

def koch_generator(u, level):
    """
    迭代生成科赫曲线的点序列。
    
    参数:
        u: 初始线段的端点数组（复数表示）
        level: 迭代层数
        
    返回:
        numpy.ndarray: 生成的所有点（复数数组）
    """
    points = u.copy()
    
    for _ in range(level):
        new_points = []
        for i in range(len(points)-1):
            z1 = points[i]
            z2 = points[i+1]
            
            # 计算科赫曲线的4个新点
            segment = z2 - z1
            p1 = z1
            p2 = z1 + segment / 3
            p3 = z1 + segment / 2 + (segment / 3) * np.exp(1j * np.pi/3)
            p4 = z1 + 2 * segment / 3
            p5 = z2
            
            new_points.extend([p1, p2, p3, p4])
        
        new_points.append(points[-1])  # 添加最后一个点
        points = np.array(new_points)
    
    return points

def minkowski_generator(u, level):
    """
    迭代生成闵可夫斯基香肠曲线的点序列。
    
    参数:
        u: 初始线段的端点数组（复数表示）
        level: 迭代层数
        
    返回:
        numpy.ndarray: 生成的所有点（复数数组）
    """
    points = u.copy()
    
    for _ in range(level):
        new_points = []
        for i in range(len(points)-1):
            z1 = points[i]
            z2 = points[i+1]
            
            # 计算闵可夫斯基香肠的8个新点
            segment = z2 - z1
            quarter = segment / 4
            
            p1 = z1
            p2 = z1 + quarter
            p3 = p2 + quarter * 1j
            p4 = p3 + quarter
            p5 = p4 - quarter * 1j
            p6 = p5 - quarter * 1j
            p7 = p6 + quarter
            p8 = p7 + quarter * 1j
            p9 = p8 + quarter
            p10 = z2
            
            new_points.extend([p1, p2, p3, p4, p5, p6, p7, p8, p9])
        
        new_points.append(points[-1])  # 添加最后一个点
        points = np.array(new_points)
    
    return points

if __name__ == "__main__":
    # 初始线段 (复数表示)
    init_u = np.array([0 + 0j, 1 + 0j])
    
    # 绘制不同层级的科赫曲线
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for i in range(4):
        koch_points = koch_generator(init_u, i+1)
        axs[i//2, i%2].plot(
            np.real(koch_points), np.imag(koch_points), 'k-', lw=1
        )
        axs[i//2, i%2].set_title(f"Koch Curve Level {i+1}")
        axs[i//2, i%2].axis('equal')
        axs[i//2, i%2].axis('off')
    plt.tight_layout()
    plt.savefig('koch_curve.png')
    plt.show()
    
    # 绘制不同层级的闵可夫斯基香肠曲线
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for i in range(4):
        minkowski_points = minkowski_generator(init_u, i+1)
        axs[i//2, i%2].plot(
            np.real(minkowski_points), np.imag(minkowski_points), 'k-', lw=1
        )
        axs[i//2, i%2].set_title(f"Minkowski Sausage Level {i+1}")
        axs[i//2, i%2].axis('equal')
        axs[i//2, i%2].axis('off')
    plt.tight_layout()
    plt.savefig('minkowski_sausage.png')
    plt.show()
