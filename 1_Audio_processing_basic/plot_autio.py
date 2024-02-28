import wave
import matplotlib.pyplot as plt
import numpy as np

obj = wave.open("D:\My storage\Desktop\Speech_Recognition\output.wav", "rb")

sample_freq = obj.getframerate()
n_samples = obj.getnframes()
signal_wave = obj.readframes(-1)

obj.close()

if sample_freq is None or n_samples is None or signal_wave is None:
    print("Error obtaining audio properties.")
    exit()

t_audio = n_samples / sample_freq

print(t_audio)

signal_array = np.frombuffer(signal_wave, dtype=np.int32)

if len(signal_array) != n_samples:
    print("Error: Size of signal array does not match the number of frames.")
    exit()

times = np.linspace(0, t_audio, num=n_samples)

plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.ylabel("Signal wave")
plt.xlabel("Time (s)")
plt.xlim(0, t_audio)
plt.show()
