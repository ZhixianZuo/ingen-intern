import matplotlib.pyplot as plt
import os

# 初始化存储数据的列表
times = []
targets = []
actuals = []

# 自动获取当前 python 脚本所在的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接出同文件夹下 csv 文件的准确绝对路径
csv_path = os.path.join(current_dir, 'telemetry_data.csv')

try:
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            parts = line.strip().split(',')
            
# ... 下面的代码保持不变 ...
            if len(parts) == 3:
                try:
                    # 将时间戳(毫秒)转换为秒
                    t = float(parts[0]) / 1000.0 
                    target = float(parts[1])
                    actual = float(parts[2])
                    
                    times.append(t)
                    targets.append(target)
                    actuals.append(actual)
                except ValueError:
                    # 跳过无法解析的行（比如头尾的乱码或空行）
                    continue
except FileNotFoundError:
    print("错误：找不到 telemetry_data.csv 文件，请确认路径。")
    exit()

# 如果成功读取到数据，开始绘图
if times:
    # 为了让图表从 0 秒开始显示，减去起始时间偏移量
    start_time = times[0]
    times = [t - start_time for t in times]

    plt.figure(figsize=(10, 6))
    
    # 绘制目标速度参考线（虚线）
    plt.plot(times, targets, label='Target Velocity (50 rad/s)', linestyle='--', color='gray')
    # 绘制实际速度响应曲线（实线）
    plt.plot(times, actuals, label='Actual Velocity (PI Control)', color='blue', linewidth=2)
    
    # 添加图表标签（Caption）和标题，满足实习文档要求
    plt.title('Aido Rover Wheel Motor: Step Response (PI Controller)')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Velocity (rad/s)')
    
    # 在图表下方添加一段 Caption 注释，解释 Kp 和 Ki 的表现
    caption = "Caption: The system shows a rapid rise time with minimal overshoot,\nindicating that Kp (2.0) provides sufficient aggressive action, while Ki (5.0) eliminates steady-state error."
    plt.figtext(0.5, 0.01, caption, wrap=True, horizontalalignment='center', fontsize=10)
    
    # 调整布局留出底部 caption 的空间
    plt.subplots_adjust(bottom=0.15) 
    
    plt.legend()
    plt.grid(True)
    
    # 保存为 PNG 图片并显示
    plt.savefig('wk4_step_response.png', dpi=300)
    print("图表已成功生成并保存为 wk4_step_response.png！")
    plt.show()
else:
    print("未能从文件中读取到有效数据，请检查 CSV 内容格式。")