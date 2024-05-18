import marsAtm as atm
import math
import numpy as np
import matplotlib.pyplot as plt

velocity_x = [246.19945324]
velocity_y = [-89.609314383]
modV = [(velocity_y[-1]**2 + velocity_x[-1]**2)**0.5]
height = [20]

def calculateThings():
    g0 = -3.711 #m/s^2
    kv = 0.05 #gain
    CdS = 4.92 #m^2
    Ve = 4400 #m/s
    m = 699 #kg
    m_fuel = 70 #kg
    m_tot = [m+m_fuel]
    ɣ = [-20] #20deg in rad
    dt = 0.01 #seconds
    time = [0]
    ht = 1.771 #Thruster deployment altitude, km 1.7
    ṁ = [0]
    h=20
    s = [0]

    while h>0:
        h = height[-1] #km
        #Catches negative height error
        try: ρ = atm.marsAtm(h, atm.marsinit())[1]
        except: print(h)

        modV.append((velocity_y[-1]**2 + velocity_x[-1]**2)**0.5)

        #Forces
        Fd = 1/2 * modV[-1]**2 * ρ * CdS 
        
        if h>ht or h<0.0003: 
            ΣFʸ = (m_tot[-1]) * g0 - Fd*math.sin(math.radians(ɣ[-1]))

            ṁ.append(0)

            ΣFₓ = -Fd*math.cos(math.radians(ɣ[-1]))

        elif 0.0003<h<ht and m_tot[-1] > 699: 

            ṁ.append(min(5,( -m_tot[-1] * g0) / Ve + kv * (-2-velocity_y[-1])))

            T = ṁ[-1]*Ve

            m_tot.append(m_tot[-1] - ṁ[-1]*dt)

            ΣFʸ = (m_tot[-1]) * g0 - (Fd+T) *math.sin(math.radians(ɣ[-1]))

            ΣFₓ = -Fd*math.cos(math.radians(ɣ[-1]))- T*math.cos((math.radians(ɣ[-1])))

        aʸ = ΣFʸ/(m_tot[-1])
        aₓ = ΣFₓ/(m_tot[-1])

        velocity_x.append(velocity_x[-1] + aₓ*dt)
        velocity_y.append(velocity_y[-1] + aʸ*dt)

        height.append(height[-1] + (velocity_y[-1]*dt)/1000)
        s.append(s[-1]+ (velocity_x[-1]*dt)/1000)
        ɣ.append(math.degrees(math.atan2(velocity_y[-1], velocity_x[-1])))

        time.append(time[-1] + dt)

    figure, axis = plt.subplots(2, 3) 

    axis[0,0].plot(s, height)
    axis[0, 0].set_title("Trajectory")
    axis[0, 0].set_xlabel("X Displacement")
    axis[0, 0].set_ylabel("Height")

    axis[0,1].plot(modV, height)
    axis[0, 1].set_title("Speed") 
    axis[0, 1].set_xlabel("Speed")
    axis[0, 1].set_ylabel("Height")
    
    axis[0,2].plot(time, ṁ)
    axis[0, 2].set_title("ṁ vs time") 
    axis[0, 2].set_xlabel("Time")
    axis[0, 2].set_ylabel("Mass flowrate")

    axis[1,0].plot(time, height)
    axis[1, 0].set_title("height vs time") 
    axis[1, 0].set_xlabel("Time")
    axis[1, 0].set_ylabel("Height")

    axis[1,1].plot(time, modV)
    axis[1, 1].set_title("Speed vs time") 
    axis[1, 1].set_xlabel("Time")
    axis[1, 1].set_ylabel("Speed")

    axis[1,2].plot(time, ɣ)
    axis[1, 2].set_title("ɣ vs time") 
    axis[1, 2].set_xlabel("Time")
    axis[1, 2].set_ylabel("Flight path angle")
    plt.show()
calculateThings()