import os
import time

original = open(f"pacenotes_combined_english_orig.tsv", encoding="utf-8")
data = open(f"pacenotes_combined_english.tsv", encoding="utf-8")


def to_dict(tsv):
    d = {}
    for line in tsv:
        line = line.strip()
        key, value = line.split("\t", 1)
        d[key] = value
    return d


original = to_dict(original)
data = to_dict(data)

from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-GB", name="en-GB-Wavenet-F"
)

# Set the text input to be synthesized
item_count = len(data.items())
i = 1

for key, value in data.items():
    print(i, item_count)
    if key in original and original[key] == value:
        print("skip")
        continue

    synthesis_input = texttospeech.SynthesisInput(ssml=value)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1.2, pitch=-4
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(f"../voices/English Woman/{key}.wav", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(key)

    i += 1
    time.sleep(0.5)

