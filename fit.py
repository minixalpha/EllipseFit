#coding:utf-8

# Fit ellipse using eight arc

import decimal
import math
import sys

W = 1000
H = 1000

def c2d(a):
    return decimal.Decimal(a)

def d2c(a):
    return float(a)

def getR1(da, db, emax1, emax2):
    r = ((db * db / da + (da*da - db*db) * emax1 / (da*da)) 
        + db/(da*da)*((da*da-db*db)*(c2d(2)*da-emax1)*emax1).sqrt())
    x = da - r
    y = decimal.Decimal(0)

    return (r, x, y)

def getR2(da, db, emax1, emax2):
    r = ((da * da / db + (da*da-db*db)*emax2/(db*db)) 
        - da/(db*db)*((da*da-db*db)*(c2d(2)*db+emax2)*emax2).sqrt())
    x = decimal.Decimal(0)
    y = db - r

    return (r, x, y)

def getR3(da, db, emax1, emax2):
    (r1,x1,y1) = getR1(da, db, emax1, emax2)
    (r2,x2,y2) = getR2(da, db, emax1, emax2)

    cost1 = (da*da+db*db-c2d(2)*da*r1)/(da*da-db*db)
    t1 = c2d(math.acos(cost1))

    sint2 = (c2d(2)*db*r2-(da*da+db*db))/(da*da-db*db)
    t2 = c2d(math.asin(sint2))

    tgsita2 = db/da*c2d(math.tan(t2))
    sita2 = c2d(math.atan(tgsita2))

    sinw2 = (r2-db)*c2d(math.cos(sita2))/r2
    w2 = c2d(math.asin(sinw2))

    beita2 = c2d(math.pi)/c2d(2)-c2d((sita2+w2))
    tanalpha = (da-r1)/(r2-db)
    alpha = c2d(math.atan(tanalpha))

    psi2 = alpha - beita2
    k = ((r2-db)*(r2-db) + (da-r1)*(da-r1)).sqrt()

    r = ((r2*r2+k*k-r1*r1-c2d(2)*k*r2*c2d(math.cos(psi2)))
        / (c2d(2)*(r2-r1-k*c2d(math.cos(psi2)))))

    sinpsi1 = (r2-r)*c2d(math.sin(psi2))/(r-r1)
    psi1 = c2d(math.asin(sinpsi1))
    beita1 = c2d(math.pi/2) - (alpha+psi1)
    beita0 = psi1 + psi2

    x = (r2 - r) * c2d(math.sin(beita2))
    y = (r2 - r) * c2d(math.cos(beita2)) - (r2 - db)
    beita = (beita0, beita1, beita2)

    return ((r, x, y), beita)

def getError(a, b, c1, c2, c3, beita):
    s = c2d(math.pi) * a * b
    (r1,x1,y1) = c1
    (r2,x2,y2) = c2
    (r,x0,y0) = c3
    (b0, b1, b2) = beita

    s0 = 2*(r1*r1*b1 + r2*r2*b2 + r*r*b0 + 
            (r-r1)*(r2-r) * c2d(math.sin(b0)) - (a-r1)*(r2-b))

    error = (s-s0)/s0

    return error

def getChordLen(r, a):
    l2 =  c2d(2)* c2d(r) * c2d(r) * (c2d(1) - c2d(math.cos(a)))
    return l2.sqrt()

def getCR(a, b, emax1, emax2):
    da = decimal.Decimal(a)
    db = decimal.Decimal(b)

    c1 = getR1(da, db, emax1, emax2)
    c2 = getR2(da, db, emax1, emax2)
    (c3, beita) = getR3(da, db, emax1, emax2)

    error = getError(a, b, c1, c2, c3, beita)

    cl1 = getChordLen(c1[0], beita[1])
    cl2 = getChordLen(c2[0], beita[2])
    cl3 = getChordLen(c3[0], beita[0])
    (c1,c2,c3) = (list(c1), list(c2), list(c3))
    c1.append(cl1)
    c2.append(cl2)
    c3.append(cl3)

    return ((c1, c2, c3), error)

def printResult(r, e):
    for item in r:
        print (u'半径: ' + str(item[0]))
        print (u'横坐标: ' + str(item[1]))
        print (u'纵坐标: ' + str(item[2]))
        print (u'弦长: ' + str(item[3]))
        print '--------'
    print (u"面积相对误差:" + str(e))
    
def isDigit(s):
    s = str(s)
    if len(s)> 0 and s[0] == '-':
        s = s[1:]
    for c in s:
        if not c=='.' and not c.isdigit():
            return False
    return True
    
def reInput():
    print(u"非数字，请重新输入")
    print("==========\n")
    return getInput()

def getInput():
    print(u"请输入椭圆长轴长度(-1退出): "),
    major_axis = raw_input()
    if not isDigit(major_axis):
        return reInput()
    if c2d(major_axis) == c2d(-1):
        return (-1, -1, -1)
   
    print(u"请输入椭圆短轴长度: "),
    minor_axis = raw_input()
    if not isDigit(minor_axis):
        return reInput()
        
    print(u"请输入拟合误差: "),
    emax = raw_input()
    if not isDigit(emax):
       return reInput()
    print ("\n")

    return (major_axis, minor_axis, emax)

def main():
    while True:
        major_axis, minor_axis, emax = getInput()
        if major_axis == -1:
            break
        emax1 = emax2 = c2d(emax)
        semi_major_axis = c2d(major_axis)/c2d(2.0)
        semi_minor_axis = c2d(minor_axis)/c2d(2.0)

        (result, error) = getCR(semi_major_axis, semi_minor_axis, emax1, emax2)
        printResult(result, error)
        print ("\n")

if __name__ == "__main__":
    main()
