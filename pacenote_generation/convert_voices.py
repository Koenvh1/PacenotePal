import os


for voice in os.listdir("../voices"):
    for file in os.listdir("voices/" + voice):
        os.makedirs(f"voices2\\{voice}", exist_ok=True)
        print(voice, file)
        os.system(f"ffmpeg -i \"voices\\{voice}\\{file}\" -acodec pcm_s16le -ac 1 -ar 44100 \"voices2\\{voice}\\{file}\"")