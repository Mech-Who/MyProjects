"""
基于FFT的频率分析
FFT是傅立叶变换的一种，可将时域信号转换为频域信号。
通过对频域信号进行分析处理，可以用来提取音频中的各种特征，如音高、音量等。
"""
import scipy.fftpack

# 对音频数据进行FFT变换
samples = scipy.fftpack.fft(data)

# 获取FFT变换后的频率和强度
frequencies = scipy.fftpack.fftfreq(len(samples)) * sample_rate
power = np.abs(samples)

# 获取频率和强度最大的值
index = np.argmax(power)
frequency = frequencies[index]
db = 20 * np.log10(power[index])

print("Frequency:", frequency)
print("DB:", db)
