#biblioteki potrzebne do projektu
from cProfile import label
from tkinter import *
import sys

sys.path.insert(0, './zxcvbn')
from zxcvbn_pl.zxcvbn import zxcvbn

DIS='offline_fast_hashing_1e10_per_second'
DIE='offline_slow_hashing_1e4_per_second'
TRT='crack_times_display'

def clear():
	lbl_result.config(text="")
	warn.config(text="")
	fedback.config(text="")

def fun():
	haslo = ent1.get()
	if not haslo:
		lbl_result.config(text="hasło nie może być puste!!")
		return
	clear()
	res = zxcvbn(haslo)

	message = "Czas potrzebny na złamanie: "+res[TRT][DIS]
	czas1.config(text= message)

	message = "Oraz metodą wolną: "+res[TRT][DIE]
	czas2.config(text= message)

	lp_br=False
	
	if (res['feedback']['suggestions']):
		sugestie ="Sugestie : \n"
		for j in range(len(res['feedback']['suggestions'])):
			sugestie += res['feedback']['suggestions'][j]+"\n"
		fedback.config(text = sugestie)
	
	if (res['feedback']['warning']):
		sugestie ="Uwaga: \n"+res['feedback']['warning']
		warn.config(text = sugestie)
	
	if (res['sequence']):
		slowa = "\n"+"znalezione sekfencje: "
		for i in range(len(res['sequence'])):
			if i ==4:
				slowa+="\nitd.."
				break
			slowa+="\n"+res['sequence'][i]['pattern']+" -> "+res['sequence'][i]['token']
			if (res['sequence'][i]['pattern']=='bruteforce'):
				lp_br=True
		l_slowa.config(text = slowa)
	
	if res['score']<2:
		message1 = "hasło słabe, należy zmienić jak najszybciej"
		sumary.config(text = message1, fg="red")
	elif res['score']==4:
		message1 = "Hasło bardzo dobre. nada się do ataków bezpośrednich"
		sumary.config(text = message1, fg="green")
	else:
		message1 = "hasło umiarkowane, może zabespieczać mniej ważne dane(odporne na ataki online)"
		sumary.config(text = message1,fg="orange")
	if (lp_br):
		typ.config(text="Typ ataku brute-force")
	else:
		typ.config(text="Typ ataku słownikowy lub mięszany")

if __name__=='__main__':
	win = Tk()
	win.title('Pass calc')
	frame = Frame(master=win, width=550, height=500)
	frame.pack()

	Label(win, text='podaj swoje hasło: ').place(x=70,y=50)
	ent1 = Entry(win) 
	ent1.place(x=180,y=50)

	btn=Button(win,text="Oblicz", width=4,height=1,command=fun)
	btn.place(x=40,y=80) 

	l_slowa=Label(win, text = "", wraplength=350, justify="left")
	l_slowa.place(x=30,y=110)

	typ=Label(win,text = "", fg="blue")
	typ.place(x=220,y=120)

	czas1=Label(win, text="")
	czas1.place(x=220,y=140)

	czas2=Label(win, text="")
	czas2.place(x=220,y=160)

	fedback=Label(win, text = "", wraplength=350, justify="left")
	fedback.place(x=30, y=240)

	warn=Label(win, text="", wraplength=350, justify="left")
	warn.place(x=30, y=360)

	sumary=Label(win, text ="", wraplength=350, justify="left")
	sumary.place(x=50,y=450)

	lbl_result = Label(master=win, text="", fg="red")
	lbl_result.place(x=120,y=80)
	win.mainloop()