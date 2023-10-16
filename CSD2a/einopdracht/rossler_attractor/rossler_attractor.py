import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import simpleaudio as sa
import pathlib
import time
import multiprocessing


DIR_PATH = pathlib.Path(__file__).parent.resolve()
SAMPLES_DICT = {
   "X": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/bleepC4.wav"),
   "Y": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/hihat.wav"),
   "Z": sa.WaveObject.from_wave_file(f"{DIR_PATH}/samples/kick.wav")
}


"""

DESCRIPTION
----------------

Rhythmical sonification of Rössler Attractor based on Treshold and Gradient Conditioning.

Behold the inquisitive normalization (for the sake of simplicity), altering the 'classical' shape of the attractor.

Plotting realised with Matlab. (Animation work-in-progress; commented out for now)
Credit to Leo Corte's visualization method https://thebrickinthesky.wordpress.com/2013/02/23/maths-with-python-2-rossler-system/

Feel free to experiment with parameters and the twofold sonification methods in the __main__ function.


"""




"""

Section 1 - Data Processing of Rössler Attractor
-------------------------------------------------

"""

def rossler_attractor(x, y, z, parameters = {'a': 0.3, 'b': 0.21, 'c': 5}):

    """
    Equations for calculation of three-dimensional Rössler Attractor.
    
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
    Normalizes each axis according to its (!) individual (!) min and max value.
    
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

def DataMain(start_values = [0.1,0.1,0.1], parameters = {'a': 0.3, 'b': 0.21, 'c': 5}, steps= 10000, step_size = 0.01):

    """
    Initializes the the necessary steps for calculating and preparing the sonification data,
    offering the crucial parameters as arguments.
    
    """

    xx, yy, zz = calculation(rossler_attractor, start_values, parameters, steps, step_size)
    xx_norm, yy_norm, zz_norm = normalizeData(xx, yy, zz)

    return xx_norm, yy_norm, zz_norm



"""

Section 2 - Sonification of Data
-------------------------------------------------

"""


def DataTresholdConditioning(AxisData, tresholds = [0.5, 0.5, 0.2]):

    """
    Creates binary rhythmical data [0,0,1,0,1, ...] based on an axis' positive crossing of a treshold value.

    Each axis can be assigned an individual treshold value in the list of arg2.
    
    """
    
    rhythmAxisData = []

    for i_axis, axis in enumerate(AxisData):

        treshold = tresholds[i_axis]
        conditioned_axis = []

        for i, val in enumerate(axis):

            if i == 0:
                conditioned_axis.append(0)
                last_val = val

            if last_val < treshold and val >= treshold:
                conditioned_axis.append(1)
            else:
                conditioned_axis.append(0)

            last_val = val

        rhythmAxisData.append(conditioned_axis)
    
    return rhythmAxisData

def DataGradientConditioning(AxisData, gradient_tresholds = [0.0, 0.0, 0.0]):

    """
    Creates binary rhythmical data [0,0,1,0,1, ...] based on an axis gradients positive crossing of a treshold value.

    Each axis can be assigned an individual gradient treshold value in the list of arg2.
    
    """
    
    rhythmAxisData = []

    for i_axis, axis in enumerate(AxisData):


        treshold = gradient_tresholds[i_axis]
        conditioned_axis = []

        for i, val in enumerate(axis):
            
            if i == 0:
                conditioned_axis.append(0)
                last_val = 0
                last_gradient = 0
                
            
            gradient = val - last_val

            if last_gradient < treshold and gradient >= treshold:
                conditioned_axis.append(1)
            else:
                conditioned_axis.append(0)

            last_val = val
            last_gradient = gradient

        conditioned_axis

        rhythmAxisData.append(conditioned_axis)
    
    return rhythmAxisData

def BinaryNotesToTimestamps(AxisData, steps_per_second = 3000):

    """
    Created timestamps from binary note list based on a given speed, specified in data "steps-per-second" (arg2). 
    
    """

    timestampsAxisList = []

    for axis in AxisData:
        
        timestamps = [0]
        last_timestamp = (len(axis)-1)*(1/steps_per_second)
        print(last_timestamp)

        for i, note in enumerate(axis):
            time = i*(1/steps_per_second)
            if note == 1:
                timestamps.append(time)
            
            ## Add empty timestamp, to make sure, every axis waits till last step before looping, to stay synchronized
            if i+1 == (len(axis)):
                timestamps.append(last_timestamp)
            

        
        timestamps.pop(0)
        timestampsAxisList.append(timestamps)
    
    return timestampsAxisList

def timestampPlayback(timestampsAxis, samples_dict, AxisIndex = "X", DisplaySign = "+++"):

    """
    Plays back timestamps of an individual axis using the sample (dict in arg2) assigned to the Axisindex (arg3).

    Minimalistic visualizazion in terminal using symbols of arg4.

    Employed in multiprocessing below.

    """

    if AxisIndex == "X":
        displayIndex = f"{DisplaySign}      "
    if AxisIndex == "Y":
        displayIndex = f"   {DisplaySign}   "
    if AxisIndex == "Z":
        displayIndex = f"      {DisplaySign}"

    sample = samples_dict.get(AxisIndex)
    start_time = time.time()
    end_time = timestampsAxis.pop(-1)

    print(f"Playing Axis {AxisIndex}.")

    for n, timestamp in enumerate(timestampsAxis):
    
        elapsed_time = time.time() - start_time
        current_event = int(n+1)

        if elapsed_time < timestamp:
            time.sleep(timestamp - elapsed_time)
            elapsed_time = time.time() - start_time
            print(f"Axis {AxisIndex} {displayIndex}        Playing Note {current_event:04} of {len(timestampsAxis):04}.       Elapsed time: {elapsed_time:.2f}       Latency: {(elapsed_time-timestamp)*1000:.2f} ms")
            play_obj = sample.play()

        if n+1 == len(timestampsAxis) and elapsed_time < end_time:
            time.sleep(end_time - elapsed_time)
            play_obj.wait_done()
    
    elapsed_time = time.time() - start_time
    print(f"\nAxis {AxisIndex}:   Playback finished at {elapsed_time}.\n")
               
def multiprocessingPlayback(AxisData):

    """
    Initializes multiprocessEventHandler() processes based on the number of input sequences.
  
    """

    processes = []
    axis_indexes = ["X", "Y", "Z"]

    for i, axis in enumerate(AxisData):
        process = multiprocessing.Process(target=timestampPlayback, args=(axis, SAMPLES_DICT, axis_indexes[i]))
        processes.append(process)

    print(f"\nMultiprocessing Playback started.\n")

    for process in processes:
        process.start()

    for process in processes:
        process.join()

def AudioMain(NoteConditioning, AxisData, Tresholds = [0.5,0.5,0.2], StepsPerSecond = 5000):
    """
    Initializes the necesarry functions and processes for multiprocessing playback based on timestamps derived from axis data from threshold conditioning method.
    
    """
    binaryRhythmAxisData = NoteConditioning(AxisData, Tresholds)
    timestampsAxisData = BinaryNotesToTimestamps(binaryRhythmAxisData, StepsPerSecond)
    print(timestampsAxisData)
    multiprocessingPlayback(timestampsAxisData)


"""

