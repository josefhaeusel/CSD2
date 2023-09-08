import simpleaudio as sa
import time

filepath = "/Users/josef.haeusel/My Drive/Musikdesign/HKU/Unterricht/Python/CSD2_git/python_basics/toycar.wav"  #OPTIONAL: input("input path of .wav file")
wave_obj = sa.WaveObject.from_wave_file(filepath)

numPlaybackTimes = int(input("How often do you want the file to play (int)?"))
playback_rhythms = []

for x in range(numPlaybackTimes):
    rhythm_value = [float(input("\nHow long is the {}. note of the {}?".format(x+1, numPlaybackTimes)))]
    playback_rhythms = playback_rhythms + rhythm_value
    print("-> Your rhythm:", playback_rhythms)

playback_bpm = 60/int(input("\nAt how many BPM should your rhythm be played?"))

for x in range(numPlaybackTimes):
    play_obj = wave_obj.play()
    time.sleep(playback_rhythms[x]*playback_bpm)