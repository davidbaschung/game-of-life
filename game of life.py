# code créé dans le cadre des cours d'option complémentaire informatique du gymnase français de Bienne, en Avril 2013.
# créé par David Baschung


from tkinter import *
import random

def out(event) : fen.destroy() ### (quitter)

def debut_event(event) :    ### permet de recommencer le jeu à l'aide de touches (automate désactivé)
    global chk1
    if chk1.get()==0 or chk1.get()==1 and chk3.get()==1: debut() #vérifie que le processus automatique soit désactivé, ou qu'il se soit arrêté automatiquement à la fin
def move_event(event) :     ### permet de passer à l'étape suivante à l'aide de touches (automate désactivé)
    global chk1
    if chk1.get() != 1 : move() # vérifie que l'automate ne soit pas activé
def f_AutoWork_event(event) :   ### active la fonction f_AutoWork à l'aide de touches
    global speed,chk1
    if chk1.get() == 0 : chk1.set(1)    # coche le checkbutton de l'automate
    elif chk1.get() == 1 : chk1.set(0)  # décoche le checkbutton
    fen.after(speed,f_AutoWork)         # active enfin la fonction
    
def debut() :   ### fonction générant un nombre aléatoire de cellules au début de chaque jeu/session
    global g,can,total,oldTotal1,oldTotal2,oldTotal3,oldTotal4,oldTotal5, speed,oval,alive_color, dead_color, ColorMode, percents, mem_replay
    textstatus.config(text = "  NEW GAME  ",fg="black",bg="white")      # statut du processus (indication texte)
    oldTotal5,oldTotal4,oldTotal3,oldTotal2,oldTotal1 = -5,-4,-3,-2,-1  # réinitialise les variables stockant les résultats sur 5 étapes
    if chk2.get() == 1 : ColorMode = True   # établit un mode multicolore ou non (checkbutton)
    else : ColorMode = False                #
    if ColorMode :                          #
        multicolor()                        # accède à la fonction générant des couleurs
    for y in range(1,11) :                          # pour chaque cellule, chaque ligne,
        for x in range(1,11):                       # et chaque colonne
            hasard = random.randint(0,100)          # génère aléatoirement si la cellue est vivante
            if hasard< 100-percents : g[y][x] = 0   # selon un pourcentage donné par l'utilisateur
            else : g[y][x] = 1                      # et la variable indiquant la vie sera stockée dans une liste, regroupant toutes les cellules
            can.itemconfig(oval[y][x],fill=colorcircle(g[y][x],ColorMode)) # utilise la fonction des couleurs, avec paramètre du mode multicolore ##################### la fonction itemconfig agit comme config mais pour des éléments d'un Canvas. Ici, les cercles ont déjà étés créés lors du lancement du programme et utiliser ce système au lieu de create_oval évite de créer indéfiniment des variables qui prennent de la mémoire et finissent par ralentir le programme. Le premier paramètre donne l'objet à configuer.
            mem_replay[y][x] = g[y][x]              # à chaque début de jeu, la liste aléatoire générée sera stockée dans une autre liste pour pouvoir repasser la séquence sur demande (Button)
    if chk1.get() == 1 : fen.after(speed,move)      # après chaque début de jeu, on redirige vers la fonction move qui changera d'étape en boucle
