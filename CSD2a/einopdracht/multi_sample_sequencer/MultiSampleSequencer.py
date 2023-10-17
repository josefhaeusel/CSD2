import simpleaudio as sa
import pathlib
import time
import datetime
import multiprocessing
from midi_writer import MIDIFile

##    Global Variables
DIR_PATH = pathlib.Path(__file__).parent.resolve()
SAMPLES_DICT = {
   1: sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/toyhit.wav"),
   2: sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/toycar.wav"),
   3: sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/toytrain.wav")
}

"""
DESCRIPTION
-----------------------

Prompts the user (terminal) to create multiple rhythmical sequences, to be played back simultaneously through multiprocessing.

The created sequences be saved as individual one-track MIDI Files.


"""



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

def inputNumSequences(default_num = 3):
  
  """
  Asks the user to input the number of sequences to enter, to be played back simultaneously. If input is empty, a default value (arg1) is used.
  
  """

  if type(default_num) != int:
     raise ValueError("default_times (arg1) has to be an integer")

  while True:

    numSequences_input = input(f"\nHow many sequences do you want to enter, to be played back simultaneously? Press Enter for default (= {default_num}):   \n")
    if numSequences_input == "":
      return default_num
    
    if errorFunction(numSequences_input, checkPositive=True, checkInt=True) == "Error":
       continue
    else:
       return int(numSequences_input)

def inputNoteDurations():
    
    """
    Asks the user to input a sequence of note durations.

    Note durations: 0.25 = 16th, 0.5 = 8th, 1 = Quarter, ...
    
    """

    while True:
      numPlaybackTimes = input("How many notes does your sequence have (int)?   ")
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
        print("-> Your rhythm: \n", noteDurations)
      
    return noteDurations

def inputLooptimes(default_times = 4):

  """
  Asks the user to input the number of loops to play back a sequence. If input is empty, a default value (arg1) is used.
  
  """
  if type(default_times) != int:
     raise ValueError("default_times (arg1) has to be an integer")

  while True:

    looptimes_input = input(f"\nSet number of loops or press Enter for default (= {default_times} loops):   \n")
    if looptimes_input == "":
      return default_times
    
    if errorFunction(looptimes_input, checkPositive=True, checkInt=True) == "Error":
       continue
    else:
       return int(looptimes_input)

def inputBpm(default_bpm = 60):
  
  """
  Asks the user to input a BPM number. If input is empty, a default bpm (arg1) is used.
  
  """

  while True:

    bpm_input = input(f"\nSet BPM or press Enter for default ({default_bpm:.2f} BPM):   \n")
    if bpm_input == "":
      return default_bpm
    
    if errorFunction(bpm_input, checkPositive=True) == "Error":
       continue
    else:
       return float(bpm_input)  

def inputInstrumentation(sequence, samples_dict):
    
    """
    Ask user to input a list of instrumentation indexes corresponding to a given sequence.
    
    """

    if type(sequence) != list:
       raise ValueError("Input sequence (arg1) has to be a list.")

    instrumentationList = []
    for note, timestamp in enumerate(sequence):
      
      while True:
        print(f"\nWhat instrument plays the {note+1}. note [{timestamp}] of sequence {sequence}?")
        instrument_index = input(f"Input Number (1 = Toyhit, 2 = Toycar, 3 = Toytrain):\n")

        if errorFunction(instrument_index, checkInt=True, checkPositive=True) == "Error":
          continue
        
        if int(instrument_index) > len(samples_dict):
           print(f"ERROR: Maximum Input Number is {len(samples_dict)}.")
           continue
        
        else:
            instrument_index = int(instrument_index)
            break

      instrumentationList.append(instrument_index)
      print("-> Your Instrumentation: \n", instrumentationList)

    return(instrumentationList)

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

def multiprocessEventHandler(event_lists, loop_times_lists, samples_dict, sequenceIndex = 1):
    
    """
    Takes a list of event_lists (arg1) and loop_times (arg2) as input and plays back the one indicated by sequenceIndex (arg4, starts at 1)
    with event_list keys 'timestamp' and 'instrument'. Suited for Multiprocessing application.
    Samples_dict provides simpleaudio-based WaveObjects (indeced from 0 to number of instruments).

    """

    if sequenceIndex < 0:
       raise ValueError("sequenceIndexes start at 0")
    
    if type(event_lists) != list:
       raise ValueError("First argument has to be a list of event lists, even if it's one event list.")
    
    if type(loop_times_lists) != list:
       raise ValueError("Second argument has to be a list of integers.")
    
    if len(event_lists) != len(loop_times_lists):
       raise ValueError("event_lists and loop_times_lists must have the same length.")
    

    event_list = event_lists[sequenceIndex]
    num_loops = loop_times_lists[sequenceIndex]
    length_loop = len(event_list)/num_loops
    start_time = time.time()

    for n, event in enumerate(event_list):

      current_event = int((n%length_loop)+1)
      elapsed_time = time.time() - start_time

      if elapsed_time < event['timestamp']:
          time.sleep(event['timestamp'] - elapsed_time)
          elapsed_time = time.time() - start_time

      print(f"Sequence {sequenceIndex+1}    Playing Event: {current_event:03}.      Instrument: {event['instrument']:02}.      Elapsed time: {elapsed_time:.3f}")
      play_obj = samples_dict[event['instrument']].play()

      if n+1 == len(event_list):
          play_obj.wait_done()

    print(f"\nSequence {sequenceIndex+1}:   Playback finished.\n")

