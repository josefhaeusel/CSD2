import simpleaudio as sa
import time

filepath = "/Users/josef.haeusel/My Drive/Musikdesign/HKU/Unterricht/Python/CSD2_git/CSD2a/opdrachten/python_basics/toycar.wav"
wave_obj = sa.WaveObject.from_wave_file(filepath)

numPlaybackTimes = int(input("How often do you want the file to play (int)?\n"))
playback_rhythms = []

for x in range(numPlaybackTimes):
  rhythm_value = float(input("How long is the {}. note of the {}?\n".format(x+1, numPlaybackTimes)))
  playback_rhythms.append(rhythm_value)
  print("-> Your rhythm:\n", playback_rhythms)


def enter_bpm(default_bpm):
  bpm_input = input(f"Set BPM or press Enter for default ({default_bpm:.2f} BPM):\n")
  if bpm_input == "":
    return default_bpm
  else:
    while float(bpm_input) <= 0:
      print("Error: BPM has to be above 0\n")
      bpm_input = float(input("Set BPM:\n"))
    return float(bpm_input)

bpm = enter_bpm(120)

for x in range(numPlaybackTimes):
  print("Playing note {} in {} BPM".format(x+1,bpm))
  play_obj = wave_obj.play()
  time.sleep(playback_rhythms[x]*(60 / bpm))

print("Playback finished\n")

  