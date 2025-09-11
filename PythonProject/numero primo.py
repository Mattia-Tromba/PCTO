def isprimo(x):
    a=0
    z = 2
    while a != 1 and z<x:
        if x % z == 0:
            a=1
        z += 1
    if a==1:
        return False
    else:
        return True

def numeri(x):
    y=2
    trovato=0
    while trovato != x :
        if isprimo(y):
            print (y)
            trovato +=1
        y+=1

numeri(8)