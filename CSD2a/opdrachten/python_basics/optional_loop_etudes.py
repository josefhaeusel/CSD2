"""
_____________________ Etude 1 _____________________
Use one forloop to generate a list with the following indices
10, 13, 16, 19, 22, 25, 28, ...
"""
list = []
for x in range(10):
    y = 10+3*x
    list = list + [y]
    print(list)


"""
_____________________ Etude 2 _____________________
Use one forloop to generate a list with the following indices
0, 2, 4, 6, 8, 10, 12, 14, 16, ...
"""
list = []
for x in range(10):
    y = 2*x
    list = list + [y]
    print(list)

"""
_____________________ Etude 3 _____________________
Use one forloop to generate a list with the following indices
0, 2, 4, 6, 8, 10, 0, 2, 4, 6, 8, 10, 0, 2, ...
"""

list = []
for x in [0,2,4,6,8,10]*10:
    list = list + [x]
    print(list)




    


"""
_____________________ Etude 4 _____________________
Use a double forloop to generate a list with the following indices
0, 2, 4, 6, 8, 10, 0, 2, 4, 6, 8, 10, 0, 2, ... # repeat sublist n times
"""
list=[]
for _ in range(10):
    for x in range(6):
        y = 2*x
        list = list + [y]
    print(list)


"""
_____________________ Etude 5 _____________________
Use while loop to generate a list with the following indices.
tip: use a multiplication of -1 at certain moments
0, 2, 4, 6, 8, 10, 8, 6, 4, 2, 0, 2, 4, 6, 8, 10, 8, ... # repeat sublist n times
"""

n = 3
list = []
i = 0
direction = 1

while len(list) < n*10:
    list.append(i)
    i += direction *2
    if i == 10 or i == 0:
        direction *= -1
print(list)
    


