import time
from datetime import datetime
counter = 0
running = True


def count():
    if running:
        global counter
        # To manage the initial delay.
        tt = datetime.fromtimestamp(counter)
        print(tt)
        string = tt.strftime("%H:%M:%S")
        print(string)
        counter += 1
        print(counter)
    time.sleep(1)
    count()


count()

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

