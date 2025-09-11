def distanza (x):
    minimo = x[0]
    massimo = x[0]
    for z in range(len(x)):
        if minimo > x[z]:
            minimo = x[z]
        if massimo < x[z]:
            massimo = x[z]
    print(massimo)
    print(minimo)
    risultato = massimo - minimo
    print("distanza più grande = %f " %risultato)
lista=[1,2,3,2.5,3.5,120, -10000]
distanza(lista)