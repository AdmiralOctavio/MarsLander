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
    ɣ = [-0.349066] #20deg in rad
    dt = 0.007 #seconds
    time = [0]
    ht = 1.7 #Thruster deployment altitude, km
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
        
        if h>ht: 
            ΣFʸ = (m_tot[-1]) * g0 - Fd*math.sin(ɣ[-1]*0.0174533) 
            ṁ.append(0)

        elif 0.003<h<ht and m_tot[-1] > 699: 

            ṁ.append(min(5,( -m_tot[-1] * g0) / Ve + kv * (-2-velocity_y[-1])))

            T = ṁ[-1]*Ve

            m_tot.append(m_tot[-1] - ṁ[-1]*dt)

            ΣFʸ = (m_tot[-1]) * g0 - Fd*math.sin(ɣ[-1]*0.0174533) - T*math.sin(ɣ[-1]*0.0174533)
            print(str(T) + " | " + str(ṁ[-1]))

        else: 
            ΣFʸ = m_tot[-1]*g0
            ṁ.append(0)

        ΣFₓ = -Fd*math.cos(ɣ[-1])
        aʸ = ΣFʸ/(m_tot[-1])
        aₓ = ΣFₓ/(m_tot[-1])

        velocity_x.append(velocity_x[-1] + aₓ*dt)
        velocity_y.append(velocity_y[-1] + aʸ*dt)

        height.append(height[-1] + (velocity_y[-1]*dt)/1000)
        s.append(s[-1]+ (velocity_x[-1]*dt)/1000)

        if velocity_x[-1] >0:

            ɣ.append(57.2958 * math.atan2(velocity_y[-1], velocity_x[-1]))

        else: 
            ɣ.append(57.2958 * math.atan2(velocity_y[-1], velocity_x[-1])) + 180

        time.append(time[-1] + dt)

    figure, axis = plt.subplots(2, 3) 

    axis[0,0].plot(s, height)
    axis[0, 0].set_title("Trajectory") 

    axis[0,1].plot(modV, height)
    axis[0, 1].set_title("Speed") 

    axis[0,2].plot(time, ṁ)
    axis[0, 2].set_title("ṁ vs time") 

    axis[1,0].plot(time, height)
    axis[1, 0].set_title("height vs time") 

    axis[1,1].plot(time, modV)
    axis[1, 1].set_title("Speed vs time") 

    axis[1,2].plot(time, ɣ)
    axis[1, 2].set_title("ɣ vs time") 
    plt.show()

calculateThings()