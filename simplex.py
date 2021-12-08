#
# //TODO Pievienot, ka mainīgie var būt ierobežoti ar kādu no konstantēm, ne 0 vai brīvi
#
# ???
# //TODO Vēl analīze datiem
# ???
#
# //TODO Atrisināt radušos jautājumus saistībā ar duālo problēmu
#

import math
import time
import sys

from numpy.core.fromnumeric import var
from forma import izsauktTab, reztab
import numpy as np
global merkFnKof, dublMerkKof, zime,varzime,optbvrt,bkopija,AtgKoef, maxfn
global IrSub
IrSub = []
merkFnKof = dublMerkKof =  ierob =tabula  =  [],[],[],[]
ieejas = []
vaiIrrez = False
maxfn = 0
varzime = dati = zime = brivmain  =[],[],[],[],[]

# Nepieciešams, ja būs dualā problēma ar transponēto matricu
# kopijazime= []

# izsauc funkciju, kas izveido formu, kur smuki ievadīt datus
dati = izsauktTab()

n = dati[3]
m = dati[4]
zime = dati[5]
mim = dati[6][0]
varzime  = dati[7]
# Tiek izveidots saraksts ar mērķfunkcijas koeficientiem.
merkFnKof = dati[2]

# Tiek ievadītas vektora b vērtības.
ierob = dati[1]

#Ievada vērtības tabulai
tabula = dati[0]
merkis = dati[6][0]
AtgKoef = dati[8]


# Funkcijas, kas nosaka, kādas ir pieļaujamās vektora c koeficentu izmaiņas
# Lai optimālā bāze saglabātos
def coptizm():
    cvertejums = []
    for i in range(0,n):
    
        if i not in ieejas:
            cvertejums.append("delta c_" + str(i+1) + " <= " + str(round(tabula[m][i],3)))
        else:
            if i in brivmain:
                z = "+ "
            elif i>1 and i-1 in brivmain:
                z = "- "
            else:
                z = ""
            novertpoz = []
            novertneg = []

            for ii in range(0,n+m):
                if ii in ieejas:
                    continue

                if (tabula[ieejas[i]][ii]) > 0:
                    novertpoz.append(-1 *  (tabula[m][ii])/(tabula[ieejas[i]][ii]))
                else:
                    novertneg.append(-1 * (tabula[m][ii])/(tabula[ieejas[i]][ii]))

                if len(novertpoz) ==0 :
                    x = "- bezgaliba <"
                else:
                    x = str(round(max(novertpoz),3)) + " <= "
                
                if len(novertneg) == 0:
                    y = " < + bezgaliba"
                else:
                    y = " <= " + str(round(min(novertneg),3))

            cvertejums.append("c-" + str(i+1) + " -tā vērtība ir robežās  " + x + "  " + "delta_c" + str(i+1) + z + y)
    return cvertejums


# Funkcijas, kas nosaka, kādas ir pieļaujamās vektora b koeficentu izmaiņas
# Lai bāzē esošo vektori nemainītos
def boptizm():
    bvertejums = []
    for i in range(0,m):

        # Šeit pēc teorijas sanāk, ka jānobauda tik tas viens
        # Vai gadījumā tas nekrīt laukā
        if n+i in ieejas:
            bvertejums.append("I-" + str(i+1) + "-tais ierobežojums ir robežās   " +"delta_b" + str(i+1) + " => " + str(- round(tabula[i][n+m],3)))
    

        else:
            novertpoz = []
            novertneg = []
            for ii in range(0,m):
                if (tabula[ii][n+i]) > 0:
                    novertpoz.append(-1 *  (tabula[ii][n+m])/(tabula[ii][n+i]))
                else:
                    novertneg.append(-1 * (tabula[ii][n+m])/(tabula[ii][n+i]))

                if len(novertpoz) ==0 :
                    x = "- bezgaliba <"
                else:
                    x = str(round(max(novertpoz),3)) + " <= "
                
                if len(novertneg) == 0:
                    y = " < + bezgaliba"
                else:
                    y = " <= " + str(round(min(novertneg),3))

            bvertejums.append("I-" + str(i+1) + " -tais ierobežojums ir robežās  " + x + "  " + "delta_b" + str(i+1) + " "+ y)

    return bvertejums

# Funkcija atrod, kuri mainīgie ieies bāzē pie b vektora izmaiņām, kuras pārsniedz "normu"
def izmbazee():
    vrtmain = []
    
    for i in range(0,m):
        AtrastJnoVert = []
        indeksuKopa = []
        for j in range(0,m+n):
            if j not in ieejas:
                if tabula[i][j] <= 0 :
                  continue
                else:
                    AtrastJnoVert.append( tabula[i][j] / tabula[m][j])
                    indeksuKopa.append(j)

                indeks = indeksuKopa[AtrastJnoVert.index(min(AtrastJnoVert))]    
        if AtrastJnoVert == []:
            
            # ! Nav info, vai šāds gadījums ir iespējams, bet ja ir, nav skaidrs, vai šāda ir atbilde
            vrtmain.append("Gadījums, kad b maiņas dēļ nemainīsies optimālā bāze ")

        else:
            vrtmain.append("Mainoties b" + str(i+1) + " vērtībai, bāzi pamet: x" + str(ieejas[i]+1) + " ko nomainīs: x" + str(indeks+1) )
    return vrtmain

