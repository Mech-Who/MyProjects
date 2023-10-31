"""
基于滤波器的音频处理
滤波器可用来对音频数据进行降噪、去除杂音等处理。
Python的scipy模块提供了多种滤波器，如Butterworth、Chebyshev等。
"""
from scipy.signal import butter, lfilter

# Butterworth滤波器
low = 500/8000
high = 2000/8000
order = 4
b, a = butter(order, [low, high], btype='band')
filtered = lfilter(b, a, data)
