import simpleaudio as sa
import time
import librosa

FILEPATH = "/Users/josef.haeusel/My Drive/Musikdesign/HKU/Unterricht/Python/CSD2_git/CSD2a/opdrachten/python_basics/toycar.wav"   

def errorFunctionNumber(number, check_int = True, check_positive = True):
    
    if check_positive and number <= 0:
        print(f"ERROR: Number has to be positive")
        return "Error"

##Try Catch      

def inputNoteDurations():
    while True:
      numPlaybackTimes = int(input("How often do you want the sample to play (int)?   "))
      if errorFunctionNumber(numPlaybackTimes, check_positive=True) == "Error":
         continue
      else:
         break

    print("\n0.25 = Sixteenth Note, 1 = Quarter Note, 2 = Half Note,... ")
    noteDurations = []
    for x in range(numPlaybackTimes):
        duration = float(input(f"How long is note {x+1} out of {numPlaybackTimes}?    "))
        noteDurations.append(duration)
        print("-> Your rhythm: ", noteDurations)
    return noteDurations

def durationsToSixteenthTimestamps(noteDurations):
  timestamps = [0]
  for note_length in noteDurations:
    sixteenth = note_length * 4
    timestamps.append(sixteenth + timestamps[-1])
  timestamps.pop()
  return timestamps

def sixteenthTimestampsToSecondTimestamps(sixteenthTimestamps, bpm):
  timestamps = []
  for timestamp in sixteenthTimestamps:
    timestamp = timestamp/4*(60/bpm)
    timestamps.append(timestamp)
  return timestamps

def input_bpm(default_bpm):
  bpm_input = input(f"Set BPM or press Enter for default ({default_bpm:.2f} BPM):   ")

  if bpm_input == "":
    return default_bpm
  else:
    while float(bpm_input) <= 0:
      print("\nError: BPM has to be above 0\n")
      bpm_input = float(input("Set BPM: "))
    return float(bpm_input)

def playbackTimestamps(timestampsSeconds, filepath):

    y, sr = librosa.load(filepath)
    sample_duration = librosa.get_duration(y=y, sr=sr)
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    start_time = time.time()

    for note, timestamp in enumerate(timestampsSeconds):

        elapsed_time = time.time() - start_time
        if elapsed_time < timestamp:
            time.sleep(timestamp - elapsed_time)
            elapsed_time = time.time() - start_time

        print(f"Playing note {note+1}. Elapsed time: {elapsed_time}")

        if note+1 < len(timestampsSeconds):
        
            play_obj = wave_obj.play()

        else:
            play_obj = wave_obj.play()
            time.sleep(sample_duration)

    print("\nPlayback finished.\n")



###Ciskas Solution with while Loop.
def playbackTimestamps2(timestampsSeconds, filepath):

    print("\n\nTIMESTAMPS", timestampsSeconds, "\n\n")
    y, sr = librosa.load(filepath)
    sample_duration = librosa.get_duration(y=y, sr=sr)
    wave_obj = sa.WaveObject.from_wave_file(filepath)


    if timestampsSeconds:
      timestamp = timestampsSeconds.pop(0)
    else:
       exit()

    start_time = time.time()
    is_playing = True
    while is_playing:
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= timestamp:
          play_obj = wave_obj.play()
          print(f"Playing note at {timestamp} in BPM. Elapsed time: {elapsed_time}")
          print(timestampsSeconds)
          timestampsSeconds.pop(0)
        else:
           time.sleep(0.0001)
        
        if len(timestampsSeconds) == 1:
          play_obj = wave_obj.play()
          time.sleep(sample_duration)
        

          

    print("\nPlayback finished.\n")


def main():
  noteDurations = inputNoteDurations()
  bpm = input_bpm(default_bpm=60)
  timestamps16th = durationsToSixteenthTimestamps(noteDurations)
  timestampsSeconds = sixteenthTimestampsToSecondTimestamps(timestamps16th, bpm)
  playbackTimestamps(timestampsSeconds, FILEPATH)

if __name__ == "__main__":
  main()


