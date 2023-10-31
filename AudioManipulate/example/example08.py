import librosa
import scipy.signal as signal
import numpy as np

folder = 'D:/Downloads/TeamSpeek/TeamSpeak_2023-10-21/'
input_file = 'playback_Locier_2023-10-21.wav'
output_file = 'locier_processed.wav'

y, sr = librosa.load(folder + input_file)

def denoise(y):  
    # 计算音频的功率谱  
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y))**2, ref=np.max)  
    # 应用Wiener滤波器进行去噪  
    D_denoised = signal.wiener(D, 511)  
    # 将去噪后的功率谱转换回音频信号  
    y_denoised = librosa.istft(np.exp(librosa.db_to_amplitude(D_denoised)))  
    return y_denoised

y_denoised = denoise(y)

librosa.output.write_wav(folder + output_file, y_denoised, sr)
