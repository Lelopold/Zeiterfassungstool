# Python program to illustrate a stop watch
# using Tkinter
#importing the required libraries
import tkinter as Tkinter
from datetime import datetime
counter = 0
running = False
def counter_label(label):
	def count():
		if running:
			global counter

			# To manage the initial delay.
			if counter==0:
				display="Starting..."
			else:
				tt = datetime.fromtimestamp(counter)
				string = tt.strftime("%H:%M:%S")
				display=string

			label['text']=display # Or label.config(text=display)

			# label.after(arg1, arg2) delays by
			# first argument given in milliseconds
			# and then calls the function given as second argument.
			# Generally like here we need to call the
			# function in which it is present repeatedly.
			# Delays by 1000ms=1 seconds and call count again.
			label.after(1000, count)
			counter += 1

	# Triggering the start of the counter.
	count()

# start function of the stopwatch
def Start(label):
	global running
	running=True
	counter_label(label)
	start['state']='disabled'
	stop['state']='normal'
	reset['state']='normal'

# Stop function of the stopwatch
def Stop():
	global running
	start['state']='normal'
	stop['state']='disabled'
	reset['state']='normal'
	running = False

# Reset function of the stopwatch
def Reset(label):
	global counter
	counter=0

	# If rest is pressed after pressing stop.
	if running==False:
		reset['state']='disabled'
		label['text']='Welcome!'

	# If reset is pressed while the stopwatch is running.
	else:
		label['text']='Starting...'

root = Tkinter.Tk()
root.title("Stopwatch")

# Fixing the window size.
root.minsize(width=250, height=70)
label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.pack()
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label))
stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)
reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(label))
f.pack(anchor = 'center',pady=5)
start.pack(side="left")
stop.pack(side ="left")
reset.pack(side="left")
root.mainloop()

# import tkinter as tk
# from tkinter import ttk
# import keyboard
#
# def open_window():
#     window = tk.Tk()
#     window.title("Tabelle Auswahl")
#     window.lift()  # Fenster auf die oberste Ebene heben
#     window.focus_force()  # Fokus auf das Fenster setzen
#
#     # Tabelle
#     columns = ('#1',)
#     tree = ttk.Treeview(window, columns=columns, show='headings')
#     tree.heading('#1', text='Daten')
#     tree.insert('', 'end', values='Zeile 1')
#     tree.insert('', 'end', values='Zeile 2')
#     tree.insert('', 'end', values='Zeile 3')
#     tree.pack()
#
#     # Key bindings
#     def on_arrow_key(event):
#         if event.keysym == 'Up':
#             tree.selection_set(tree.prev(tree.selection()))
#         elif event.keysym == 'Down':
#             tree.selection_set(tree.next(tree.selection()))
#
#     def on_enter_key(event):
#         item = tree.item(tree.selection())
#         print("Ausgewählt:", item['values'])
#         window.destroy()
#
#     window.bind('<Up>', on_arrow_key)
#     window.bind('<Down>', on_arrow_key)
#     window.bind('<Return>', on_enter_key)
#
#     window.mainloop()
#
# # Globales Tastenkürzel registrieren
# keyboard.add_hotkey('ctrl+alt+a', open_window)
#
# # Das Hauptprogramm im Hintergrund halten
# keyboard.wait('esc')  # Drücken von ESC beendet das Programm

