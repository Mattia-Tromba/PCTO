gusti = ["banana", "cioccolato", "limone", "pistacchio", "mirtillo", "fragola", "vaniglia"]
c = 0
for x in range (len(gusti)):
    for y in range (len(gusti)):
        if gusti[y] != gusti[x] and y>=c:
            print(gusti[x] + ", " + gusti[y])
    c+=1