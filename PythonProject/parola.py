def longest_word(x):
    sequenza=x.split()
    lungo = ""
    print(sequenza)
    for x in range (len(sequenza)):
        if len(sequenza[x]) > len(lungo):
            lungo = sequenza[x]
    print(lungo)
stringa=input()
if stringa != "":
    longest_word(stringa)
else:
    print("hai inserito un valore non valido")