def move() : ### étapes
    global g,f,can,total,oldTotal1,oldTotal2,oldTotal3,oldTotal4,oldTotal5, speed,oval,chk1,ColorMode,move_mode_status,chk3
    textstatus.config(text = "   Processing   ",fg="white",bg="black")
    f = []  # crée une variable de copie afin de traiter les nouveaux résultats à partir des anciens
    for i in g : f.append(i[:]) #copie
    oldTotal5 = oldTotal4 # à chaque étape, on stocke les 5 derniers résultats pour vérifier qu'une suite d'étapes se répétant à l'infini n'est pas en cours
    oldTotal4 = oldTotal3
    oldTotal3 = oldTotal2
    oldTotal2 = oldTotal1
    oldTotal1 = total
    total     = 0   
    for y in range(1,11) :
        for x in range(1,11):               # calcule le nombre de voisins de chaque cellule
            voisin = 0
            if g[y-1][x-1] == 1 : voisin += 1
            if g[y-1][x]   == 1 : voisin += 1
            if g[y-1][x+1] == 1 : voisin += 1
            if g[y][x-1]   == 1 : voisin += 1
            if g[y][x+1]   == 1 : voisin += 1
            if g[y+1][x-1] == 1 : voisin += 1
            if g[y+1][x]   == 1 : voisin += 1
            if g[y+1][x+1] == 1 : voisin += 1
            if move_mode_status == 'invasion' :     # mode qui choisit si une cellule est vivante d'après un grand nombre de voisins
                if voisin >= 3 : f[y][x] = 1
                if voisin <= 1 : f[y][x] = 0
                if voisin == 2 : f[y][x] = g[y][x]
            if move_mode_status == 'traditional' :  # mode traditionnel qui choisit si une cellule est vivante selon les règles établies à l'origine
                if voisin > 3 or voisin <= 1 : f[y][x] = 0
                if voisin == 3 : f[y][x] = 1
                if voisin == 2 : f[y][x] = g[y][x]
            if f[y][x] == 1 : total += 1
            can.itemconfig(oval[y][x],fill=colorcircle(f[y][x],ColorMode))
    g = []                      # on stocke les résultats modifiés comme nouveaux vrais résultats
    for i in f : g.append(i[:]) # copie
    if not total==oldTotal5:        # afin d'éviter une suite d'étape à l'infini, on compare les anciens résultats aux nouveaux
        if chk1.get() == 1 :        # si l'automate est activé__________________________#
            if total != 100 and total != 0 : fen.after(speed,move)                      #   on passe
            if (total == 100 or total == 0) and chk3.get() == 0 : fen.after(speed,debut)#
    if total==oldTotal3: textstatus.config(text="YOU HAVE ENTERED INTO AN INFINITE LOOP",fg="black",bg="#%02x%02x%02x" % (255,255,50))
    if total==oldTotal5:                        # si on a une suite infinie
        if chk1.get() == 1 and chk3.get() == 0: # que l'automate est activé et que le processus ne se met pas en pause à la fin
            fen.after(speed,debut)              # on recommence

def colorcircle(v,ColorMode_test): ### cette fonction définit le choix d'une couleur d'après les paramètres : (vie, mode couleurs aléatoires ou non)
    global alive_color, dead_color
    if not ColorMode_test :     #-mode multicolore désactivé :
        if v == 1 :
            return "green"      # vivant = vert
        else :
            return "dark red"   # mort = rouge
    if ColorMode_test :         #-mode multicolore activé :
        if v == 1 :
            return alive_color  # retourne la couleur 'vivant' générée aléatoirement au début de la session
        else :
            return dead_color   # retourne la couleur 'mort'     générée aléatoirement au début de la session

        
def light_can(event) : ### fonction affichant une grille de zones à cliquer lors du passage de la souris sur le Canvas
    global lines_ver,lines_hor
    for i in range(0,9) :
        can.itemconfig(lines_hor[i],fill='light grey')
        can.itemconfig(lines_ver[i],fill='light grey')
def unlight_can(event) : ### fonction effaçant la grille
    for i in range(0,9) :
        can.itemconfig(lines_hor[i],fill='black')
        can.itemconfig(lines_ver[i],fill='black')
        
def SpeedScale_command(event) : ### fonction calculant la vitesse , personnalisée à partir de la position horizontale d'une échelle
    global speed
    ScaleX = SpeedScale.get()
    LabelSpeed = -1/ScaleX*1000
    speed = int(float(LabelSpeed)*1000)
    SpeedScale.config( label=("Intervals speed (in seconds)  ",str(LabelSpeed)) ) #affichage de la vitesse dans : le texte de l'échelle

def f_AutoWork() : ### fonction du checkbutton de l'automate
    global total,oldTotal5, speed, g, mem_replay ,chk3
    if chk1.get() == 1 : #lorsqu'on active le checkbutton, il faut relancer 'debut' ou 'move', car pour arrêter ces fonctions, on n'a pas rempli leurs conditions de relancement
        for y in range(1,11) :
            for x in range(1,11):
                mem_replay[y][x] = g[y][x]
        if not total==oldTotal5:
            for i in f : g.append(i[:])
            if total != 100 and total != 0 : fen.after(speed,move)
            if total == 100 or total == 0 : fen.after(speed,debut)
        else :
            textstatus.config(text="YOU HAVE ENTERED INTO AN INFINITE LOOP",fg="black",bg="#%02x%02x%02x" % (255,255,50))
            if chk3.get() == 0 : fen.after(speed,debut)

def f_move_mode() : ### modifie le type de traitement des listes lors des étapes + le texte du bouton
    global move_mode_status
    if move_mode_status == 'invasion' :
        move_mode_status = 'traditional'
        move_mode.config(text='                                  toogle to INVASION evolution mode                                   ')
    elif move_mode_status == 'traditional' :
        move_mode_status = 'invasion'
        move_mode.config(text='                              toogle to TRADITIONAL evolution mode                                ')

