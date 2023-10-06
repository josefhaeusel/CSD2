import numpy as np
import matplotlib.pyplot as plt

def rossler_attractor(x=0, y=0, z=0, a=0.3, b=0.21, c=5):
    """
    Equations for three-dimensional Rössler Attractor.
    
    """

    x_dot = -y - z
    y_dot = x + a * y
    z_dot = b + z * (x - c)
    return x_dot, y_dot, z_dot

def calculation(rossler_function, start_values = [0.1,0.1,0.1], steps= 10000, step_size = 0.01):
    """
    Calculates a three-dimensional recursive function.
    
    """

    xx = np.empty((steps + 1))
    yy = np.empty((steps + 1))
    zz = np.empty((steps + 1))
    
    xx[0], yy[0], zz[0] = (start_values[0], start_values[1], start_values[2])

    for i in range(steps):
        x_dot, y_dot, z_dot = rossler_function(xx[i], yy[i], zz[i])
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

def plotData(xx, yy, zz, plot_angle=30):

    """"
    Plots three-dimensional data using MatLab.
    
    """

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    plt.gca().patch.set_facecolor('grey')

    ax.plot(xx, yy, zz, '-', color='blue', lw=0.1)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    # Set axis limits based on the min and max values
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)

    # Add ticks for scales
    ax.set_xticks(np.linspace(0, 1, 5))
    ax.set_yticks(np.linspace(0, 1, 5))
    ax.set_zticks(np.linspace(0, 1, 5))

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True)

    ax.view_init(azim=plot_angle)

    plt.show()


def main():
    xx, yy, zz = calculation(rossler_attractor, start_values=[0.1,0.1,0.1], steps=100000, step_size=0.01)
    xx_norm, yy_norm, zz_norm = normalizeData(xx, yy, zz)
    plotData(xx_norm, yy_norm, zz_norm)


if __name__ == "__main__":
    main()
