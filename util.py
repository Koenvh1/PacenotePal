import io
import os
import sys
import wave

import pyaudio


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def open_stream(audio_bytes):
    if type(audio_bytes) is bytes:
        audio_bytes = io.BytesIO(audio_bytes)
    with wave.open(audio_bytes, "rb") as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        return p, stream


def play_audio(stream, audio_bytes):
    if type(audio_bytes) is bytes:
        audio_bytes = io.BytesIO(audio_bytes)
    with wave.open(audio_bytes, "rb") as wf:
        stream.write(wf.readframes(wf.getnframes()), wf.getnframes())


def play_beep():
    with open(str(resource_path("beep.wav")), "rb") as f:
        data = f.read()
        p, stream = open_stream(data)
        play_audio(stream, data)
        stream.close()
        p.terminate()


def initialise_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(1),
                    channels=2,
                    rate=44100,
                    output=True)
    stream.close()
    p.terminate()