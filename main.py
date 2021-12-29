import os
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
from time import sleep


client = OpenRGBClient()
client.clear()
motherboard = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
mouse = client.get_devices_by_type(DeviceType.MOUSE)[0]

def set_color(rgb):
    for i in range(3):
        if rgb[i] < 0:
            rgb[i] = 0
    motherboard.set_color(RGBColor(*rgb))
    sleep(0.000001)


def smooth_set_color(first_rgb, second_rgb, padding = 1):
    rgb = list(first_rgb)
    red_high, red_low = second_rgb[0], first_rgb[0]
    green_high, green_low = second_rgb[1], first_rgb[1]
    blue_high, blue_low = second_rgb[2], first_rgb[2]
    abss = [red_high - red_low, green_high - green_low, blue_high - blue_low]
    mn = min(map(lambda x : abs(x) // padding, list(filter(lambda x : x != 0, abss))))
    abss = list(map(lambda x : x // mn, abss))

    for i in range(mn):
        for j in range(3):
            rgb[j] += abss[j]
        set_color(rgb)
    set_color(second_rgb)

def hex2rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def init():
    global colors
    if not os.path.exists('index.txt'):
        with open('index.txt','w+') as file:
            steps = int(input("Enter number of profile steps : ")) + 1
            for i in range(1, steps):
                hx, duration = input(f"Enter the hex of {i}'st\\rd step : "), int(input(f"Enter the duration of {i}'st\\rd step : "))
                color = {
                    "RGB": hex2rgb(hx),
                    "Duration":duration
                }
                colors.append(color)
                print(hx,color.duration, file=file)
    else:
        with open('index.txt','r') as file:
            for line in file.readlines():
                hx, duration = line.split(' ')
                duration = float(duration)
                color = {
                    "RGB": hex2rgb(hx),
                    "Duration": duration
                }
                colors.append(color)

def mainloop():
    global colors
    while True:
        for i in range(1,len(colors)):
            smooth_set_color(colors[i - 1]["RGB"], colors[i]["RGB"], 10)
            sleep(colors[i]["Duration"])
        else:
            smooth_set_color(colors[-1]["RGB"], colors[0]["RGB"], 10)
            sleep(colors[0]["Duration"])



if __name__ == "__main__":
    init()
    mainloop()


