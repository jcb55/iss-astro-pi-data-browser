
# -*- coding: utf-8 -*-
"""
This is a utility to browse the data gathered from the astro-pi ISS mission
Hannah Belshaw and John Belshaw
You should edit the filename and Directory below to the path on your computer

It requires matplotlib, numpy, mpl_toolkit, ephem to be installed which makes 
it easy to do numerical calculations on the data and plot it. Tested 
on windows, linux x86 and raspberry pi B2.


Lists the headers in the file and some statistics for each of 
the measurements - min, max, median, average, stddev

A graph is drawn for the first measurement, for 1104 points which is 2 orbits.

3 figure windows are opened (you may have to spread them out) -
fig 1 is a line graph of the current measurement
fig 2 is a plot of the iss ground track, night/day shaded for short intervals
fig 3 is a window filled with buttons to browse the data - 
Scroll through the current measurement data using the buttons <-- -->
select new measurements using meas +, and meas -
zoom in and out using zoom + and zoom -  (by a factor of 2x)
the orbit button re-draws the iss track (which is not automatic)

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

There is a data set in the file - 
Columbus_Ed_astro_pi_datalog.csv.gz which should be uncompresssed before use

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os 
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
import ephem
import sys


class issElements:
    """ Class to read the available orbital elements extract the ISS data
    and provide a function to return the elements for a particular time
    
    elements is an array of elements, which is a tuple of the 2 lines
    
    elementi is an array of datetimes which is index to the elements
    """
    elements=[]
    elementi=[]
    # set to True to see more debug
    chatty=False
    directory=""
    
    def __init__(self):
        filePath = ("issOrbital.txt")
        if (self.chatty): print filePath, "filePath"
	try:
            with open (filePath, 'r') as infile:
                fileLines = (infile.read().splitlines())[6:]     
        except:
            print "cannot open file - ", filePath
            sys.exit()
	n =  -1
	for line in fileLines:
	  n += 1
	  if line[0] == "1":
	    ael = []
	    ael.append(fileLines[n])
	    ael.append(fileLines[n+1])
	    self.elements.append(ael)
	    # date entry is yy.ddd.######
	    line1s = fileLines[n].split()
	    line2s = line1s[3].split(".")
	    #if(self.chatty): print line1s[3],line2s 
	    #if(self.chatty): print line2s[1], float("."+line2s[1]), (float("."+line2s[1])*3600.*24.)
	    dt = datetime.strptime(line2s[0], '%y%j') + \
	    timedelta(seconds=(float("."+line2s[1])*3600.*24.))
	    self.elementi.append(dt)
	    
    def findDateFromString(self,string):
       if (self.chatty): print "findDateFromString ", string
       #return(datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f'))
       # for the spacecraft data
       return(datetime.strptime(string, '%Y-%m-%d %H:%M:%S'))
        
    def elemsFromDateString(self,string):
        t = self.findDateFromString(string)
	n = -1
	for te in self.elementi:
	  n += 1
	  if te > t:
	    if (self.chatty): print "Found elements at ",n , self.elements[n]
	    return(self.elements[n])
    
  
class ISSData():
  Arrays=[]
  rows = 0
  n = 0
  step = 1104
  Headers = []
  Directory = ''
  normPath = ""
  chatty = False
  map = ""
  ag =""
  
  def __init__(self,fileName,directory=""):
      """ Check to see if files exists 
      """
      self.map = Basemap(projection='mill',lon_0=-10)
      normPath = os.path.normpath(directory+fileName)
      try:
          dFile= open(normPath,"r")
      except:
          print "Cannot open", normPath
      # save tested path for later use
      self.normPath = normPath
      dFile.close()  
      
   
  def readDataFromFile(self):
    NL=0
    with open(self.normPath) as file:
      for line in file:
        line= line.rstrip()
        NL +=1
        ns = line.split(",")
        if (NL==1):
          headers= ns
          for h in headers:
              self.Headers.append(h)   
          self.Headers.pop(-1) # remove time stamp header as time is not a float
          for val in ns:
            empty=[]
            self.Arrays.append(empty)  
        else:
          nv = 0
          for val in ns:
            self.Arrays[nv].append(val)
            nv +=1
    file.close()
    self.rows = len(self.Arrays[0])

    nh=0
    print " File", self.normPath, "  rows=", self.rows, self.rows/360, "hours"
    print self.Arrays[19][0]," - ", self.Arrays[19][-1]
    print " Measurement      #    min         max        median      average    stddev"
    for h in self.Headers:
        narray = np.array(self.Arrays[nh]).astype(np.float32)
        if (nh == 0):
        # each data point is 10 secs so this scales x axis to minutes
            narray = narray / 6.0
        #Calculate some basic stats on each row
 
        max = np.amax(narray)
        if (headers[nh] == "pitch") or (headers[nh] == "yaw") :
            if (max >= 20000.):
                # convert from radians to degrees?
                # in the first Spacecraft dataset only (I think)
                narray = narray / 57.3
            nv=0
            for val in narray:
              if (val <= -180.0):
                narray[nv] = narray[nv] + 360.0
              elif (val >= 180.0):
                 narray[nv] = narray[nv] - 360.0
              nv +=1
              # pitch looks better when normalized about zero 
            max = np.amax(narray)
        min = np.amin(narray)
        med = np.median(narray)
        aver = np.average(narray)
        stddev = np.std(narray)
        print "%12s %6s %10.5f %10.5f %10.5f %10.5f %10.5f" % (h, nh, min,max, med, aver, stddev)
        self.Arrays[nh] = narray
        nh +=1
    # Normalize 


  def printStats(self,param=1,n=0,step=1104):
        print step,"datapoints - ", (self.Arrays[19][n])," - ", \
        (self.Arrays[19][n+step])
        print " Measurement      #    min         max        median      average    stddev"
        min = np.amin(self.Arrays[param][n:n+step])
        max = np.amax(self.Arrays[param][n:n+step])
        med = np.median(self.Arrays[param][n:n+step])
        aver = np.average(self.Arrays[param][n:n+step])
        stddev = np.std(self.Arrays[param][n:n+step])
        print "%12s %6s %10.5f %10.5f %10.5f %10.5f %10.5f" % ( self.Headers[param], param, min,max, med, aver, stddev)

  def drawNightDay(self,param=1,n=0,step=1104):
        if (self.chatty): print self.Headers[param], n,step
        cn = int(n + step /2)
        ct = self.Arrays[19][cn]
        print "Centre time period = ", ct
        # miller projection
        
        # plot coastlines, draw label meridians and parallels.
        self.map.drawcoastlines()
        self.map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
        self.map.drawmeridians(np.arange(self.map.lonmin,self.map.lonmax+30,60),labels=[0,0,0,1])
        # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
        self.map.drawmapboundary(fill_color='white')
        self.map.fillcontinents(color='coral',lake_color='white')
        # shade the night areas, with alpha transparency so the
        # map shows through. Use current time in UTC.
        #en = el.findIndexFromDate(ct)
        #eo = el.extractISSfromIndex(en)
        #print eo
        date = el.findDateFromString(ct)
        if (step <= 1104):
            self.map.nightshade(date)
        else: print "Track too long for night shading"
        plt.title('ISS Track %s (UTC)' % ct)
#        self.drawIssTrack(elements,param,n,step)
        
        
  def drawIssTrack(self,elements,param=1,n=0,step=1104):
      st = self.Arrays[19][n]
      et = self.Arrays[19][n+step]
      print "Plotting from - ", st, " to ", et
      cn = int(n + step /2)
      ct = self.Arrays[19][cn]
      line1,line2=elements.elemsFromDateString(ct)
      if (self.chatty): print "drawIssTrack", n,step, ct, line1, line2
      for nn in range(n,n+step,6):
          ntime = self.Arrays[19][nn]
          #if self.chatty: print ntime
          tle_rec = ephem.readtle("ISS", line1, line2)
          tle_rec.compute(ntime)
          #convert to strings#
          lat2string = str(tle_rec.sublat)
          long2string = str(tle_rec.sublong)
          lati = lat2string.split(":")
          longt = long2string.split(":")
          #if self.chatty: print "ISS SUBSURFACE -", lati,longt
          lat = float(lati[0]) + float(lati[1])/60. + float(lati[2])/3600.
          lon = float(longt[0]) + float(longt[1])/60. + float(longt[2])/3600. 
          xpt,ypt=self.map(lon,lat)
	  # drawing style
	  kargs = "g+"
          if (nn == n):
              plt.text(xpt,ypt,"start")
          if (nn >= (n+step -6) ):
              plt.text(xpt,ypt,"end")
	  # make every 5 mins dot
	  if ((nn % 30) == 0): kargs = "g." 
          self.map.plot(xpt,ypt,kargs)
       
        
  def drawDataPlot(self,param=1,n=0,step=1104):
      plt.figure(1)
      plt.clf()
      plt.title(self.Headers[param])
      plt.plot(self.Arrays[0][n:(n+step)],self.Arrays[param][n:(n+step)])
      #self.ag.set_xdata(self.Arrays[0][n:(n+step)])
      plt.draw()
     
    
class interactiveLoop():
    param=1
    n = 0
    step = 1104
    minStep = 10
    maxStep = 20000
    data = ""
    elements = ""
    
    ind = 0

    def scrollf(self, event):
        self.n = self.n + self.step
        if (self.n  >= self.data.rows - self.step):
            print "Wrapping round to beginning"
            self.n = 1
        self.data.drawDataPlot(self.param,self.n,self.step)    
        
    def scrollb(self, event):
        self.n = self.n - self.step
        if (self.n  < 0):
            print "Wrapping round to end"
            self.n = self.data.rows - self.step -1
        self.data.drawDataPlot(self.param,self.n,self.step)    
        
    def measf(self,event):
        self.param = self.param + 1
        if (self.param >= 19):
            print "Wrapping round to beginning"
            self.param = 1
        self.data.drawDataPlot(self.param,self.n,self.step)  
        
    def measb(self, event):
        self.param = self.param - 1
        if (self.param <= 0):
            print "Wrapping round to end"
            self.param = 18
        self.data.drawDataPlot(self.param,self.n,self.step)  
        
    def zoomIn(self, event):
        if (self.step >= self.minStep): 
                self.step = int(self.step/2)
                self.data.drawDataPlot(self.param,self.n,self.step)
        else:
            print "Maximum zoom"
        
        
    def zoomOut(self, event):
        if (self.step <= self.maxStep):
                self.step = int(self.step * 2)
                self.data.drawDataPlot(self.param,self.n,self.step)
        else:
            print "Minimum zoom"
        self.data.drawDataPlot(self.param,self.n,self.step) 
    
    def drawOrbit(self, event):
        plt.figure(2)
        plt.cla()        
        self.data.drawNightDay(self.param,self.n,self.step)
        self.data.drawIssTrack(self.elements,self.param,self.n,self.step)
        plt.draw()
    
    def __init__(self,data,elements):
        """ data is an instance of ISSData,
        elements is an instance of issElements
        """
        self.data = data
        self.elements = elements


if __name__ == '__main__':
     
    #Directory='C:/Users/jbelshaw/Desktop/Working/ISS/' 
    #Directory='' 
    #Filename='Columbus2_Ed_astro_pi_datalog.csv'
    #Filename='Columbus_Ed_astro_pi_datalog.csv'
    #Filename='NewSC.csv'
    
    el = issElements()
    idata=ISSData("Columbus_Ed_astro_pi_datalog.csv")
    idata.readDataFromFile()
    il = interactiveLoop(idata,el)
    plt.figure(1)
    idata.drawDataPlot(1,0,1104)  
    #idata.drawDataPlot(il.param,il.n,il.step)    
    idata.printStats(il.param,il.n,il.step)
    plt.figure(2)
    idata.drawNightDay(il.param,il.n,il.step)
    idata.drawIssTrack(il.elements,il.param,il.n,il.step)
    plt.figure(3,figsize=(6,2))    
    bscrollf = Button(plt.axes([0.6, 0.5, 0.2, 0.4]),"-->")
    bscrollb = Button(plt.axes([0.4, 0.5, 0.2, 0.4]),"<--")
    bscrollf.on_clicked(il.scrollf)
    bscrollb.on_clicked(il.scrollb)
    bmeasf = Button(plt.axes([0.2, 0.1, 0.2, 0.4]),"meas +")
    bmeasb = Button(plt.axes([0.0, 0.1, 0.2, 0.4]),"meas -")
    bmeasf.on_clicked(il.measf)
    bmeasb.on_clicked(il.measb)
    bzoomf = Button(plt.axes([0.6, 0.1, 0.2, 0.4]),"zoom +")
    bzoomb = Button(plt.axes([0.4, 0.1, 0.2, 0.4]),"zoom -")
    bzoomf.on_clicked(il.zoomIn)
    bzoomb.on_clicked(il.zoomOut)
    borbit = Button(plt.axes([0., 0.5, 0.2, 0.4]),"orbit")
    borbit.on_clicked(il.drawOrbit)
    
    plt.show()
