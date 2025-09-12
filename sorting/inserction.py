l = [23, 11, 3, 17, 29, 1, 64]

def sort(lista):
    for x in range(len(lista)-1):
        y = x+1
        while y != 0:
            if lista[y] >= lista[y-1]:
                y = 1
            else:
                lista[y], lista[y - 1] = lista[y - 1], lista[y]
            print(lista)
            y-=1
    return lista
print(sort(l))