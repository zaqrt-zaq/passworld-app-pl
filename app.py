#biblioteki potrzebne do projektu
from tkinter import *
from zxcvbn import zxcvbn
import math
from python_translator import Translator

DIS='offline_fast_hashing_1e10_per_second'
TRT='crack_times_seconds'

def sec2str(seconds):
	minute = 60
	hour = minute * 60
	day = hour * 24
	month = day * 31
	year = month * 12
	century = year * 100
	ans=["mniej niż sekunde","minej niż minutę", " minut" ,"godzinę" , " godzin", "dzień"," dni","miesiąc"," miesięcy"," rok"," lat","długo ("]
	if seconds < 1:
		return ans[0]
	elif seconds < minute:
		return ans[1]
	elif seconds < hour:
		return str(math.ceil(seconds/minute))+ans[2]
	elif seconds == hour:
		return ans[3]
	elif seconds < day:
		return str(math.ceil(seconds/hour))+ans[4]
	elif seconds == day:
		return ans[5]
	elif seconds < month:
		return str( math.ceil(seconds/day))+ans[6]
	elif seconds == month:
		return ans[7]
	elif seconds < year:
		return str( math.ceil(seconds/month))+ans[8]
	elif seconds == year:
		return ans[9]
	elif seconds < century:
		return str( math.ceil(seconds/year))+ans[10]
	else:
		return ans[11]+str( math.ceil(seconds/year))+" lat)"

def topl(text):
	translator = Translator()
	text=str(text)
	result = str(translator.translate(text, "polish", "english"))
	return 	"\n"+result[2:-3].replace(',',"\n").replace("'","")

def fun():
	haslo = ent1.get()
	if haslo:
		lbl_result.config(text="")
		res = zxcvbn(haslo)
		seconds = math.ceil(int(res[TRT][DIS]))

		message = "czas potrzebny na złamanie: "+str(sec2str(seconds))
		czas1.config(text= message)

		message = "oraz metodą wolną: "+str(sec2str(seconds*1000))
		czas2.config(text= message)

		if (res['feedback']['suggestions']):
			message = "sugestie : "+topl(str(res['feedback']['suggestions']))
			fedback.config(text = message)
		if seconds<60*60:
			message1 = "hasło słabe, należy zmienić jak najszybciej"
			sumary.config(text = message1, fg="red")
		elif seconds>60*60*24*31:
			message1 = "hasło bardzo dobre. nada się do ataków bezpośrednich"
			sumary.config(text = message1, fg="green")
		else:
			message1 = "hasło umiarkowane, może zabespieczać mniej ważne dane(odporne na ataki online)"
			sumary.config(text = message1,fg="orange")
	else:
		lbl_result.config(text="hasło nie może być puste!!")

win = Tk()
win.title('Pass calc')
frame = Frame(master=win, width=400, height=400)
frame.pack()

Label(win, text='podaj swoje hasło: ').place(x=70,y=70)
ent1 = Entry(win) 
ent1.place(x=180,y=70)

btn=Button(win,text="Oblicz", width=4,height=1,command=fun)
btn.place(x=40,y=100) 

sumary=Label(win, text ="", wraplength=350, justify="left")
sumary.place(x=50,y=350)

czas1=Label(win, text="")
czas1.place(x=30,y=140)

czas2=Label(win, text="")
czas2.place(x=30,y=160)

fedback=Label(win, text = "", wraplength=350, justify="left")
fedback.place(x=30,y=180)

lbl_result = Label(master=win, text="", fg="red")
lbl_result.place(x=120,y=120)
win.mainloop()
