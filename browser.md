This is a utility to browse the data gathered from the astro-pi ISS mission
John Belshaw from an idea by Hannah Belshaw

The orbital elements in the file issObital.txt are kindly provided by Dr T.S Kelso http://celestrak.com

Requires matplotlib, numpy, mpl_toolkit, ephem to be installed which makes 
it easy to do numerical calculations on the data and plot it. Tested 
on windows, linux x86 and raspberry pi B2.

Lists the headers in the file and some statistics for each of 
the measurements - min, max, median, average, stddev

A graph is drawn for the first measurement, for 1104 points which is 2 orbits.

3 figure windows are opened (you may have to spread them out) -
fig 1 is a line graph of the current measurement
fig 2 is a plot of the iss ground track, night/day shaded for short intervals
fig 3 is filled with buttons to browse the data - 
scroll through the current measurement data using the buttons <-- -->
select new measurements using meas +, and meas -
zoom in and out using zoom + and zoom -  (by a factor of 2x)
orbit button re-draws the iss track (which is not automatic)

Each time a change is made the statistics for the current measurement and 
time period are printed.


Measurements - in array Headers
0 ROW_ID
1 temp_cpu
2 temp_h
3 temp_p
4 humidity
5 pressure
6 pitch
7 roll
8 yaw
9 mag_x
10 mag_y
11 mag_z
12 accel_x
13 accel_y
14 accel_z
15 gyro_x
16 gyro_y
17 gyro_z
18 reset
19 Time Stamp

If you want to re-use the data for your code it is in the data object -Arrays 
as a 2d arrary Arrays. This has 20 elements, each of which is a sub-array 
with all the data points.  So Arrays[6] is an array of all the pitch 
measurements (quite long!) and Arrays[6][0] is the first data point, 
Arrays[6][-1] is the last data point Arrays[0] is the ROW_ID/6  which is the 
elapsed time in minutes Arrays[19] is the time stamp for that row.