
# coding: utf-8

# In[1]:

import random
import math
import timeit
import pickle

# In[2]:

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


# In[3]:

def random_new_set(A,n):
    Ap = []
    Ap = Ap + A
    set_flag = True
    while (set_flag):
        set_broj = random.randint(0, n - 1)
        if (not (set_broj in A)):
            zamena = random.randint(0,len(A)-1)
            Ap[zamena] = set_broj
            set_flag = False
    return Ap


# In[4]:

# slucajno generisan graf sa 1000 cvorova

n = 1000  # broj cvorova
with open ('outfile', 'rb') as fp:
    matrica = pickle.load(fp)
for x in range(0, n):
    print x, matrica[x]

# In[5]:

# inicijalizacija nekih podataka
k = 10  # broj elemenata u setu (top k)
d = 2  # broj "skokova" za heuristiku udaljenih cvorova , oni koriste 2 pa cemo i mi
p = 0.05  # verovatnoca da jedan cvor utice na drugi cvor
np = 1 - p  # koristi se cesce nego p
wg = [0,
      0]  # prvi element se zamenjuje drugim elementom da A pretvori u A' racuna se u sash , ali je bitno da je inicijalizovan

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


# In[6]:

#izracunavanje prve ocene
ocena_glavno = sim(matrica, A_glavno, p, 1000)



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
    A_prim = random_new_set(A_glavno, n)
    ocena_prim = sim(matrica, A_prim, p, 1000)

    count += 1
    df = ocena_prim - ocena_glavno

    if df > 0:
        # A <- A'
        ocena_glavno = ocena_prim

        A_glavno = []
        A_glavno = A_glavno + A_prim

        if ocena_glavno > max_ocena:
            max_ocena = ocena_glavno
            max_skup = []
            max_skup = A_glavno
    else:
        xi = random.random()
        if math.exp(df / Tt) > xi:
            # A <- A'
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
ocena = sim (matrica, max_skup, p, 1000)
print(A_glavno)
print 'Vreme izvrsavanja: %.3f' % (stop - start)
print ocena
print max_skup
# In[ ]:



