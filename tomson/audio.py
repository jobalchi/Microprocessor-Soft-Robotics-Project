import wave
import pyaudio

# WAV 파일 열기
wav_file = wave.open('Thomas_ost.wav', 'rb')

# PyAudio 인스턴스 생성
audio = pyaudio.PyAudio()
0
# 스트림 열기
stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                    channels=wav_file.getnchannels(),
                    rate=wav_file.getframerate(),
                    output=True)

# WAV 파일 데이터를 스트림으로 재생
chunk = 1024
data = wav_file.readframes(chunk)

while data:
    stream.write(data)
    data = wav_file.readframes(chunk)

# 스트림과 파일 닫기
stream.stop_stream()
stream.close()
audio.terminate()
wav_file.close()
