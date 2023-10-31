import pyaudio
import wave
from tqdm import tqdm
import time
import pprint
import os
import shutil

p = pyaudio.PyAudio()
device_count = p.get_device_count()
device_infos = []
for i in range(device_count):
    device_info = p.get_device_info_by_index(i)
    device_infos.append((device_info, i))
input_devices = [(item['name'], i) for item, i in device_infos if item['maxInputChannels']>0]
output_devices = [(item['name'], i) for item, i in device_infos if item['maxOutputChannels']>0]
pprint.pprint(input_devices)
pprint.pprint(output_devices)

folder = 'D:/Downloads/TeamSpeek/TeamSpeak_2023-10-21/'
input_file = 'playback_Locier_2023-10-21.wav'
output_file = 'locier_processed.wav'

def record_audio(wave_out_path, record_second, channels):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    if not os.path.exists(wave_out_path):
        with open(wave_out_path, 'w'):
            pass
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("* recording")
    for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()


record_audio(output_file, 5, 1)


def play_audio(wave_path):
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # read data
    data = wf.readframes(CHUNK)
    # play stream (3)
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()


def play_audio_callback(wave_path):
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()

