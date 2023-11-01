# Rössler Attractor Sonification

This Python script generates a rhythmic sonification of the Rössler Attractor based on threshold and gradient conditioning. It also provides plotting and animation of the attractor.

## Demo

Find a video demonstration under the following link:


## Description

This script calculates and sonifies a three-dimensional Rössler Attractor, with the option to use different parameters. The main focus of this script is to explore the sonification of the attractor based on threshold and gradient conditions.

The following sections provide an overview of the key functions and functionalities:

## Section 1 - Data Processing of Rössler Attractor

This section describes how the Rössler Attractor is calculated and normalized. It includes functions for calculating the attractor, normalizing data, and initializing the data processing.

## Section 2 - Sonification of Data

In this section, the script explores two methods of sonification: threshold conditioning and gradient conditioning. The resulting binary data is converted into timestamps, which are used for audio playback. Multiprocessing is employed to play back audio events for each axis simultaneously.

## Section 3 - Plotting and Animation

This section provides functions for plotting and animating the three-dimensional data of the Rössler Attractor.

The animation is still WIP, thus commented out.

## Usage

The script provides examples of how to use it, including setting parameters for the Rössler Attractor and methods for sonification. You can experiment with different parameters and methods in the `__main__` section of the script.

## Dependencies

The script relies on the following Python libraries:

- NumPy
- Matplotlib
- Simpleaudio
- Pathlib
- Time
- Multiprocessing

## Acknowledgments

The script credits Leo Corte's visualization method, which is used for plotting the Rössler Attractor.


