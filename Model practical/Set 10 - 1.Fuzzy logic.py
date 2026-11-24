
def cold(temp):
    if temp <= 15:
        return 1
    elif temp < 25:
        return (25 - temp) / 10
    return 0

def warm(temp):
    if temp <= 15 or temp >= 35:
        return 0
    elif temp <= 25:
        return (temp - 15) / 10
    else:
        return (35 - temp) / 10

def hot(temp):
    if temp <= 25:
        return 0
    elif temp < 35:
        return (temp - 25) / 10
    return 1

def fan_control(temp):
    c = cold(temp)
    w = warm(temp)
    h = hot(temp)

    speed = (c * 20 + w * 50 + h * 100) / (c + w + h)

    print("\nTemperature:", temp, "°C")
    print("Cold Membership:", round(c, 2))
    print("Warm Membership:", round(w, 2))
    print("Hot Membership:", round(h, 2))
    print("Fan Speed:", round(speed, 2), "%")

    if speed <= 30:
        print("Fan Status: LOW")
    elif speed <= 70:
        print("Fan Status: MEDIUM")
    else:
        print("Fan Status: HIGH")

temp = float(input("Enter temperature in Celsius: "))
fan_control(temp)