def createSequences():

  """
  Calls several input functions, that prompt user to design rhythmical sequences.
  Processes noteDurations into timestamps based on bpm.
  Creates event lists with keys for 'timestamp' and 'instrument'.
  Returns list of event-lists and loop-times.

  """

  sequencesEventLists = []
  sequencesLoopTimes = []

  numSequences = inputNumSequences(default_num=3)
  
  for sequence in range(numSequences):
    print(f"\nCreating {sequence+1}. of {numSequences} Sequences:\n")

    noteDurations = inputNoteDurations()
    instrumentationList = inputInstrumentation(noteDurations, SAMPLES_DICT)

    loopTimes = inputLooptimes(default_times = 4)
    noteDurations *= loopTimes
    instrumentationList *= loopTimes

    bpm = inputBpm(default_bpm=60)

    timestamps16th = durationsToSixteenthTimestamps(noteDurations)
    timestampsSeconds = sixteenthTimestampsToSecondTimestamps(timestamps16th, bpm)

    eventList = makeEventList(timestampsSeconds, instrumentationList)
    sequencesEventLists.append(eventList)
    sequencesLoopTimes.append(loopTimes)

    print(f"\nFinished creating {sequence+1}. of {numSequences} Sequences.\n")
  
  return sequencesEventLists, sequencesLoopTimes

def multiprocessingSequencePlayback(sequencesEventLists, sequencesLoopTimes, samples_dict):

  """
  Initializes multiprocessEventHandler() processes based on the number of input sequences.
  
  """

  numSequences = len(sequencesLoopTimes)
  processes = []

  for process_num in range(numSequences):
      process = multiprocessing.Process(target=multiprocessEventHandler, args=(sequencesEventLists, sequencesLoopTimes, samples_dict, process_num))
      processes.append(process)

  print(f"\nMultiprocessing Playback started.\n")

  for process in processes:
      process.start()

  for process in processes:
      process.join()

def MIDI_Writer(sequencesEventLists):

   """
   Creates MIDI Files out of a list of sequences. Saves them as individual tracks / files.
   Returns True / False message, conditioning the continuation of the loop of further sequence creation.
   
   """

   prompt = input("\nDo you want to save these sequences as MIDI files? [Y / N]\n")

   if prompt in "Nn":
      prompt = input("\nDo you want to create new sequences? [Y / N]\n")
      if prompt in "Nn":
         print("\nYou don't know, what you are missing.\n")
         return False
      if prompt in "Yy":
         return True
   
   if prompt in "Yy":
      
      #Unique Filenaming
      current_time = datetime.datetime.now()
      filetag = current_time.strftime("%Y-%m-%d %H:%M:%S")
      midi_directory = f"{DIR_PATH}/MIDI_sequences/"

      for i, sequence in enumerate(sequencesEventLists):

         midiFile = MIDIFile(1)
         midiFile.add_tempo(track = 0, tempo = 60, time = 0)
         midi_filepath = midi_directory + f"sequence_{filetag}_track{i}.mid"
         
         for event in sequence:
            time = event['timestamp']
            note = event['instrument'] + 52
            midiFile.add_note(track = 0, channel = 9, pitch = note, time = time, duration = 0.5, volume = 70)
         
         with open(midi_filepath, "wb") as output_file:
            midiFile.write_file(output_file)

      print(f"\nSaved {len(sequencesEventLists)} MIDI Files successfully!\nDirectory: {midi_directory}")

      prompt = input("\nDo you want to create more sequences? [Y / N]\n")
      if prompt in "Nn":
         print("\nAlright, then have fun with your sequences! Goodbye.\n")
         return False
      if prompt in "Yy":
         return True


if __name__ == "__main__":
  
   while True: 
      sequencesEventLists, sequencesLoopTimes = createSequences()
      multiprocessingSequencePlayback(sequencesEventLists, sequencesLoopTimes, SAMPLES_DICT)
      continue_feedback = MIDI_Writer(sequencesEventLists)
      
      if continue_feedback:
         continue
      else:
         break








