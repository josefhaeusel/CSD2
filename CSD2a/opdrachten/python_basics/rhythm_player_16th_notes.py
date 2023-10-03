import simpleaudio as sa
import time

FILEPATH = "/Users/josef.haeusel/My Drive/Musikdesign/HKU/Unterricht/Python/CSD2_git/CSD2a/opdrachten/python_basics/toycar.wav"   

def errorFunction(number, checkPositive=False, checkInt=False):
    """
    Checks whether a given number is a valid number, positive and / or integer and returns an "Error" message if not.

    """

    # Attempt to convert the input to a float
    try:
        number = float(number)
    except ValueError:
        print("\nERROR: Invalid input. Please enter a valid number.\n")
        return "Error"

    if checkPositive and number <= 0:
        print("\nERROR: Number has to be positive\n")
        return "Error"

    if checkInt and not number.is_integer():
        print("\nERROR: Number has to be an integer\n")
        return "Error"

    return number

def inputNoteDurations():
    
    """
    Asks the user to input a sequence of note durations.

    Note durations: 0.25 = 16th, 0.5 = 8th, 1 = Quarter, ...
    
    """

    while True:
      numPlaybackTimes = input("How often do you want the sample to play (int)?   ")
      if errorFunction(numPlaybackTimes, checkPositive=True, checkInt=True) == "Error":
         continue
      else:
         numPlaybackTimes = int(numPlaybackTimes)
         break

    print("\n0.25 = Sixteenth Note, 1 = Quarter Note, 2 = Half Note,... ")
    noteDurations = []
    for x in range(numPlaybackTimes):
        
        while True:
          duration = input(f"How long is note {x+1} out of {numPlaybackTimes}?    ")
          if errorFunction(duration, checkPositive=True) == "Error":
            continue
          else:
             duration = int(duration)
             break

        noteDurations.append(duration)
        print("-> Your rhythm: ", noteDurations)
      
    return noteDurations

def durationsToSixteenthTimestamps(noteDurations):
  
  """
  Formats a list of single note durations into a list of sequential timestamps.

  Note durations (arg1): 0.25 = 16th, 0.5 = 8th, 1 = Quarter, ...
  Example input: [0.25, 1, 0.5. 0.75, ...]
  
  """
  
  timestamps = [0]
  for note_length in noteDurations:
    sixteenth = note_length * 4
    timestamps.append(sixteenth + timestamps[-1])
  timestamps.pop()
  return timestamps

def sixteenthTimestampsToSecondTimestamps(sixteenthTimestamps, bpm):
  
  """
  Converts a given list of note duration timestamps (arg1) into a seconds, based on the provided BPM (arg2).

  Note durations (arg1): 0.25 = 16th, 0.5 = 8th, 1 = Quarter, ...
  Example input: [0.25, 0.75, 1, 1.75, 2, ...]
  
  """
  
  timestamps = []
  for timestamp in sixteenthTimestamps:
    timestamp = timestamp/4*(60/bpm)
    timestamps.append(timestamp)
  return timestamps

def input_bpm(default_bpm):
  
  """
  Asks the user to input a BPM. If input is empty, a default bpm (arg1) is used.
  
  """
  while True:

    bpm_input = input(f"Set BPM or press Enter for default ({default_bpm:.2f} BPM):   \n")
    if bpm_input == "":
      return default_bpm
    
    if errorFunction(bpm_input, checkPositive=True) == "Error":
       continue
    else:
       return float(bpm_input)
    
    

def playbackTimestamps(sample_path, timestampsSeconds):

    """
    Plays a given sample (arg1) in a rhythm-sequence according to a timestamp list in seconds (arg2).
    
    """

    wave_obj = sa.WaveObject.from_wave_file(sample_path)
    start_time = time.time()

    for note, timestamp in enumerate(timestampsSeconds):

        elapsed_time = time.time() - start_time

        if elapsed_time < timestamp:
            time.sleep(timestamp - elapsed_time)
            elapsed_time = time.time() - start_time

        print(f"Playing note {note+1}. Elapsed time: {elapsed_time:.3f}")
        play_obj = wave_obj.play()

        if note+1 == len(timestampsSeconds):
            play_obj.wait_done()

    print("\nPlayback finished.\n")



def main():
  noteDurations = inputNoteDurations()
  bpm = input_bpm(default_bpm=60)
  timestamps16th = durationsToSixteenthTimestamps(noteDurations)
  timestampsSeconds = sixteenthTimestampsToSecondTimestamps(timestamps16th, bpm)
  playbackTimestamps(FILEPATH,timestampsSeconds)

if __name__ == "__main__":
  main()


