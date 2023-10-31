"""
Python语音去噪是一种目前比较流行的声音处理技术，
它可以在语音信号中去除噪声，提升语音的信噪比，使语音更加清晰。
在Python中，我们可以使用Librosa库来进行语音去噪。
"""
import librosa
import librosa.display
#加载音频文件
y, sr = librosa.load(r'D:\Downloads\TeamSpeek\TeamSpeak_2023-10-21_21-00-23.223541.wav', sr=44100)
#计算声音的短时傅里叶变换
D = librosa.stft(y)
#计算噪声的能量
noise_power = librosa.core.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr))
#通过软阈值去除噪声
D_noise = librosa.decompose.nn_filter(D, noise_power, hop_length=512, n_fft=2048, win_length=512)
#逆变换，得到去噪后的音频信号
y_noise = librosa.istft(D_noise)
#保存去噪后的音频
librosa.output.write_wav(r'D:\Downloads\TeamSpeek\locier_processed.wav', y_noise, sr)
