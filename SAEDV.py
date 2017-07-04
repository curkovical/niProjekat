
# coding: utf-8

# In[16]:

import random
import math
import timeit
import pickle

# In[17]:

def SAEDV(mat, A, Ap, w, NB, rv, pro):
    w1 = w[0]
    w2 = w[1]
    if (w2 in A):
        ocena = len(A)
        for x in NB:
            if (not (x in A)):
                ocena = ocena + (1 - pow(pro, rv[x]))
    else:
        for x in mat[w1]:
            if (rv[x] == 1):
                NB.remove(x)
            rv[x] = rv[x] - 1
        for x in mat[w2]:
            if (rv[x] == 0):
                NB.append(x)
            rv[x] = rv[x] + 1

        ocena = len(Ap)
        for x in NB:
            if (not (x in Ap)):
                ocena = ocena + (1 - pow(pro, rv[x]))

    return ocena


# In[18]:

def random_new_set(A,n,w):
    Ap = []
    Ap = Ap + A
    set_flag = True
    while (set_flag):
        set_broj = random.randint(0, n - 1)
        if (not (set_broj in A)):
            zamena = random.randint(0,len(A)-1)
            Ap.remove(A[zamena])
            Ap.append(set_broj)
            set_flag = False
            w[0] = A[zamena]
            w[1] = set_broj
    
    return Ap


# In[19]:

# slucajno generisan graf sa 1000 cvorova

n = 1000  # broj cvorova
with open ('outfile', 'rb') as fp:
    matrica = pickle.load(fp)
for x in range(0, n):
    print x, matrica[x]


# inicijalizacija nekih podataka
k = 30  # broj elemenata u setu (top k)
d = 2  # broj "skokova" za heuristiku udaljenih cvorova , oni koriste 2 pa cemo i mi
p = 0.05  # verovatnoca da jedan cvor utice na drugi cvor
np = 1 - p  # koristi se cesce nego p
wg = [0, 0]  # prvi element se zamenjuje drugim elementom da A pretvori u A' racuna se u sash , ali je bitno da je inicijalizovan

A_glavno = []  # inicijalizuje prvi skup 
for x in range(0, k):
    gen_flag = True
    while (gen_flag):
        gen_broj = random.randint(0, n - 1)
        if (not (gen_broj in A_glavno)):
            A_glavno.append(gen_broj)
            gen_flag = False

print (A_glavno)

A_prim = []  # ovde cemo cuvati promenjenji skup (A') za slucaj da ga zamenimo sa A

ocena_glavno = 0
ocena_prim = 0

NB_glavno = []  # koriste se za SAEDV , i menja se u toku rada algoritma
NB_prim = []  # prim cuvamo za slucaj da dodje do promene A' i A , funkciju pozivamo sa NB_prim i rv_prim
rv_glavno = []
rv_prim = []


# In[21]:

# inicijalizacija za SAEDV funkciju , takodje racuna sigma(A) - ocena na pocetku

NB_glavno = NB_glavno + A_glavno
for x in A_glavno:
    for y in matrica[x]:
        if (not (y in NB_glavno)):
            NB_glavno.append(y)

for x in range(0, n):
    if (x in NB_glavno):
        dodatak = 0
        for y in A_glavno:
            for z in matrica[y]:
                if (z == x):
                    dodatak = dodatak + 1
        rv_glavno.append(dodatak)
    else:
        rv_glavno.append(0)

ocena_glavno = len(A_glavno)
for x in NB_glavno:
    if (not (x in A_glavno)):
        ocena_glavno = ocena_glavno + (1 - pow(np, rv_glavno[x]))


# In[ ]:




# In[22]:

T0 = 10000
Tf = 1000
deltaT = 500
q = 100
t = 0
Tt = T0
count = 0
max_ocena = 0
max_skup = []

start = timeit.default_timer()

while Tt > Tf:
    A_prim = random_new_set(A_glavno,n,wg)
    NB_prim = []
    NB_prim = NB_prim + NB_glavno
    rv_prim = []
    rv_prim = rv_prim + rv_glavno
    ocena_prim = SAEDV(matrica, A_glavno, A_prim, wg, NB_prim, rv_prim, np)

    count += 1
    df = ocena_prim - ocena_glavno

    if df > 0:
        # A <- A'
        NB_glavno = []
        NB_glavno = NB_glavno + NB_prim
        rv_glavno = []
        rv_glavno = rv_glavno + rv_prim
        ocena_glavno = ocena_prim
        if ocena_glavno > max_ocena:
            max_ocena = ocena_glavno
            max_skup = []
            max_skup = A_glavno

        A_glavno = []
        A_glavno = A_glavno + A_prim
    else:
        xi = random.random()
        if math.exp(df / Tt) > xi:
            # A <- A'
            NB_glavno = []
            NB_glavno = NB_glavno + NB_prim
            rv_glavno = []
            rv_glavno = rv_glavno + rv_prim
            ocena_glavno = ocena_prim

            A_glavno = []
            A_glavno = A_glavno + A_prim

            if ocena_glavno > max_ocena:
                max_ocena = ocena_glavno
                max_skup = []
                max_skup = A_glavno

    if count > q:
        print ('Tt: ', Tt)
        print (A_glavno)
        print (ocena_glavno)
        Tt = Tt - deltaT
        t = t + 1
        count = 0

stop = timeit.default_timer()


# In[23]:

def sim(mat, A , pro, broj_simulacija):
    suma = 0
    for brojac in range (1 , broj_simulacija):
        lista_aktivnih = []
        lista_aktivnih = lista_aktivnih + A
        for x in lista_aktivnih:
            for y in mat[x]:
                if (not (y in lista_aktivnih)):
                    sansa = random.random()
                    if (sansa < pro):
                        lista_aktivnih.append(y)
        suma = suma + len(lista_aktivnih)
    
    return (suma / broj_simulacija)


ocena = sim (matrica, max_skup, p, 1000)
print 'Ocena: ', ocena
print 'Vreme izvrsavanja: %.3f sekundi' % (stop - start)
print max_skup

# In[ ]:



