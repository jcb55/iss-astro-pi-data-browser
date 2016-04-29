# -*- coding: utf-8 -*-
"""
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


"""
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import os 

Directory='C:/Users/jbelshaw/Desktop/Working/ISS/' 
#Filename='Columbus2_Ed_astro_pi_datalog.csv'
#Filename='Columbus_Ed_astro_pi_datalog.csv'
Filename='Node2_Izzy_astro_pi_datalog.csv'


Headers=[]
Arrays = []
NL=0

#FilePath = normpath(Directory+Filename)


with open(os.path.normpath(Directory+Filename)) as file:
  for line in file:
    NL +=1
    if (NL==1):
        headers=line.split(",")
        for h in headers:
            Headers.append(h)   
        Headers.pop(-1) # remove time stamp header as time is not a float
    ns = line.split(",")
    if (NL==1):
        for val in ns:
            empty=[]
            Arrays.append(empty)   
    else:
        nv = 0
        for val in ns:
            Arrays[nv].append(val)
            nv +=1
file.close()
rows = len(Arrays[0])

nh=0
print
print " File", Filename, "  rows=", rows, rows/360, "hours"
print
print " Measurement      #    min         max        median      average    stddev"
for h in Headers:
    narray = np.array(Arrays[nh]).astype(np.float32)
    if (Headers[nh] == "pitch"):
        # pitch seems to oscillate from close to zero to about 350 
        # so normalise it so it is close to zero
        nv = 0
        for val in narray:
             if (val >= 180.0):
                 narray[nv] = narray[nv]-360.0
                 #print val, narray[nv] 
             if (val <= -180.0):
                 narray[nv] = narray[nv] + 360.0
                 #print val, narray[nv] 
             nv +=1
    if (nh == 0):
        # each data point is 10 secs so this scales x axis to minutes
        narray = narray / 6.0
    #Calculate some basic stats on each row
    min = np.amin(narray)
    max = np.amax(narray)
    med = np.median(narray)
    aver = np.amax(narray)
    stddev = np.std(narray)
    print "%12s %6s %10.5f %10.5f %10.5f %10.5f %10.5f" % (h, nh, min,max, med, aver, stddev)
    Arrays[nh] = narray
    nh +=1
   
# at this point all data is in the array Array
# and headers in the array Headers

 # Code to plot out figures 
axes = host_subplot(111, axes_class=AA.Axes)      
param = 1
n = 0 
step = 2208 # 4 orbits 
while True:
    plt.cla()
    plt.ion()
    print "plotting", n, "to", n+step, "for ", Headers[param]
    axes.plot(Arrays[0][n:(n+step)],Arrays[param][n:(n+step)] )  
    plt.show()
    keyPress = raw_input("WASD to navigate ")
    if (keyPress == "w"): # w
        param +=1
    if (keyPress == "s" ): # s
        param -=1
    if (keyPress == "a"): # a
        n -=step
    if (keyPress == "d"): # d
        n +=step
    # Careful not to go outside of data arra, or plot the ROW_ID
    if (param <= 1):
        param = 1
    if (param >= len(Headers)-1):
        param = len(Headers)-1
    if (n > rows ):
        print "END of DATA SET, wrapping round to start"
        n = 0
    if (n < 0):
        print "OVERSHOT Start of DATA SET, Wrapping round to end"
        n = rows - step
        
    


