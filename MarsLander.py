import marsAtm as atm
import math
import numpy as np
import matplotlib.pyplot as plt
g0 = 3.711 #m/s^2
h0 = 20 #km
kv = 0.005 #gain
CdS = 4.92 #m^2
Ve = 4400 #m/s
m = 699 #kg

velocity_x = [246.19945324]
velocity_y = [89.609314383]
height = [20]

def calculateThings():
    ɣ = [0.349066] #rad 
    modV = [(velocity_y[-1]**2 + velocity_x[-1]**2)**0.5]
    dt = 0.1 #seconds
    time = [0]
    h=20
    while h>0:
        h = height[-1] #km

        try: ρ = atm.marsAtm(h, atm.marsinit())[1]
        except: print(h)

        modV.append((velocity_y[-1]**2 + velocity_x[-1]**2)**0.5)

        Fd = 1/2 * modV[-1]**2 * ρ * CdS 

        ΣFʸ = m*g0 - Fd*math.sin(ɣ[-1])
        ΣFₓ = - Fd*math.cos(ɣ[-1])
        aʸ = ΣFʸ/m
        aₓ = ΣFₓ/m

        velocity_x.append(velocity_x[-1] + aₓ*dt)
        velocity_y.append(velocity_y[-1] + aʸ*dt)

        height.append(height[-1] - (velocity_y[-1]*dt)/1000)
        ɣ.append(math.atan(velocity_y[-1]/velocity_x[-1]))
        time.append(time[-1] + dt)

    plt.plot(time, modV)
    plt.show()

calculateThings()