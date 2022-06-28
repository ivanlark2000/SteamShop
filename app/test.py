import random

lst = list(range(50))
while len(lst) != 0:
    rez = random.choice(lst)
    lst.remove(rez)
    print(rez)

