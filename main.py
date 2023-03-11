import os
import glob
import numpy as np
import matplotlib.pyplot as pp
import pandas as pd
import math
import time
import statistics
filelocation = "D:/UGP/data/data3/DS1_Modification_TimeFunctions/usuario1001/*"
filelocation = glob.glob(filelocation)
pie = 3.14159265359
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
        # here totalpoints are the points with pendowns only
        totalpoints = 0
        for i in range(len(data)):
            if (data[i][3]):
                totalpoints += 1
        # ---------------------------section 1 -----------------------------------------------------
        # x y and pressure series
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

        # time series for section 2
        timeseries = []

        for i in range(len(data)):
            if (data[i][3]):
                x.append((data[i][0]-xmin))
                y.append((data[i][1]-ymin))
                timeseries.append(data[i][2])
                pressure.append(data[i][4])

        meanx = sum(x)/totalpoints
        meany = sum(y)/totalpoints
        meanpressure = sum(pressure)/totalpoints
        # print("mean x is"+str(meanx))
        # print("mean y is"+str(meany))
        # print("mean pressure is"+str(meanpressure))

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

        # print("std x is "+str(stdx))
        # print("std y is"+str(stdy))
        # print("std pressure is"+str(stdpressure))
        # print(timeseries)

        # ------------------------------section 2------------------------------------------------------
        # radial distance and theta series
        # radialdist=d
        d = []
        theta = []

        meand = 0
        meantheta = 0

        stdd = 0
        stdtheta = 0

        for i in range(len(data)):
            if (data[i][3]):
                d.append(
                    math.sqrt(pow(data[i][0]-xmin, 2)+pow(data[i][1]-ymin, 2)))
                if (data[i][0]-xmin == 0):
                    theta.append(pie/2)
                else:
                    theta.append(
                        math.atan((data[i][1]-ymin)/(data[i][0]-xmin)))

        meand = sum(d)/totalpoints
        meantheta = sum(theta)/totalpoints

        # print("mean d is"+str(meand))
        # print("mean theta is"+str(meantheta))

        mediand = statistics.median(d)
        mediantheta = statistics.median(theta)

        # print("meadin of d is"+str(mediand))
        # print("median of theta is"+str(mediantheta))

        stdsumd = 0
        stdsumtheta = 0
        for i in range(len(d)):
            stdsumd += pow(d[i]-meand, 2)
            stdsumtheta += pow(theta[i]-meantheta, 2)

        stdd = math.sqrt(stdsumd/totalpoints)
        stdtheta = math.sqrt(stdsumtheta/totalpoints)

        # print("std d is"+str(stdd))
        # print("std theta is"+str(stdtheta))
        # ------------------------section 5----------------------------------------------
        #  making skewness and kurtosis
        skewnesssumx = 0
        skewnesssumy = 0
        kurtosissumx = 0
        kurtosissumy = 0
        for i in range(len(x)):
            skewnesssumx += pow((x[i]-meanx), 3)
            skewnesssumy += pow((y[i]-meany), 3)
            kurtosissumx += pow((x[i]-meanx), 4)
            kurtosissumy += pow((y[i]-meany), 4)
        skewnessx = skewnesssumx/((totalpoints-1)*pow(stdx, 3))
        skewnessy = skewnesssumy/((totalpoints-1)*pow(stdy, 3))
        kurtosisx = kurtosissumx/((totalpoints-1)*pow(stdx, 3))
        kurtosisy = kurtosissumy/((totalpoints-1)*pow(stdx, 3))

        # ------------------------section 3----------------------------------------------
        # velocity acceleration angular velocity
        tend = max(timeseries)
        tstart = min(timeseries)

        velocity = []
        acceleration = []
        angvelocity = []

        for i in range(len(x)-1):
            temp = (math.sqrt(pow(x[i+1]-x[i], 2) +
                    pow(y[i+1]-y[i], 2)))*(tend-tstart)
            velocity.append(temp/(timeseries[i+1]-timeseries[i]))
            if (x[i+1] == 0 or x[i] == 0):
                if (x[i+1] == 0 and x[i] == 0):
                    temp1 = 0
                elif (x[i+1] == 0 and x[i] != 0):
                    temp1 = (abs(pie/2 -
                                 math.atan(y[i]/x[i])))*(tend-tstart)
                elif (x[i+1] != 0 and x[i] == 0):
                    temp1 = (abs(math.atan(y[i+1]/x[i+1]) -
                                 pie/2))*(tend-tstart)

            else:
                temp1 = (abs(math.atan(y[i+1]/x[i+1]) -
                             math.atan(y[i]/x[i])))*(tend-tstart)
            angvelocity.append(temp1/(timeseries[i+1]-timeseries[i]))

        for i in range(len(velocity)-1):
            temp = (abs(velocity[i+1]-velocity[i]))*(tend-tstart)
            acceleration.append(temp/(timeseries[i+1]-timeseries[i]))
        avgvelocity = sum(velocity)/len(velocity)
        avgacceleration = sum(acceleration)/len(acceleration)
        avgangvelocity = sum(angvelocity)/len(angvelocity)
        # -------------------------section 4-----------------------------------------------
        # numbers of penups and down
        pencount = 0
        for i in range(len(data)-1):
            if (data[i+1][3] != data[i][3]):
                pencount += 1
        # print(pencount)

        # --------------------------making features vector----------------------------------
        features = []
        features.append(meanx)
        features.append(meany)
        features.append(meanpressure)
        features.append(stdx)
        features.append(stdy)
        features.append(stdpressure)
        features.append(meand)
        features.append(meantheta)
        features.append(mediand)
        features.append(mediantheta)
        features.append(stdd)
        features.append(stdtheta)
        features.append(skewnessx)
        features.append(skewnessy)
        features.append(kurtosisx)
        features.append(kurtosisy)
        features.append(avgvelocity)
        features.append(avgacceleration)
        features.append(avgangvelocity)
        print(features)
