# Autio file format
# .mp3
# .wav
# .flac
import wave

# Audio signal parameters:
# - number of channels: số lượng kênh (1 hoặc 2) 1 là đơn âm và 2 là âm thanh nổi. mang đến âm thanh từ 2 hướng
# - sample width: byte có mỗi mẫu
# - framerate / sample_rate: tốc độ mẫu, tần số mẫu (44.100Hz)
# - number of frames: tổng số mẫu nhận được
# - values of a frame: giá trị cho từng mẫu

obj = wave.open("bangvan.wav", "rb")

print("Number of channels", obj.getnchannels())
print("Sample width", obj.getsampwidth())
print("Frame rate", obj.getframerate())
print("Number of frames", obj.getnframes())
print("Parameters", obj.getparams())

t_audio = obj.getnframes() / obj.getframerate()

print(t_audio)

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames) / 2)

obj.close()

obj_new = wave.open("bangvan_new.wav", "wb")

obj_new.setnchannels(2)
obj_new.setsampwidth(2)
obj_new.setframerate(48000.0)

obj_new.writeframes(frames)

obj_new.close()