Section 3 - Plotting and Animation
-------------------------------------------------

"""

def plotData(xx, yy, zz, plot_angle=30, min_display = 0, max_display = 1):

    """"
    Plots three-dimensional data (using MatLab.
    
    """

    fig = plt.figure("Plot",figsize=(6, 6))
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

"""
#TODO Animation

def plotAnimatedData(xx, yy, zz, plot_angle=30, min_display=0, max_display=1):


    fig = plt.figure("Animation", figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.patch.set_facecolor('grey')

    line, = ax.plot([], [], [], '-', color='orange', lw=0.1)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    ax.set_xlim(min_display, max_display)
    ax.set_ylim(min_display, max_display)
    ax.set_zlim(min_display, max_display)

    ax.set_xticks(np.linspace(min_display, max_display, 5))
    ax.set_yticks(np.linspace(min_display, max_display, 5))
    ax.set_zticks(np.linspace(min_display, max_display, 5))

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True)

    def update_point(num, line, point):
        x = xx[num]
        y = yy[num]
        z = zz[num]
        line.set_data(x, y)
        line.set_3d_properties(z)
        point.set_3d_properties(z)  # Update the Z position of the point
        return line, point

    ax.view_init(azim=plot_angle)

    # Create the animated point (sphere) at the starting position
    point, = ax.plot([xx[0]], [yy[0]], [zz[0]], 'ro', markersize=6)

    # Set up the animation and store it in the "anim" variable
    anim = animation.FuncAnimation(fig, update_point, frames=len(xx), fargs=(line, point),
                                   interval=50, repeat=True)

    plt.show()  # Display the animation

    return anim

#Example of Animation Usage
xx = np.linspace(0, 10, 100)
yy = np.sin(xx)
zz = np.cos(xx)
anim = plotAnimatedData(xx, yy, zz)

"""





if __name__ == "__main__":

    X_Axis, Y_Axis, Z_Axis   =   DataMain(  start_values = [0.1,0.1,0.1],
                                            parameters = {'a': 0.29, 'b': 0.14, 'c': 14},
                                            steps= 50000, step_size = 0.01     )
    
    
    #Interesting Parameters
    # {'a': 0.2, 'b': 0.2, 'c': 14}     -> Better Method 1
    # {'a': 0.29, 'b': 0.14, 'c': 14}   -> Better Method 2

    plotData(X_Axis, Y_Axis, Z_Axis)
    
    AxisData = [X_Axis, Y_Axis, Z_Axis]

    ###  Method 1 - Threshold Conditioning
    AudioMain(DataTresholdConditioning, AxisData, Tresholds = [0.5, 0.5, 0.1], StepsPerSecond = 2500)

    ###  Method 2 - Gradient Conditioning
    AudioMain(DataGradientConditioning, AxisData, Tresholds = [0, 0, 0], StepsPerSecond = 2000)




    

