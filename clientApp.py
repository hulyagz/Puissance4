import tkinter as tk
from tkinter import *
import json
from tkinter import Canvas, NW, Label, Button
from client import Client
from tkinter import scrolledtext


class ClientApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=2)

        self.frames = {}
        for F in (StartPage, PageMain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Messagerie config:", fg="blue").grid(row=0, column=0)
        tk.Label(self, text="username:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="server:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="port:").grid(row=3, column=0, padx=10, pady=10)

        self.entryUsername = tk.Entry(self)
        self.entryUsername.grid(row=1, column=1)
        self.entryServer = tk.Entry(self)
        self.entryServer.grid(row=2, column=1)
        self.entryPort = tk.Entry(self)
        self.entryPort.grid(row=3, column=1)
        button = tk.Button(self, text="valider", width=20, fg="blue", command=lambda: self.validateConfig({
            'username': self.entryUsername.get(),
            'server': self.entryServer.get(),
            'port': int(self.entryPort.get())
        }))
        button.place(relx=0.5, rely=0.5, anchor=CENTER)
        button.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

    def validateConfig(self, data):
        self.controller.frames['PageMain'].receive_data(data)
        self.controller.show_frame("PageMain")


class PageMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.clair = "light blue"
        self.fonce = "navy blue"
        self.police1 = "Times 17 normal"
        self.police2 = "Arial 10 normal"
        self.police3 = "Times 15 bold"
        self.cases = []  # Cases d�j� remplies
        self.listerouge = []  # Liste des cases rouges
        self.listejaune = []  # Liste des cases jaunes
        self.dgagnantes = []  # Cases d�j� gagnantes et donc ne peuvent plus l"�tre � nouveau (cf "Continuer")
        self.running = 1  # Type de partie en cours
        self.couleur = ["Rouges", "Jaunes"]
        self.color = ["red", "#EDEF3A"]
        self.monCanvas = Canvas(self, width=446, height=430, bg=self.fonce, bd=0)
        self.monCanvas.grid(row=0, column=0)
        self.messages = scrolledtext.ScrolledText(self, width=50)
        self.messages.grid(row=0, column=1, padx=10, pady=10)

        self.entryMessage = tk.Entry(self, width=30)
        self.entryMessage.insert(0, "Votre message")
        self.entryMessage.grid(row=1, column=1, padx=10, pady=10)
        self.messages.tag_config('message', foreground='#3498db')

        def send_message():
            #clientMessage = self.entryMessage.get()
            #self.client.send(clientMessage)
            to_be_send = {
                'type': 'message',
                'data': {
                    'message': self.entryMessage.get(),
                },
            }
            
            self.client.send(to_be_send)

        btnSendMessage = tk.Button(self, text="Send", width=20, command=send_message)
        btnSendMessage.grid(row=2, column=1, padx=10, pady=20)

    def receive_data(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.client.listen(self.handle)

    def handle(self, data):
        self.messages.insert(tk.END, data + '\n', 'message')
        #data_parsed = json.loads(data)
        #self.messages.insert(tk.END, data + '\n', data_parsed)

        self.joueur = 1
        self.monCanvas.create_rectangle(20, 400, 115, 425, fill=self.clair)
        self.monCanvas.create_text(35, 405, text="Joueur :", anchor=NW, fill=self.fonce, font=self.police2)
        self.indiccoul = self.monCanvas.create_oval(85, 405, 100, 420, fill=self.color[1])

        # Bouton Nouveau Jeu

        self.monCanvas.create_rectangle(330, 400, 420, 425, fill=self.clair)
        self.monCanvas.create_text(340, 405, text="Nouveau jeu", anchor=NW, fill=self.fonce, font=self.police2)

        # Cr�ation des cases

        self.ovals = []
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.ovals.append(self.monCanvas.create_oval(x, y, x + 50, y + 50, fill="white"))

            # En cas de click

        self.monCanvas.bind("<Button-1>", self.click)

        # Pour relier � la fin les coordonn�es des centres des cases

        self.coordscentres = []

        # Comptabilisation des suites de pi�ces

        self.rouges, self.jaunes = 0, 0

        # Dictionnaire de reconnaissance

        self.dictionnaire = {}
        v = 0
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.dictionnaire[(x, y, x + 50, y + 50)] = v
                v += 1
                self.coordscentres.append((x + 25, y + 25))

    def click(self, event):  # En cas de click
        print(event)
        if 330 < event.x and 400 < event.y and event.x < 420 and event.y < 425:
            self.new()  # =>Nouveau jeu

            # Jeu en cours: reconnaissance de la case jou�e

        else:
            if self.running != 0:
                for (w, x, y, z) in self.dictionnaire:
                    if event.x > (w, x, y, z)[0] and event.y > (w, x, y, z)[1] and event.x < (w, x, y, z)[
                        2] and event.y < (w, x, y, z)[3]:
                        self.colorier(self.dictionnaire[(w, x, y, z)])  # => Jouer

    def colorier(self, n, nb=0):  # G�re la coloration des cases

        if n in self.cases: return  # Une case colori�e ne peut plus changer de couleur

        if n + 7 not in self.cases and n + 7 < 49:  # Si la case en dessous est vide et existe, on essaie d'abord de colorier celle-l�
            self.colorier(n + 7)

        else:

            # Sinon on colorie celle-ci

            self.monCanvas.itemconfigure(self.ovals[n], fill=self.color[self.joueur])
            self.cases.append(n)
            self.color[self.joueur] == 'red' and self.listerouge.append(n) or self.listejaune.append(n)
            self.listejaune = [case for case in self.listejaune if case not in self.listerouge]
            self.verif(n)

            # Changement de joueur

            self.joueur = [0, 1][[0, 1].index(self.joueur) - 1]
            self.monCanvas.itemconfigure(self.indiccoul, fill=self.color[self.joueur])

            # On regarde toutes les cases sont remplies

            self.verificationFinale()

        return

    def verif(self, n):  # V�rifie si la pi�ce ajout�e s'aligne avec trois autres d�j� plac�es

        if self.running == 0: return

        if n in self.listerouge and n + 7 in self.listerouge and n + 14 in self.listerouge and n + 21 in self.listerouge:  # D'abbord � la verticale,
            # s�par�ment car proximit� d'un bord inint�ressante
            liste = [n, n + 7, n + 14, n + 21]  # Pour g�r�r les parties "plurigagnantes"
            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
            return

            # idem pour jaunes

        if n in self.listejaune and n + 7 in self.listejaune and n + 14 in self.listejaune and n + 21 in self.listejaune:
            liste = [n, n + 7, n + 14, n + 21]
            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
            return

        for x in (1, -6, 8):

            if n in self.listerouge:  # en s'assurant qu'elles ne sont trop pr�s des bords (pour ne pas arriver de l'autre cot� du plateau)
                if n % 7 != 6 and n + x in self.listerouge:
                    if n % 7 != 5 and n + 2 * x in self.listerouge:
                        if n % 7 != 4 and n + 3 * x in self.listerouge:
                            liste = [n, n + x, n + 2 * x, n + 3 * x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return
                        if n % 7 > 0 and (n - x) in self.listerouge:
                            liste = [n - x, n, n + x, n + 2 * x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return
                    if n % 7 > 1 and (n - x) in self.listerouge:
                        if n % 7 > 2 and n - (2 * x) in self.listerouge:
                            liste = [n - 2 * x, n - x, n, n + x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return

                # Pareil pour les jaunes

            if n in self.listejaune:
                if n % 7 != 6 and n + x in self.listejaune:
                    if n % 7 != 5 and n + 2 * x in self.listejaune:
                        if n % 7 != 4 and n + 3 * x in self.listejaune:
                            liste = [n, n + x, n + 2 * x, n + 3 * x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return
                        if n % 7 > 0 and (n - x) in self.listejaune:
                            liste = [n - x, n, n + x, n + 2 * x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return
                    if n % 7 > 1 and (n - x) in self.listejaune:
                        if n % 7 > 2 and n - (2 * x) in self.listejaune:
                            liste = [n - 2 * x, n - x, n, n + x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return

        for x in (-1, 6, -8):

            if n in self.listejaune:
                if n % 7 != 0 and (n + x) in self.listejaune:
                    if n % 7 != 1 and n + (2 * x) in self.listejaune:
                        if n % 7 != 2 and n + (3 * x) in self.listejaune:
                            liste = [n, n + x, n + 2 * x, n + 3 * x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return
                        if n % 7 < 6 and (n - x) in self.listejaune:
                            liste = [n - x, n, n + x, n + 2 * x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return
                    if n % 7 < 5 and (n - x) in self.listejaune:
                        if n % 7 < 4 and n - (2 * x) in self.listejaune:
                            liste = [n - 2 * x, n - x, n, n + x]
                            if self.gagnantes(liste): self.win("jaunes", liste[0], liste[3])
                            return

            if n in self.listerouge:
                if n % 7 != 0 and (n + x) in self.listerouge:
                    if n % 7 != 1 and n + (2 * x) in self.listerouge:
                        if n % 7 != 2 and n + (3 * x) in self.listerouge:
                            liste = [n, n + x, n + 2 * x, n + 3 * x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return
                        if n % 7 < 6 and (n - x) in self.listerouge:
                            liste = [n - x, n, n + x, n + 2 * x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return
                    if n % 7 < 5 and (n - x) in self.listerouge:
                        if n % 7 < 4 and n - (2 * x) in self.listerouge:
                            liste = [n - 2 * x, n - x, n, n + x]
                            if self.gagnantes(liste): self.win("rouges", liste[0], liste[3])
                            return

    def verificationFinale(self):  # Lorsque toutes les cases sont remplies

        if len(self.cases) == 49:  # On comptabilise les points
            typ = self.plus()  # Type de partie gagn�e
            if typ[1] == 0:
                self.texte2 = Label(self, text="Les " + typ[0] + " ont d�finitivement gagn� !", bg=self.fonce,
                                    fg=self.clair, font=self.police1)
                self.texte2.grid()
            elif typ[1] == 1:
                self.texte2 = Label(self, text="Les " + typ[0] + " ont gagn� les premiers!", bg=self.fonce,
                                    fg=self.clair, font=self.police1)
                self.texte2.grid()
            else:
                self.texte2 = Label(self, text=typ[0], bg=self.fonce, fg=self.clair, font=self.police1)
                self.texte2.grid(padx=110)

    def win(self, qui, p, d):  # Partie gagn�e

        # Marquage des pi�ces gagnantes

        self.monCanvas.create_line(self.coordscentres[p][0], self.coordscentres[p][1],
                         self.coordscentres[d][0], self.coordscentres[d][1],
                         fill="blue")

        if qui == "rouges": self.rouges += 1  # Comptabilisation des suites
        if qui == "jaunes": self.jaunes += 1

        if self.running == 3:
            self.pRouges.config(text="Rouges : " + str(self.rouges))
            self.pJaunes.config(text="Jaunes : " + str(self.jaunes))
            return

            # Affichage des scores

        self.qui = qui
        self.texte = Label(self, text="Les %s ont gagne !" % (qui), bg=self.fonce, fg=self.clair, font=self.police1)
        self.texte.grid()
        self.running = 0

        # Proposition de continuer

        self.BtnContinuer = Button(self, text=" Continuer cette partie", bd=0, bg=self.fonce, fg=self.clair,
                                   font=self.police3, command=self.continuer)
        self.BtnContinuer.grid(padx=120)

    def continuer(self):  # Si on choisi de poursuivre la m�me partie (d�j� gagn�e par un joueur)

        self.running = 3

        # Affichage des scores

        self.pRouges = Label(self, text="Rouges : %s" % (str(self.rouges)),
                             font=self.police3, bg=self.fonce, fg=self.clair)
        self.pJaunes = Label(self, text="Jaunes : %s" % (str(self.jaunes)),
                             font=self.police3, bg=self.fonce, fg=self.clair)

        self.BtnContinuer.destroy()
        self.texte.destroy()
        self.pRouges.grid(padx=160)
        self.pJaunes.grid(padx=160)

    def gagnantes(self,
                  liste=[]):  # On v�rifie que les pi�ces ne sont pas encore gagnantes, et on les ajoute dans la liste si elles le deviennent

        for i in liste:
            if i in self.dgagnantes: return 0

        for n in liste:
            self.dgagnantes.append(n)

        return 1

    def plus(self):  # Donner le r�sultat final

        if self.rouges > self.jaunes: return "Rouges", 0
        if self.jaunes > self.rouges: return "Jaunes", 0
        if self.rouges != 0: return self.qui, 1  # En cas d'�galit�, le premier � avoir align� ses pi�ces gagne

        return "Personne n'a gagn�", 2  # Sinon, tous deux ont perdu

    def new(self):  # Nouveau Jeu

        # Op�rations non certaines

        try:
            self.BtnContinuer.destroy()
        except:
            pass
        try:
            self.texte.destroy()
        except:
            pass
        try:
            self.texte2.destroy()
        except:
            pass
        try:
            self.pRouges.destroy()
        except:
            pass
        try:
            self.pJaunes.destroy()
        except:
            pass

            # Op�rations qui le sont



if __name__ == '__main__':
    ClientApp().mainloop()
