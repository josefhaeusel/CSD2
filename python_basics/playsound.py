import simpleaudio as sa

filepath = input("input path to .wav file")
wave_obj = sa.WaveObject.from_wave_file(filepath)
play_obj = wave_obj.play()
play_obj.wait_done()

n_times = int(input("How often do you want the file to play (int)?"))

for x in range(n_times):
    play_obj.wait_done()