# Funkija, kas izrēķina optimālā rezultāta vērtību
def optvert(  maxfn):
 
    maxvert = []
    for i in range(0,len(ieejas)):

        if ieejas[i] < n:
            indkol = ieejas[i] 
            maxfn = maxfn +  merkFnKof[ indkol] * tabula[i][n+m]

          #  if ieejas[i] in IrSub:
            maxvert.append( "x_" + str(ieejas[i] +1)+ " = " + str(round(tabula[i][n+m],3) + AtgKoef[ieejas[i]]) )
           # else:
        #    maxvert.append( "x_" + str(ieejas[i] +1)+ " = " + str(round(tabula[i][n+m],3)) )
        else:
            maxvert.append( "x_" + str(ieejas[i]+1 )+ " = " + str(round(tabula[i][n+m],3)) )
    return [maxfn,maxvert]


#Atrod nākamo iterācijas kolonnu!
def atrastKol(vektors,tabula):

    # Pārbauda vai min vērtība ir negatīva
  
    indx = vektors.index(min(vektors))
    
    if vektors[indx] < 0:
        for ii in range(0,m): 
                
               # Ja pie min vērtības, kolonnā ir kaut viena pozitīva vērtība
            if tabula[ii][indx] > 0:

                    # atgriež indexu listei
                    
                    return indx

                    # -2 , ja optimālais atrisinājums ir bezgaliba
                    # Jo pie min indexa nav pozitīvu vērtību
        return -2

            # Atgriež -1, ja atrasts optimāls atrisinājums
    return -1

# Funkcija, kas izveido tabulu

def tabulasIzveide(n,merkFnKof,maxfn):

    # Pārkopē mērķfunkcijas vektora vērtības tabulai
    dublMerkKof = merkFnKof[:]

    # Tiek veiktas substitūcijas, ja 
    # Kāds no mainīgajiem nav ierobežot no lejas ar nulli
    for i in range(0,n):
        # Gadījums, kad mainīgais ir neierobežots
        if varzime[i]== "brivs":
            for ii in range(0,m):
                tabula[ii].insert( i+1,-tabula[ii][i])
            dublMerkKof.insert(i+1,-dublMerkKof[i])
            merkFnKof.insert(i +1,-merkFnKof[i])


            # Gadījumā, ja būs nepieciešams zināt, kuri mainīgie bija brīvi, bez ierob.
           # brivmain.append(i -len(brivmain)  )
            i+=1
            n+=1
            # Gadījums, kad mainīgais ir ierobežot no augšas ar nulli
        elif varzime[i]=="<=":
            for ii in range(0,m):

                IrSub.append(i)

                maxfn = maxfn +  AtgKoef [i] * merkFnKof[i]
                ierob[i] =  ierob[i] - AtgKoef[i] * tabula[i][ii]

                tabula[ii][i] = tabula[ii][i] *-1
            dublMerkKof[i] =    dublMerkKof[i]* -1
            merkFnKof[i]=-merkFnKof[i]

            # Trešais gadījums arī jāapsakta, jo :
            # var  būt no lejas ierobežots ar kādu konstanti
        else:
            for ii in range(0,m):
                IrSub.append(i)
                maxfn = maxfn +  AtgKoef[i] * merkFnKof[i]
                ierob[i] =  ierob[i]  - AtgKoef[i] * tabula[i][ii]

            # Ja nu gadījumā būs nepieciešams zināt, kur bija ierobežot no augšas ar 0
          #  negmain.append(i - len(brivmain))

    # Tālāk tiek pievienoti mākslīgie mainīgie, kas kalpos kā sākuma bāze
    for i in range(0,m):

        if zime[i] == '=':
            dublMerkKof.append(- pow(10,5))
        else:
           
            dublMerkKof.append(0)
        for ii in range(0,m):
            if i==ii:
                if  zime[ii] == '>=':
                    tabula[ii].append(-1)

                else:
                    tabula[ii].append(1)

                ieejas.append(n+ii)

            else:
                tabula[i].append(0)

