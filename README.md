# iss-astro-pi-data-browser
This is a utility to browse the data gathered from the astro-pi ISS mission
Hannah Belshaw and John Belshaw
You should edit the filename and Directory below to the path on your computer

It requires matplotlib and numpy to be installed which makes it easy to 
do numerical calculations on the data and plot it

Lists the headers in the file and some statistics for each of 
the measurements - min, max, median, average, stddev

A graph is drawn for the first measurement, for 2208 points which is 4 orbits.

You can scroll through the data by typing one of wasd then return, 
a scrolls back 2000, d goes forward 2000 points, 
w goes to the next measurement, s goes back to the previous measurement

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

If you want to re-use the data for your code it is in the 2d arrary Arrays.
which has 19 elements, each of which is a sub-array  with all the data points
so Arrays[6] is an array of all the pitch measurements (quite long!)
and Arrays[6][0] is the first data point, Arrays[6][-1] is the last data point
Arrays[0] is the ROW_ID which is just the line number in the file