def f_percentage(event) : ### reçoit le chiffre entré par l'utilisateur dans la zone d'entrée, et l'utilise comme pourcentage approximatif 
    global percents
    percentage.config(bg='light grey',fg='black')
    
    text = list(percentage.get())
    if text[len(text)-1] == '%' : percentage.delete(len(text)-1,len(text))
##        del(text[len(percentage.get())-1])
    
##    text2 = "".join(text)
    try :
        text = int(percentage.get())
        percents = text
    except ValueError :
        percentage.config(bg='red',fg='white')
        percentage.insert(0,'please enter a VALID value, thanks!')
    if percents>100 or percents<0 :
        percentage.insert(0,'please enter a VALID value, thanks!')
        percentage.config(bg='red',fg='white')
    percentage.insert(END,'%')
    percentage.icursor(len(percentage.get())-1)

def multicolor() : ### crée les couleurs aléatoires de chaque session
    global alive_color, dead_color
    a1,a2,a3 = random.randint(0,2),random.randint(0,2),random.randint(0,2)
    d1,d2,d3 = random.randint(0,2),random.randint(0,2),random.randint(0,2)
    if a1==a2 and a1==a3 : a1,a2,a3 = random.randint(0,2),random.randint(0,2),random.randint(0,2)
    if d1==d2 and d1==d3 : d1,d2,d3 = random.randint(0,2),random.randint(0,2),random.randint(0,2)
    alive_color = "#%02x%02x%02x" % (150+50*a1,150+50*a2,150+50*a3) #stock
    dead_color = "#%02x%02x%02x" % (50*d1,50*d2,50*d3)

def mouse_color(event) :
    global g, ColorMode, chk1,total 
    chk1.set(0)
    x,y = event.x,event.y
    l_hor,l_ver = int(y/45),int(x/45)
    if g[l_hor][l_ver] == 1 : g[l_hor][l_ver] = 0
    elif g[l_hor][l_ver] == 0 : g[l_hor][l_ver] = 1
    if g[l_hor][l_ver] == 0 or g[l_hor][l_ver] == 1 : can.itemconfig(oval[l_hor][l_ver],fill=colorcircle(g[l_hor][l_ver],ColorMode))
    total = 999 #permettra d'éviter des confuisions si chk3 est coché et qu'on accède à f_autoword pour reprendre après avoir dessiné

def delete_can(event) : ### tue toutes les cellules
    global can, g
    for y in range(1,11) :
        for x in range(1,11):
            g[y][x] = 0
            can.itemconfig(oval[y][x],fill=colorcircle(g[y][x],ColorMode))

def replay_command() : ### fonction du bouton repassant une séquence
    global speed,chk1,chk3
    total = 999
    chk1.set(0) # désactive l'automate (pour éviter des fonctions parallèles)
    chk3.set(1) # arrêter la séquence à la fin
    fen.after(speed,replay_command_2)
def replay_command_2() :
    global mem_replay,g,can,chk1,textstatus
    for y in range(1,11) :
        for x in range(1,11):
            g[y][x] = mem_replay[y][x]
            can.itemconfig(oval[y][x],fill=colorcircle(g[y][x],ColorMode))
    textstatus.config(text='           REPLAY           ',bg='blue',fg='white')
    chk1.set(1) # réactive l'automate
    f_AutoWork() # accède au redémarrage de l'automate

def f_geo_button() : ### redimensionne la fenêtre
    global frame_total, geo_button,geo_button_var
    if  geo_button_var == 'L' :
        geo_button_var = 'R'
        frame_total.grid(column=2,row=1,padx=4)
        fen.geometry("%dx%d%+d%+d" % (1020,566,0,0))
        fen.title("David Baschung 2013                            The game of life                                                                                                                                                           ESCAPE to Quit")
        geo_button.config(text='    __ \n    I   I \n   __I   I__ \n  \        / \n  \    / \n V')
    elif geo_button_var == 'R' :
        geo_button_var = 'L'
        frame_total.grid(column=0,row=2)
        fen.geometry("%dx%d%+d%+d" % (602,723,0,0))
        fen.title("David Baschung 2013                            The game of life                            ESCAPE to Quit")
        geo_button.config(text='_____I\ \nI            \ \nI_____    / \n       I/')

