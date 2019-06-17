from math import inf
ro = 10
syg = 0.1
w1 = 0
w2 = 0
p1x = 1
p1y = 5
p2x = 7
p2y = 3

def getInput():
    while True:
        try:
            p1x = int(input("Enter x1: "))
            break
        except:
            print("Input only integers!")
    while True:
        try:
            p1y = int(input("Enter y1: "))
            break
        except:
            print("Input only integers!")
    while True:
        try:
            p2x = int(input("Enter x2: "))
            break
        except:
            print("Input only integers!")
    while True:
        try:
            p2y = int(input("Enter y2: "))
            break
        except:
            print("Input only integers!")
    while True:
        try:
            ro = int(input("Enter ro: "))
            break
        except:
            print("Input only integers!")
    return ro, p1x, p1y, p2x, p2y



if __name__ == "__main__":

    print("Enter coordinates of 2 points and R which is going to be a divider")
    ro, p1x, p1y, p2x, p2y = getInput()

    fo = "%.2f"

    for i in range(10000):
        p1flag = False
        p2flag = False
        y = p1x*w1 + p1y*w2
        if y < ro:
            print("\n(", p1x, ",", p1y, ")")
            print(fo % p1x, "*", fo % w1, "+", fo % p1y, "*", fo % w2, "=", fo % y)
            delt = ro - y
            print("delt = ", delt)
            w1 = w1 + delt*p1x*syg
            w2 = w2 + delt*p1y*syg
            print("w1 = ", w1)
            print("w2 = ", w2)
        else:
            p1flag = True

        y = p2x*w1 + p2y*w2
        if y > ro:
            print("\n(", p2x, ",", p2y, ")")
            print(fo % p2x, "*", fo % w1, "+", fo % p2y, "*", fo % w2, "=", fo % y)
            delt = ro - y
            print("delt = ", delt)
            w1 = w1 + delt*p2x*syg
            w2 = w2 + delt*p2y*syg
            print("w1 = ", w1)
            print("w2 = ", w2)
        else:
            p2flag = True

        if abs(w1) > 5000000000000 or abs(w2) > 50000000000000:
            print("No possible solutions.")
            break

        if p1flag and p2flag:
    
            print("\nSuccess")
            y = p1x*w1 + p1y*w2
            print(fo % p1x, "*", fo % w1, "+", fo % p1y, "*", fo % w2, "=", fo % y)
            y = p2x*w1 + p2y*w2
            print(fo % p2x, "*", fo % w1, "+", fo % p2y, "*", fo % w2, "=", fo % y)
            break
