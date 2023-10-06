import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import simpleaudio as sa
import pathlib
import time
import multiprocessing

DIR_PATH = pathlib.Path(__file__).parent.resolve()
SAMPLES_DICT = {
   "X": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/low.wav"),
   "Y": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/mid.wav"),
   "Z": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/high.wav")
}

"""

Section 1 - Data Processing of Rossler Attractor
-------------------------------------------------

"""

def rossler_attractor(x, y, z, parameters = {'a': 0.3, 'b': 0.21, 'c': 5}):
    """
    Equations for three-dimensional Rössler Attractor.
    
    """

    a = parameters.get('a')
    b = parameters.get('b')
    c = parameters.get('c')

    x_dot = -y - z
    y_dot = x + a * y
    z_dot = b + z * (x - c)
    return x_dot, y_dot, z_dot

def calculation(rossler_function, start_values = [0.1,0.1,0.1], parameters = {'a': 0.3, 'b': 0.21, 'c': 5}, steps= 10000, step_size = 0.01):
    """
    Calculates a three-dimensional recursive function.
    
    """

    xx = np.empty((steps + 1))
    yy = np.empty((steps + 1))
    zz = np.empty((steps + 1))
    
    xx[0], yy[0], zz[0] = (start_values[0], start_values[1], start_values[2])

    for i in range(steps):
        x_dot, y_dot, z_dot = rossler_function(xx[i], yy[i], zz[i], parameters)
        xx[i + 1] = xx[i] + (x_dot * step_size)
        yy[i + 1] = yy[i] + (y_dot * step_size)
        zz[i + 1] = zz[i] + (z_dot * step_size)

    return xx, yy, zz

def normalizeData(xx, yy, zz):
    """
    Normalizes each axis according to its individual min and max value.
    
    """

    data = [xx, yy, zz]
    normalized_data = []

    # Normalize and scale each axis
    for axis in data:
        min_val = min(axis)
        max_val = max(axis)
        if max_val != min_val:  # Check if max and min are not equal to avoid division by zero
            scaled_axis = [((x - min_val) / (max_val - min_val)) for x in axis]
        else:
            scaled_axis = [0] * len(axis)  # If max and min are equal, set all values to 0
        normalized_data.append(scaled_axis)

    print("\nFinished Normalizing\n")
    return normalized_data[0], normalized_data[1], normalized_data[2]

def plotData(xx, yy, zz, plot_angle=30, min_display = 0, max_display = 1):

    """"
    Plots three-dimensional data (using MatLab.
    
    """

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    plt.gca().patch.set_facecolor('grey')

    ax.plot(xx, yy, zz, '-', color='orange', lw=0.1)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    # Set axis limits based on the min and max values
    ax.set_xlim(min_display, max_display)
    ax.set_ylim(min_display, max_display)
    ax.set_zlim(min_display, max_display)

    # Add ticks for scales
    ax.set_xticks(np.linspace(min_display, max_display, 5))
    ax.set_yticks(np.linspace(min_display, max_display, 5))
    ax.set_zticks(np.linspace(min_display, max_display, 5))

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True)

    ax.view_init(azim=plot_angle)
    plt.ion()
    plt.show()

def DataMain(start_values = [0.1,0.1,0.1], parameters = {'a': 0.3, 'b': 0.21, 'c': 5}, steps= 10000, step_size = 0.01):
    xx, yy, zz = calculation(rossler_attractor, start_values, parameters, steps, step_size)
    
    xx_norm, yy_norm, zz_norm = normalizeData(xx, yy, zz)
    plotData(xx_norm, yy_norm, zz_norm)

    return xx_norm, yy_norm, zz_norm

"""

Section 2 - Sonification of Data
-------------------------------------------------

"""



def DataTresholdConditioning(AxisData, tresholds = [0.5,0.5,0.2]):
    
    rhythmAxisData = []

    for i_axis, axis in enumerate(AxisData):

        treshold = tresholds[i_axis]
        conditioned_axis = []

        for i, val in enumerate(axis):

            if i == 0:
                conditioned_axis.append(0)
                last_val = val

            else:
                if last_val < treshold and val >= treshold or last_val > treshold and val <= treshold:
                    conditioned_axis.append(1)
                else:
                    conditioned_axis.append(0)

                last_val = val

        rhythmAxisData.append(conditioned_axis)
    
    return rhythmAxisData
        

        

""" 
def NotesToTimestamps(steps_per_second, AxisData):

    timestampsAxisList = []

   for axis in AxisData:
        for i, note in enumerate(axis):
            axis[i] = note


        timestampsAxisList.append()"""


def simplePlayback(Axis, samples_dict, AxisIndex = "X", sleep_time = 0.05):

    start_time = time.time()
    sample = samples_dict.get(AxisIndex)
    times_played = 0

    print(f"Playing Axis {AxisIndex}.")

    for n, event in enumerate(Axis):
      
      elapsed_time = time.time() - start_time  
      current_event = int((n)+1)

      #print(f"{AxisIndex} Count  {n}")

      if event == 1:
        times_played = times_played+1
        print(f"Axis {AxisIndex}    Playing Step: {current_event:03}.    Elapsed time: {elapsed_time:.3f}   Times Played: {times_played}")
        play_obj = sample.play()

        if n+1 == len(Axis):
            play_obj.wait_done()
      
      time.sleep(sleep_time)


    print(f"\Axis {AxisIndex}:   Playback finished.\n")


def multiprocessingPlayback(AxisData, TimeSleep):
    """
    Initializes multiprocessEventHandler() processes based on the number of input sequences.
  
    """

    processes = []
    axis_indexes = ["X", "Y", "Z"]

    for i, axis in enumerate(AxisData):
        process = multiprocessing.Process(target=simplePlayback, args=(axis, SAMPLES_DICT, axis_indexes[i], TimeSleep))
        processes.append(process)

    print(f"\nMultiprocessing Playback started.\n")

    for process in processes:
        process.start()

    for process in processes:
        process.join()

def AudioMain(AxisData, TimeSleep):
    rhythmAxisData = DataTresholdConditioning(AxisData)
    multiprocessingPlayback(rhythmAxisData, TimeSleep)



if __name__ == "__main__":
    X_Axis, Y_Axis, Z_Axis   =   DataMain(start_values = [0.1,0.1,0.1],
                              parameters = {'a': 0.31, 'b': 0.18, 'c': 6},
                              steps= 100000, step_size = 0.01 )
    
    AxisData = [X_Axis, Y_Axis, Z_Axis]

    AudioMain(AxisData, 0.001)
    
    

