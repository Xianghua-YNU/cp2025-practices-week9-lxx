import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def load_and_binarize_image(image_path, threshold=128):
    """
    加载图像并转换为二值数组
    
    参数：
    image_path -- 图像文件路径（字符串）
    threshold -- 二值化阈值（0-255之间的整数，默认128）
    
    返回：
    二值化的NumPy数组（0和1组成）
    """
    # 打开图像并转换为灰度
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    # 二值化处理
    binary_array = (img_array > threshold).astype(np.uint8)
    return binary_array

def box_count(binary_image, box_sizes):
    """
    盒计数算法实现
    
    参数：
    binary_image -- 二值图像数组（0和1组成的NumPy数组）
    box_sizes -- 盒子尺寸列表（整数列表）
    
    返回：
    字典 {box_size: count}，记录每个盒子尺寸对应的非空盒子数量
    """
    height, width = binary_image.shape
    counts = {}
    
    for box_size in box_sizes:
        # 计算网格行列数
        rows = height // box_size
        cols = width // box_size
        
        # 如果图像尺寸不是盒子尺寸的整数倍，调整边界
        if height % box_size != 0:
            rows += 1
        if width % box_size != 0:
            cols += 1
            
        count = 0
        
        # 遍历所有盒子区域
        for i in range(rows):
            for j in range(cols):
                # 计算当前盒子边界
                y_start = i * box_size
                y_end = min((i + 1) * box_size, height)
                x_start = j * box_size
                x_end = min((j + 1) * box_size, width)
                
                # 检查盒子内是否有前景像素
                if np.any(binary_image[y_start:y_end, x_start:x_end] == 1):
                    count += 1
                    
        counts[box_size] = count
        
    return counts

def calculate_fractal_dimension(binary_image, min_box_size=1, max_box_size=None, num_sizes=10):
    """
    计算分形维数
    
    参数：
    binary_image -- 二值图像数组
    min_box_size -- 最小盒子尺寸（默认1）
    max_box_size -- 最大盒子尺寸（默认图像最小尺寸的一半）
    num_sizes -- 盒子尺寸数量（默认10）
    
    返回：
    盒维数D, 元组(epsilons, N_epsilons, slope, intercept)
    """
    height, width = binary_image.shape
    
    # 设置最大盒子尺寸
    if max_box_size is None:
        max_box_size = min(height, width) // 2
        
    # 生成等比数列的盒子尺寸
    box_sizes = np.unique(np.logspace(
        np.log2(min_box_size),
        np.log2(max_box_size),
        num=num_sizes,
        base=2,
        dtype=int
    ))
    
    # 确保盒子尺寸至少为1且唯一
    box_sizes = np.unique(np.clip(box_sizes, 1, max_box_size))
    
    # 执行盒计数
    counts = box_count(binary_image, box_sizes)
    
    # 提取结果
    epsilons = np.array(list(counts.keys()))
    N_epsilons = np.array(list(counts.values()))
    
    # 对数变换
    log_eps = np.log(epsilons)
    log_N = np.log(N_epsilons)
    
    # 线性回归
    slope, intercept = np.polyfit(log_eps, log_N, 1)
    
    # 盒维数D是斜率的相反数
    D = -slope
    
    return D, (epsilons, N_epsilons, slope, intercept)

def plot_log_log(epsilons, N_epsilons, slope, intercept, save_path=None):
    """
    绘制log-log图
    
    参数：
    epsilons -- 盒子尺寸列表
    N_epsilons -- 对应的盒子计数列表
    slope -- 拟合直线斜率
    intercept -- 拟合直线截距
    save_path -- 图片保存路径（可选）
    """
    plt.figure(figsize=(8, 6))
    
    # 对数变换
    log_eps = np.log(epsilons)
    log_N = np.log(N_epsilons)
    
    # 绘制散点图
    plt.scatter(log_eps, log_N, color='blue', label='Data points')
    
    # 绘制拟合直线
    x = np.linspace(min(log_eps), max(log_eps), 100)
    y = slope * x + intercept
    plt.plot(x, y, 'r-', label=f'Fit line (D={-slope:.3f})')
    
    # 添加标签和图例
    plt.xlabel('log(ε)')
    plt.ylabel('log(N(ε))')
    plt.title('Box Counting Method - log-log Plot')
    plt.legend()
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=150)
    
    plt.show()

if __name__ == "__main__":
    # 示例路径，请根据实际情况修改
    IMAGE_PATH = "barnsley_fern.png"  
    
    try:
        # 1. 加载并二值化图像
        binary_img = load_and_binarize_image(IMAGE_PATH)
        
        # 2. 计算分形维数
        D, results = calculate_fractal_dimension(binary_img)
        
        # 3. 输出结果
        print("盒计数结果:")
        epsilons, N_epsilons, slope, intercept = results
        for eps, N in zip(epsilons, N_epsilons):
            print(f"ε={eps:3d}, N(ε)={N:5d}, log(ε)={np.log(eps):.3f}, log(N)={np.log(N):.3f}")
        
        print(f"\n估算的盒维数 D = {D:.5f}")
        
        # 4. 绘制log-log图
        plot_log_log(*results, "log_log_plot.png")
        
    except FileNotFoundError:
        print(f"错误：找不到图像文件 '{IMAGE_PATH}'")
        print("请确保图像文件存在或修改IMAGE_PATH变量")
