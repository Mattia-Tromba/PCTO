l = [23, 11, 3, 17, 29, 1, 64]

def ordinal (lista):
    k=0
    for x in range(len(lista)-1):
        for y in range(x+1, len(lista)):
            if lista[y] < lista[k]:
                k = y
        lista[x], lista[k] = lista[k], lista[x]
        print(lista)
        k=x+1
    return lista

ordinal(l)