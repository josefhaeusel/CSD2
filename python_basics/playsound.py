import simpleaudio as sa

filepath = "/Users/josef.haeusel/My Drive/Musikdesign/HKU/Unterricht/Python/CSD2_git/python_basics/toycar.wav"  #input("input path of .wav file")
wave_obj = sa.WaveObject.from_wave_file(filepath)
n_times = int(input("How often do you want the file to play (int)?"))

for x in range(n_times):
    play_obj = wave_obj.play()
    play_obj.wait_done()