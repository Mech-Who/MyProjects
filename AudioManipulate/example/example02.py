"""
Python音频模块
Python中提供了多个音频处理模块，如pydub、scipy等。
其中，pydub是一个高级音频处理库，支持大多数常见格式的音频文件，
并且可以进行音频处理、剪辑、合并等操作。
scipy则是一个Python科学计算库，提供丰富的信号处理功能。
"""
from pydub import AudioSegment
from scipy.io import wavfile

# 读取音频文件
sound = AudioSegment.from_mp3("sample.mp3")

# 导出音频文件
sound.export("sample.wav", format="wav")

# 音频采样率与数据
sample_rate, data = wavfile.read("sample.wav")
