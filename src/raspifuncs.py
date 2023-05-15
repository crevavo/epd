import setting as ss

def getCpuTemp():
    if ss.debug:
        temp = 42.5
    else:
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                temp = int(f.read()) / 1000
        except Exception as e:
                temp = 999
                
    return temp

if __name__ == '__main__':
    print(getCpuTemp())