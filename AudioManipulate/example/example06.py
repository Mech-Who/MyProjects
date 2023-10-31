"""
基于时域的音频处理
时域分析是指将音频信号的每个样本进行分析处理。
常见的时域分析方法包括均衡器、压缩器、限制器等。
"""
from scipy.signal import medfilt

# 中值滤波器
filtered = medfilt(data, kernel_size=3)

# 调节音量
gain = 0.5
filtered = filtered * gain

# 压缩声音
threshold = 0.5
ratio = 2
for i in range(len(filtered)):
    if filtered[i] > threshold:
        filtered[i] = threshold + (filtered[i] - threshold) / ratio

# 限制最大音量
max_value = np.max(filtered)
if max_value > 32767:
    scale = 32767 / max_value
    filtered = filtered * scale
