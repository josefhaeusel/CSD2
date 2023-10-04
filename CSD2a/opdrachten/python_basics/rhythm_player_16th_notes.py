import simpleaudio as sa
import pathlib
import time

###Global Variables
DIR_PATH = pathlib.Path(__file__).parent.resolve()
SAMPLES_DIR = f'{DIR_PATH}/samples'
SAMPLES_DICT = {
   1: sa.WaveObject.from_wave_file(f"{SAMPLES_DIR}/toyhit.wav"),
   2: sa.WaveObject.from_wave_file(f"{SAMPLES_DIR}/toycar.wav"),
   3: sa.WaveObject.from_wave_file(f"{SAMPLES_DIR}/toytrain.wav")
}

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
             duration = float(duration)
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

def input_bpm(default_bpm = 60):
  
  """
  Asks the user to input a BPM number. If input is empty, a default bpm (arg1) is used.
  
  """
  while True:

    bpm_input = input(f"Set BPM or press Enter for default ({default_bpm:.2f} BPM):   \n")
    if bpm_input == "":
      return default_bpm
    
    if errorFunction(bpm_input, checkPositive=True) == "Error":
       continue
    else:
       return float(bpm_input)  

def inputInstrumentation(timestampsSeconds):
    
    """
    Ask user to input a list of instrumentation indexes corresponding to length of timestamps
    
    """

    instrumentationList = []
    for note, timestamp in enumerate(timestampsSeconds):
      
      while True:
        print(f"What instrument plays the {note+1}. note [{timestamp}] out the sequence {timestampsSeconds}?")
        instrument_index = input(f"Input Number (1 = Toyhit, 2 = Toycar, 3 = Toytrain):\n")
        if errorFunction(instrument_index, checkInt=True) == "Error" :
          continue
        else:
            instrument_index = int(instrument_index)
            break

      instrumentationList.append(instrument_index)
      print("-> Your Instrumentation: ", instrumentationList)

    return(instrumentationList)

def makeEventList(timestampsSeconds, instrumentationList):
   
   """
   Format corresponding lists of timestamps and instruments into a list of events (dicts).
   
   """

   if len(timestampsSeconds) != len(instrumentationList):
      print("The two lists do not have the same length")
      raise ValueError("Lists must have the same length")
   
   event_list = []

   for n in range(len(timestampsSeconds)):
      event = {}
      event['timestamp'] = timestampsSeconds[n]
      event['instrument'] = instrumentationList[n]
      event_list.append(event)
    
   def getTimestamp(event):
      return event['timestamp']
   
   event_list.sort(key=getTimestamp)
   
   return event_list

def inputLooptimes(default_times = 4):

  """
  Asks the user to input the number of loops to play back a sequence. If input is empty, a default value (arg1) is used.
  
  """
  if type(default_times) != int:
     raise ValueError("default_times (arg1) has to be an integer")

  while True:

    looptimes_input = input(f"Set number of loops or press Enter for default (= {default_times} loops):   \n")
    if looptimes_input == "":
      return default_times
    
    if errorFunction(looptimes_input, checkPositive=True, checkInt=True) == "Error":
       continue
    else:
       return int(looptimes_input)

def eventHandler(event_list, samples_dict, num_loops):
   """
   Plays an event_list with keys 'timestamp' and 'instrument'.
   Samples_dict provides simpleaudio-based WaveObjects (indeced from 0 to number of instruments).

   """
   for loop in range(num_loops):

    print(f"\nPlaying loop {loop+1} / {num_loops}.")
    start_time = time.time()

    for n, event in enumerate(event_list):

        elapsed_time = time.time() - start_time

        if elapsed_time < event['timestamp']:
            time.sleep(event['timestamp'] - elapsed_time)
            elapsed_time = time.time() - start_time

        print(f"Playing Event {(n+1):02}.      Instrument: {event['instrument']:02}.      Elapsed time: {elapsed_time:.3f}")
        play_obj = samples_dict[event['instrument']].play()

        if n+1 == len(event_list):
            play_obj.wait_done()

   print("\nPlayback finished.\n")
   

   
def main():
  noteDurations = inputNoteDurations()
  bpm = input_bpm()
  timestamps16th = durationsToSixteenthTimestamps(noteDurations)
  timestampsSeconds = sixteenthTimestampsToSecondTimestamps(timestamps16th, bpm)
  instrumentationList = inputInstrumentation(timestampsSeconds)
  eventList = makeEventList(timestampsSeconds, instrumentationList)
  loopTimes = inputLooptimes(default_times = 4)
  eventHandler(eventList, SAMPLES_DICT, loopTimes)

if __name__ == "__main__":
  main()