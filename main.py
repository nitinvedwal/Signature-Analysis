import os
import glob
import numpy as np
import matplotlib.pyplot as pp
import pandas as pd
import math
import time
filelocation = "D:/UGP/data/data3/DS1_Modification_TimeFunctions/usuario1001/*"
filelocation = glob.glob(filelocation)

# read all signature of a person usuario1001
# math.atan(x)
for file in filelocation:
    with open(f"{file}") as f:
        data = np.loadtxt(f)
        # shifting points to the origin
        xmin = data[0][0]
        ymin = data[0][1]
        xmax = data[0][0]
        ymax = data[0][1]
        for i in range(len(data)):
            xmin = min(xmin, data[i][0])
            ymin = min(ymin, data[i][1])
            xmax = max(xmax, data[i][0])
            ymax = max(ymax, data[i][1])

        totalpoints = 0
        for i in range(len(data)):
            if (data[i][3]):
                totalpoints += 1
        # section 1
        # x , y and pressure series,     x mean , y mean and pressure mean ,     sd x , sd y sd pressure
        x = []
        y = []
        pressure = []
        meanx = 0
        meany = 0
        meanpressure = 0
        stdx = 0
        stdy = 0
        stdpressure = 0

        for i in range(len(data)):
            if (data[i][3]):
                x.append((data[i][0]-xmin))
                y.append((data[i][1]-ymin))
                pressure.append(data[i][4])
        meanx = sum(x)/totalpoints
        meany = sum(y)/totalpoints
        meanpressure = sum(pressure)/totalpoints
        print("mean x is"+str(meanx))
        print("mean y is"+str(meany))
        print("mean pressure is"+str(meanpressure))

        stdsumx = 0  # (x^2-u)
        stdsumy = 0
        stdsumpressure = 0
        for i in range(len(x)):
            stdsumx += pow((x[i]-meanx), 2)
            stdsumy += pow((y[i]-meany), 2)
            stdsumpressure += pow((pressure[i]-meanpressure), 2)
        stdx = math.sqrt(stdsumx/totalpoints)
        stdy = math.sqrt(stdsumy/totalpoints)
        stdpressure = math.sqrt(stdsumpressure/totalpoints)

        print("std x is "+str(stdx))
        print("std y is"+str(stdy))
        print("std pressure is"+str(stdpressure))
