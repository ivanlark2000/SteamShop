import random

lst = list(range(50))
while lst:
    rez = random.choice(lst)
    lst.remove(rez)
    print(rez)

