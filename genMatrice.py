import random
import pickle

n = 1000  # broj cvorova
procenat_grane = 0.01  # veovatnoca za svaki cvor da ima granu ka drugom cvoru (po svakom cvoru)
matrica = []

for x in range(0, n):
    matrica.append([])
    for y in range(0, x):
        if (random.random() < procenat_grane):
            matrica[x].append(y)
    for y in range(x + 1, n):
        if (random.random() < procenat_grane):
            matrica[x].append(y)

for x in range(0, n):
    print matrica[x]


with open('outfile', 'wb') as fp:
    pickle.dump(matrica, fp)