# Cikls ,kur mērķis ir noteikt, ja gadījumā ,kāda no vektora
# b vērtībām ir negatīva, un ja ir, tad to nevienādību apgriež reizinot ar -1

        if ierob[i] < 0:
            tabula[i].append(ierob[i])

            for j in range(0,n+m):
                tabula[i][j] =   tabula[i][j] * -1
              
        else:

          tabula[i].append(ierob[i])
    

    # Izveido pēdējo rindu, kas noteiks, 
    # Kuras kolonnas tiks ievietotas bāzē
    for j in range(0, len(dublMerkKof)):
          dublMerkKof[j] =   dublMerkKof[j] * -1
    dublMerkKof.append(0)
    tabula.append(dublMerkKof)

    return [dublMerkKof,tabula,n,merkFnKof]


# Notiek tabulas izvede
# Ja nepieciešams maksimizēt mērķfunkciju
if  merkis =='max':
    atb = tabulasIzveide(n,merkFnKof,maxfn)
    n = atb[2]
    dublMerkKof = atb[0]
    tabula = atb[1]
    merkFnKof = atb[3]
        
else:
  
    # ! Aizkomentēts ir variants par dualo problēmu,
    # ! Kur tabulu transponēja

    ''''        

    masivs = np.array(tabula)
    transpose = masivs.T
    tabula = transpose.tolist()
    transpose = masivs =None
    # merkKOef - n
    # ierob - m
    # Es gribu tos samainīt. + visas nevienādības
    dublMerkKof = ierob[:]
    ierob = merkFnKof[:]
    merkFnKof = dublMerkKof[:]

    kopijazime = zime [:]
    zime = []
    for i in range(0,n):
        if varzime[i] == "brivs":
            zime.append("=")
        elif varzime[i] == "<=":
            zime.append( ">=")
        else:
            zime.append("<=")
    varzime = []
    for i in range(0,m):
        if kopijazime[i] == ">=":
            varzime.append( ">= 0")
        elif kopijazime[i] == "<=":
            varzime.append("<= 0")
        else:
            varzime.append("brivs")
    n,m = m,n
 
'''   
# Gadījums, kad nepieciešams minimizēt mērķfunkciju
# Tās koeficenti tiek reizināti  ar -1
# Iegūstot duālo problēmu, kuru nepieciešams maksimizēt
    for i in range(0, len(merkFnKof)):
        merkFnKof[i] = merkFnKof[i] * -1

    atb = tabulasIzveide(n,merkFnKof)
    n = atb[2]
    dublMerkKof = atb[0]
    tabula = atb[1]
    merkFnKof = atb[3]


# Funckija, kurā notiek Gausa eliminācija
def vvizveide():
    # izdala jauno kolonnu ar ieejoša vektora vērtību
    x = tabula[rinda][kolind]
    for  i in range(0,m+n+1):
        tabula[rinda][i] =   tabula[rinda][i] / x
   

    # Kolonna pārējās rindas nonullē
    for i in range(0, m+1):
        if i != rinda:
            if tabula[i][kolind] != 0:
                a = tabula[i][kolind]
                for j in range(0,m+n+1):
                    tabula[i][j] = tabula[i][j] + tabula[rinda][j] * (-a)


# Atrod nākamo rindu, kas ieiet bāzē
def NkmaIeja(minvert):
    for i in range(0,m):
        if tabula[i][kolind] > 0:
           
            if (minvert > tabula[i][n+m]/ abs(tabula[i][kolind])):
                minvert = tabula[i][n+m]/ abs(tabula[i][kolind])
                
                rinda = i

    ieejas[rinda ]= kolind
    dublMerkKof = tabula[m]
    return rinda
while True:


# Pārbauda vai ir atrast optimālais rezultāts
#  Vai arī optimālā rezultāta nav 

    kolind = atrastKol(dublMerkKof,tabula)

    if kolind == -1:
        print("Ir atrasts optimālais rezultāts")
        vaiIrrez = True
        break
    elif kolind == -2:
        print("Problēmas optimālais atrisinājums ir bezgalība. Līdz ar to, problēmai neeksistē atrisinājums")
        vaiIrrez = False
        break

# Minvert ir mainīgais, kuru lieto, lai atrastu bāzē ieejošo rindu/kolonnu
    minvert = pow(10,3)



# Nosaka, kurš mainīgais nākamais ieiet bāzē
    rinda = NkmaIeja(minvert)

     #  *     a-ij (ieejošais) ir nosaukts kā minvert
     #  *     rinda - rinda, kolonna - kolind



# Lietojot Gausa eliminācijas procesu, ieejošo kolonnu/rindu pārtaisa kā vienības vektoru vektoru e_i
    vvizveide()
    
    
       


# Ja ir atrast optimālais rezultāts, izreiķina tā vērtību
if vaiIrrez == True:

    cvertejums = []
    bvertejums = []
    bazmaina = []
    maxvert = []
    # Tiek izrēķināts optimālais rezultāts
    maxfn,maxvert = optvert(maxfn)

    cvertejums = coptizm()
    bvertejums = boptizm()
    bazmaina = izmbazee()
        
   
    reztab(cvertejums,bvertejums,maxfn,maxvert,bazmaina)