def f_stop_sequence() : ### checkbutton pour arrêter l'automate si suite infinie, tout vivant ou tout mort
    global total,oldTotal5,chk3,speed
    if total == 0 or total == 100 or oldTotal5 == total and chk3.get() == 0 : fen.after(speed,debut)
    
fen = Tk()
fen.title("David Baschung 2013                            The game of life                            ESCAPE to Quit")
fen.config(bg='black')
fen.geometry("%dx%d%+d%+d" % (602,723,0,0))
fen.bind('<Escape>',out)
#
textstatus = Label(fen,text = "",bg="white") 
textstatus.grid(column=0,row=0)
frame_total = Frame(fen) # Frame globale contenant des widgets et d'autres frames, pour redimenssionner la fenêtre
frame_total.grid(column=0,row=2)
SpeedScale = Scale(frame_total,from_ = -5000, to = -250, orient=HORIZONTAL, label="", length=398, showvalue=0, command = SpeedScale_command, highlightbackground="grey",bd=3)
SpeedScale.set(-1000)
SpeedScale.grid(column=0,row=2)
frame1 = Frame(frame_total)
frame1.grid(row=3,column=0)
chk1 = IntVar()
chk1.set(1)
AutoWork = Checkbutton(frame1,text="Automatic work (UP:new,R:nxt)",variable=chk1,command=f_AutoWork)
AutoWork.pack(side=LEFT)
chk2 = IntVar()
Mcolor = Checkbutton(frame1,text='Multicolor mode (wait next session)',variable=chk2)
Mcolor.pack()
ColorMode, alive_color, dead_color = False,"green","dark red" # choix mode multicolore, couleurs multicolore vivant et mort
frame2 = Frame(frame_total)
frame2.grid(column=0,row=4)
move_mode = Button(frame2,text='                              toogle to TRADITIONAL evolution mode                                ',command=f_move_mode,bg="light grey")
move_mode.pack()
move_mode_status = 'invasion'
frame3 = Frame(frame_total)
frame3.grid(column=0,row=5)
TextEntry = Label(frame3,text=' Average alive cells percentage when starting a session : (valid with "Enter")  ')
TextEntry.pack()
percentage = Entry(frame3,bg="light grey",selectbackground='white',highlightcolor="blue",bd=2)
percentage.pack()
percentage.insert(0,'05')
percentage.bind('<Return>',f_percentage)
percents = 5
frame4 = Frame(frame_total)
text3 = Label(frame4,text='Left clic : toogle cell,  Delete : kill cells,  Space : pause ')
text3.pack(side=LEFT)
frame4.grid(column=0,row=6)
replay = Button(frame4,text='Replay last sequence',command= replay_command,bg='light grey')
replay.pack(side=RIGHT)
mem_replay = [[2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2]]
chk3 = IntVar()
chk3.set(0)
stop_sequence = Checkbutton(frame_total,var=chk3,text='Stop automatic work when sequence finished (UP key to replay)',command=f_stop_sequence)
stop_sequence.grid(column=0,row=7)
geo_button = Button(fen,text='_____I\ \nI            \ \nI_____    / \n       I/',command=f_geo_button)
geo_button.grid(column=1,row=1)
geo_button_var = 'L'
speed = 800 # vitesse de changement d'étape (ms)
total,oldTotal1,oldTotal2,oldTotal3,oldTotal4,oldTotal5 = 0,-1,-2,-3,-4,-5
g = [[2,2,2,2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2,2,2,2]]
f = []
can = Canvas(fen,width=535,height=535,bg="black",highlightcolor="black")
can.grid(column=0,row=1,padx=5)
lines_ver = [0,0,0,0,0,0,0,0,0] # grille du Canvas
for i in range(0,9) : lines_ver[i] = can.create_line(i*45+90,45,i*45+90,535-45,fill='black')
lines_hor = [0,0,0,0,0,0,0,0,0] #
for i in range(0,9) : lines_hor[i] = can.create_line(45,i*45+90,535-45,i*45+90,fill='black')
# oval stocke les create_oval pour pouvoir faire item_config
oval = [[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0],[False,0,0,0,0,0,0,0,0,0,0]]
for y in range(1,11) :
    for x in range(1,11):
        oval[y][x] = can.create_oval(x*45,y*45,x*45+45,y*45+45,fill='blue',width=5)
        
can.bind('<Enter>',light_can)
can.bind('<Leave>',unlight_can)
can.bind('<Button-1>',mouse_color)
fen.bind('<Up>',debut_event)
fen.bind('<Right>',move_event)
fen.bind('<space>',f_AutoWork_event)
fen.bind('<Delete>', delete_can)
debut()
mainloop()
