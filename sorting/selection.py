def ordinamento(x):
    a, b, c = 0, 0, 0
    print(x)
    while a < len(x):
        while b < len(x):
            if x[c] > x[b]:
                c=b
            b += 1
        x[a], x[c] = x[c], x[a]
        print(x)
        a +=1
        c = a
        b = a+1

lista=[97,54,76,1,5]
ordinamento(lista)
