import math
def marsinit():
    atmList = []
    with open("marsatm.txt", "r") as mars:
        for line in mars: atmList.append(line)
    return atmList
def interpolate(h, h1, y1, y2): return (h-h1)/10 * y2 + (1-(h-h1)/10) * y1
def marsAtm(h, atmList):
    '''Returns temperature, density, speed of sound, and pressure at a given altitude on Mars.'''
    output = []
    index = math.floor(h/10)+2
    h1 = atmList[index].split()[0]
    for i in range(1, 4):
        y1, y2 = atmList[index].split()[i], atmList[index+1].split()[i]
        output.append(interpolate(h, int(h1), float(y1), float(y2)))
    output.append(191.84 * float(atmList[index].split()[1]) * float(atmList[index].split()[2])) #Pressure
    return output
print(marsAtm(15, marsinit()))