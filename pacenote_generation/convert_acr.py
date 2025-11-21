import os
import shutil


base = ''
for file in os.listdir(base):
    if file.endswith("_Any_Any_1.wav"):
        clean_file = file.replace("PN_", "").replace("_Any_Any_1", "")
        shutil.copy2(base + "/" + file, "../voices/English/" + clean_file)
        print(clean_file)

print("Done.")
