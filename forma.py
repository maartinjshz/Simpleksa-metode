import tkinter as tk

global dati 
dati = []
global tabula,Atab, vek,Bvek, kof,Ckof,taskm,varier,varzim, IerobKoef,AtgKoef
AtgKoef = []
taskm = []
tabula = []
vek = []
Bvek = []
kof = []
Ckof = []
Atab = []
zime = []
varier=[]
variable = []
varzim = []

# Izveido formu, kurā tiek ievadīti funkciju dati 
def tabulas(n,m):
    IerobKoef = []
    tabula = []
    tab=tk.Tk()
    tab.geometry( '400x300')

    label1 = tk.Label(tab, text="Ievadīt Mērķfunkcijas koeficentus" )
    label1.place(x= 30, y =10)



    label1 = tk.Label(tab, text="Ievadīt ierobežojošo funkciju vērtības" )
    label1.place(x= 30, y =65)
    for i in range(0,m):
        tabula.append([])
        for j in range(0,n):

        # Izveido tabulu, kurā ieraksta ierobežojošo funkciju vērtības
            textbox = tk.Entry( tab)
            textbox.place(x=10+55*j, y= 90+20*i, width=40, height = 20)
            tabula[i].append(textbox)
            label = tk.Label(tab, text="x" + str(j+1))
            label.place(x=40+55*j, y= 90+20*i)


        # Uztaisa dropdownus, kur izvēlēties nevineādību/vienādību
        variable.append("") 
        variable[i] = tk.StringVar( tab)  
        variable[i].set("<=") # default value
        w = tk.OptionMenu( tab, variable[i], ">=", "=", "<=")
        w.place(x=65+55*j, y= 90+20*i, width=50, height = 20)

        # Pēdējā kolonna ar vektora b vērtībām
        vettext = tk.Entry(tab)
        vettext.place(x=120+55*j, y= 90+20*i, width=40, height = 20)
        vek.append(vettext)

    for i in range(0,n):
        
        # Izveido ridnu, kur ievadīt mērķfunkciju datus

        koftxtbox= tk.Entry( tab)
        koftxtbox.place(x=10+55*i, y= 30, width=40, height = 20)
        kof.append(koftxtbox)
        label = tk.Label(tab, text="x" + str(i+1))
        label.place(x=40+55*i, y= 30)

        

        labels = tk.Label(tab, text="x" + str(i+1))
        labels.place(x=20+110*i, y=  110 + 20*m)

# Šeit norāda, kā tiek ierobežoti mainīgie
        varier.append("")
        varier[i]=tk.StringVar(tab)
        varier[i].set(">= ") # Def vērt.
        s = tk.OptionMenu(tab,varier[i], ">= " ,"<= ", "brivs")
        s.place(x=35+110*i, y= 110 + 20*m, width=60, height = 20)

        # Pievieno logus, kur ierakstīt vērtības, ar kurām ierobežo -  IerobKoef[]
        textbox = tk.Entry( tab)
        textbox.place(x=95+110*i, y= 110 + 20*m, width=40, height = 20)
        IerobKoef.append(textbox)



    # Izvēlne, vai dotā ir minimizācijas vai maksimizācijas problēma
    labelm = tk.Label(tab, text="Izvēlē vai dotā ir minimizācijas vai maksimizācijas metode")
    labelm.place(x=10, y= 140+20*m)
    mima= tk.StringVar( tab)  
    mima.set("max") # default value
    mm = tk.OptionMenu( tab, mima, "max", "min")
    mm.place(x=10, y= 170+20*m, width=80, height = 20)

# Ievadītos datus ievieto sarakstos, lai atgriestu rēķināšanai

    def vert():
        taskm.append(mima.get())

        for i in range(0,m):
            Atab.append([])
            for j in range(0,n):

                x = tabula[i][j].get()
                if x == "":
                    Atab[i].append(0)
                else:
                    Atab[i].append(int(x))

            x = vek[i].get()
            if x =="":
                Bvek.append(0)
            else:
                Bvek.append( int(x))

            zime.append(variable[i].get())

        for i in range(0,n):
            
            x = kof[i].get()
            if x =="":
                Ckof.append(0)
            else:
                Ckof.append( float(x))
            varzim.append(varier[i].get())

        # Paņem no logiem IerobKoef vērtības
            if IerobKoef[i].get() == "":
                AtgKoef.append(0)
            else:
                AtgKoef.append(int(IerobKoef[i].get()))
        
        tab.destroy()  


   

    button = tk.Button(text='Ievadīt', command=vert)
    button.place(x= 10,y=200 +20*m)

    tab.mainloop()   

# izveido formu, kur iegūst n un m vērtības

def vertab():
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 400, height = 300)
    canvas1.pack()

    label1 = tk.Label(root, text= 'Ievadīt mainīgo skaitu')
    canvas1.create_window(200, 25, window=label1)

    entry1 = tk.Entry (root) 
    canvas1.create_window(200, 75, window=entry1)

    label2 = tk.Label(root, text= 'Ievadīt funkciju skaitu')
    canvas1.create_window(200, 150, window=label2)

    entry2 = tk.Entry (root) 
    canvas1.create_window(200, 200, window=entry2)
    def Vertibas():  
    
       dati.append( int(entry1.get()))
       dati.append( int(entry2.get()))
       root.destroy()     
      
        
    button1 = tk.Button(text='Ievadīt', command=Vertibas)
    canvas1.create_window(200, 250, window=button1)
    root.mainloop()


# forma, kur tiek parādīti gala rezultāti
def reztab(cvert,bvert,maxfn,maxvert, baziz):
    reztb = tk.Tk()
    canvas1 = tk.Canvas(reztb, width = 640, height = 480)
    canvas1.pack()
    cgar = len(cvert)
    bgar = len(bvert)
    izmgar = len(baziz)
    label = tk.Label(reztb, text = "Optimālais rezultāts: " + str(maxfn))
    label.place(x=30, y=20)
    for i in range(0,len(maxvert)):
    
        label = tk.Label(reztb, text=maxvert[i] )
        label.place(x=30+ 80*i, y= 40)

    label = tk.Label(reztb, text = "Robežas, kādās var mainīt mērķfunkcijas c vērtības, lai nemainītos bāzē esošo skaitļu vērtības:")
    label.place(x=30, y=60)
    for i in range(0,len(cvert)):
    
        label = tk.Label(reztb, text=cvert[i] )
        label.place(x=30, y= 80+20*i)
    label = tk.Label(reztb, text = "Robežas, kādās var mainīt b vērtības, lai optimālā rezultāta bāze nemainīgtos:")
    label.place(x=30, y= 85+cgar*20)
    bsak = 110+cgar*20
    for i in range(0,bgar):
        label = tk.Label(reztb, text=bvert[i])
        label.place(x=30, y= bsak+20*i)

    izmsak = 110 + (cgar+bgar+1)* 20
    label = tk.Label(reztb, text = "Bāzes maiņa pievektora b izmaiņām:")
    label.place(x=30, y= 85+(bgar +cgar+1)*20)
    bsak = 110+cgar*20
    for i in range(0,izmgar):
        label = tk.Label(reztb, text=baziz[i])
        label.place(x=30, y=  izmsak+20*i)
    

    reztb.mainloop() 

#funckija, kas tālā izsauc funkcijas datu ievadei
def izsauktTab():
    vertab()
    tabulas(dati[0],dati[1])
    return [Atab,Bvek,Ckof, dati[0],dati[1],zime, taskm, varzim,AtgKoef]
