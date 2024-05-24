import json

from customtkinter import *
from CTkListbox import *
from category import Category
from task import Task
from CTkMessagebox import *
import keyboard
from CTkTable import CTkTable
from datetime import datetime, timedelta

XS_FONT = ("Helvetica", 10, "bold")
S_FONT = ("Helvetica", 12, "bold")
M_FONT = ("Helvetica", 13, "bold")
L_FONT = ("Helvetica", 16, "bold")
XL_FONT = ("Helvetica", 18, "bold")
XXL_FONT = ("Helvetica", 22, "bold")
HEADLINE_FONT = ("Helvetica", 30, "bold")

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

BLUE_COL = "#1c538c"
GREY_COL = "#343434"
HOVER_GREY = "#4b4b4b"


class TaskManager:
    def __init__(self):
        # Initialisierung wichtiger GUI Elemente als Variablen, um dauerhaft darauf zugreifen zu können
        self.window = None
        self.done_button = None
        self.add_button = None
        self.delete_button = None
        self.headline = None
        self.task_scrollbar = None
        self.detail_frame = None
        self.detail_headline = None
        self.task_description = None
        self.task_category_info = None
        self.task_time_used_info = None
        self.day_info_btn = None
        self.new_cat_btn = None
        self.archive_cat_btn = None
        self.buttons = None
        self.pop_up = None
        self.task_switch_bar = None
        self.active_category_count = 0
        self.task_id = 1
        self.category_id = 1

        # Initialisierung von category_map und task_map zur Verwaltung der Aufgaben und Kategorien
        self.category_map = {}
        self.task_map = {}

        # Initialisierung sonstiger wichtiger Variablen zum Zwischenspeichern von Daten
        self.change_task_is_open = False
        self.running_task = None
        self.task_is_running = False
        self.timer = None
        self.day_data = {}
        self.current_date = str(datetime.today().date())

        # Initialisierung von Hotkey zum Öffnen und Navigieren durch das Fenster zum Wechseln der aktiven Aufgabe
        keyboard.add_hotkey("ctrl+alt+a", self.switch_active_task_gui)
        keyboard.add_hotkey("down", lambda: self.change_selection(False))
        keyboard.add_hotkey("up", lambda: self.change_selection(True))

    def home_gui(self):
        # Erstellen des Hauptfensters mit allen wichtigen Knöpfen und Informationen
        self.window = CTk()
        self.window.title("Zeiterfassungstool")
        self.window.config(padx=20, pady=20)
        self.window.grid_columnconfigure(1, weight=3)
        self.window.grid_columnconfigure(0, weight=1)

        # Button zum Abhaken von Aufgaben
        self.done_button = CTkButton(self.window, text="✔", font=M_FONT, height=40, width=40, corner_radius=8,
                                     command=lambda: self.mark_task_as_done(task_str=self.task_scrollbar.get(),
                                                                            index=self.task_scrollbar.curselection()))
        self.done_button.grid(row=0, column=4, padx=5, pady=5)

        # Button zum Hinzufügen von Aufgaben
        self.add_button = CTkButton(self.window, text="+", font=XL_FONT, height=40, width=40, corner_radius=8,
                                    command=self.new_task_gui)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

        # Button zum Entfernen von Aufgaben
        self.delete_button = CTkButton(self.window, text="➖", font=S_FONT, height=40, width=40, corner_radius=8,
                                       command=lambda: self.delete_task(task_str=self.task_scrollbar.get(),
                                                                        index=self.task_scrollbar.curselection()))
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        # Überschrift
        self.headline = CTkLabel(self.window, text="Aktuelle Aufgaben", font=HEADLINE_FONT)
        self.headline.grid(row=0, column=0, columnspan=1)

        # Liste mit allen aktiven Aufgaben
        self.task_scrollbar = CTkListbox(self.window, height=310, width=250, fg_color=BLUE_COL, border_width=0,
                                         corner_radius=20, font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY,
                                         highlight_color=HOVER_GREY, command=self.show_details)
        self.task_scrollbar.grid(row=1, column=0, columnspan=1, padx=5, pady=10)

        # Frame, welches die Elemente mit den wichtigen Informationen beinhaltet
        self.detail_frame = CTkScrollableFrame(self.window, height=310, width=300, corner_radius=20, border_width=0,
                                               fg_color=BLUE_COL)
        self.detail_frame.grid(row=1, column=1, columnspan=4, padx=5, pady=10)

        # überschrift für die Details zur ausgewählten Aufgabe in der Liste
        self.detail_headline = CTkLabel(self.detail_frame, text="Details", font=XXL_FONT)
        self.detail_headline.grid(row=0, column=0)
        self.detail_frame.grid_rowconfigure(0, weight=10)
        self.detail_frame.grid_columnconfigure(0, weight=10)

        # Beschreibung der ausgewählten Aufgabe
        self.task_description = CTkTextbox(self.detail_frame, width=300, height=160, corner_radius=15, border_width=0,
                                           font=M_FONT)
        self.task_description.grid(row=1, column=0, pady=5)
        self.task_description.insert(END, text="Beschreibung:")

        # Kategorie der ausgewählten Aufgabe
        self.task_category_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                             font=M_FONT)
        self.task_category_info.grid(row=2, column=0, pady=5)
        self.task_category_info.insert(END, text="Kategorie:")

        # bisherige Arbeitszeit der ausgewählten Aufgabe
        self.task_time_used_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                              font=M_FONT)
        self.task_time_used_info.grid(row=3, column=0, pady=5)
        self.task_time_used_info.insert(END, text="genutzte Zeit:")

        # Knopf zum Öffnen eines Fensters mit Tagesberichten
        self.day_info_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                                      text="Tagesbericht", command=lambda: self.daily_report_gui(self.current_date))
        self.day_info_btn.grid(row=2, column=0, padx=5, sticky="w")

        # Knopf zum Hinzufügen neuer Kategorien
        self.new_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                                     text="Neue Kategorie", command=self.add_category_gui)
        self.new_cat_btn.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        # Knopf zum archivieren von Kategorien
        self.archive_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                         font=M_FONT, text="Kategorien archivieren", command=self.archive_category_gui)
        self.archive_cat_btn.grid(row=2, column=2, pady=10, columnspan=3)

        # Liste aller Knöpfe im Hauptfenster
        self.buttons = [self.new_cat_btn, self.archive_cat_btn, self.delete_button, self.done_button,
                        self.day_info_btn, self.add_button]

        # Funktionen zum Laden der Aufgaben und Tagesberichte
        self.load_and_update()
        self.load_day_data()

        self.window.mainloop()

        # Funktionen zum Speichern der Aufgaben und Tagesberichte, nachdem das Fenster geschlossen wurde
        self.save_tasks()
        self.save_day_data()

    # Funktion zum Deaktivieren aller Knöpfe, wenn ein zusätzliches Fenster geöffnet ist
    # Verhindern, dass Fenster mehrfach und mehrere Fenster gleichzeitig neben dem Hauptfenster existieren
    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state=DISABLED)

    # Wieder Aktivieren der Knöpfe, wenn Nebenfenster geschlossen wird
    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state="normal")
        self.change_task_is_open = False

    # Funktion zum Hinzufügen neuer Kategorien
    def add_category_gui(self):
        # Nebenfenster
        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.configure(padx=10, pady=10)
        self.pop_up.title("Neue Kategorie anlegen")

        self.pop_up.grab_set()
        self.pop_up.focus()

        # Falls Fenster geschlossen wird (durch Drücken des X) Knöpfe wieder aktivieren
        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        # Frame für farbliche Abhebung vom Fenster
        frame = CTkFrame(self.pop_up, width=300, height=80, fg_color=BLUE_COL, border_width=0)
        frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.pop_up.columnconfigure(0, weight=1)
        self.pop_up.columnconfigure(1, weight=1)

        name_label = CTkLabel(frame, text="Name:", font=XL_FONT)
        name_label.grid(row=0, column=0, padx=5, pady=5)

        # Eingabefeld für Kategorienamen
        name_entry = CTkEntry(frame, font=L_FONT, border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Knopf zum Bestätigen der Eingabe und Zurückkehren zum Hauptmenü
        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: [self.add_category(name=name_entry.get()), self.pop_up.destroy()])
        ok_button.grid(row=1, column=1, padx=5, pady=5)

        # Knopf zum Abbrechen und Zurückkehren zum Hauptmenü
        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=1, column=0, padx=5, pady=5)

        # Cursor bereits in Eingabefeld setzen
        self.pop_up.after(1, name_entry.focus_set)

    # eingegebener Kategoriename im Eingabefeld verarbeiten
    def add_category(self, name):
        # Buttons aktivieren um nächste Aktion durchführen zu können
        self.enable_buttons()

        # Neue Kategorie mit eingegebenem Namen anlegen und dieser eine eindeutige ID zur Identifikation zuweisen
        new_category = Category(name=name, cat_id=self.category_id)

        # Zum Dictionary-Speicher aller aktiven Kategorien die Kategorie zuweisen.
        # Dafür wird dem String, mit dem die Aufgabe in den GUI-Elementen angezeigt wird, das Item zugeordnet.
        self.category_map[f"ID {new_category.id}: {new_category.name}"] = new_category
        self.pop_up.destroy()
        self.active_category_count += 1
        # category ID eins erhöhen, um nächster Kategorie diese zuweisen zu können
        self.category_id += 1

    # Pop-Up zum Archivieren von Kategorien
    def archive_category_gui(self):
        # Wenn keine aktive Kategorie existiert Anzeigen von Fehlermeldung
        if self.active_category_count == 0:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte legen Sie zuerst eine Kategorie an!")
            return None

        self.disable_buttons()

        # Nebenfenster
        self.pop_up = CTkToplevel()
        self.pop_up.configure(padx=10, pady=10)
        self.pop_up.title("Kategorie archivieren")

        self.pop_up.grab_set()
        self.pop_up.focus()

        # Knöpfe aktivieren, wenn Nebenfenster geschlossen
        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        # Dropdown-Auswahl zum Auswählen der Kategorie, die archiviert werden soll
        category_dropbox = CTkOptionMenu(self.pop_up, font=L_FONT, width=220, values=list(self.category_map.keys()),
                                         fg_color=GREY_COL, dropdown_fg_color=GREY_COL, dropdown_font=L_FONT,
                                         button_color=GREY_COL, button_hover_color=HOVER_GREY,
                                         dropdown_hover_color=HOVER_GREY)

        category_dropbox.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        # Knopf zum Bestätigen
        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: self.archive_category(category_dropbox.get()))
        ok_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        # Knopf zum Abbrechen
        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    # Auswahl aus Dropdown-Liste aus Kategorie-Speicher entfernen
    def archive_category(self, category_str: str):
        self.enable_buttons()
        self.pop_up.destroy()

        # In Dropdown Liste wurde der String ausgewählt. Mit diesem wird jetzt das zugehörige Class-Item identifiziert.
        selected_category = self.category_map[category_str]

        # Wenn Kategorie noch aktive Aufgaben hat, fragen, ob all diese als erledigt markiert werden sollen
        if selected_category.active_task_count > 0:
            msg = CTkMessagebox(self.window, width=280, height=150, title="Confirm", font=M_FONT, option_1="OK",
                                option_2="Abbrechen", message="Diese Kategorie hat noch aktive Aufgaben. Wollen"
                                                              "sie diese als erledigt markieren und die "
                                                              "Kategorie archivieren?", icon="question")

            response = msg.get()
            # Wenn nein, zurück ins Hauptmenü
            if response == "Abbrechen":
                return None

        # Wenn ja, Kategorie aus Kategorie-Speicher entfernen
        selected_category.active = False
        self.active_category_count -= 1

        # Alle aktiven Aufgaben der Kategorie finden und aus Task-Speicher entfernen
        tasks_to_delete = []
        for task_str, item in self.task_map.items():
            if item.category == selected_category:
                item.active = False
                tasks_to_delete.append(task_str)

        for task_str in tasks_to_delete:
            del self.task_map[task_str]

        # Liste der Aufgaben im Hauptmenü aktualisieren
        self.task_scrollbar.delete(0, END)
        for task_str, item in self.task_map.items():
            if item == self.running_task:
                self.task_scrollbar.insert(END, f"{task_str} ⚫")
            else:
                self.task_scrollbar.insert(END, task_str)

        del self.category_map[category_str]

    # Pop-Up zum Erstellen neuer Aufgaben
    def new_task_gui(self):
        # Fehlermeldung, falls keine aktiven Kategorien
        if self.active_category_count == 0:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte legen Sie zuerst eine Kategorie an!")
            return None

        # Nebenfenster
        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.title("Neue Aufgabe anlegen")

        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        self.pop_up.grab_set()
        self.pop_up.focus()

        # Frame zur farblichen Abhebung von Hintergrund
        name_frame = CTkFrame(self.pop_up, width=300, height=80, fg_color=BLUE_COL, border_width=0)
        name_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.pop_up.columnconfigure(0, weight=1)
        self.pop_up.columnconfigure(1, weight=1)

        name_label = CTkLabel(name_frame, text="Name:", font=XL_FONT)
        name_label.grid(row=0, column=0, padx=5, pady=5)

        # Eingabefeld Kategoriename
        name_entry = CTkEntry(name_frame, font=L_FONT, border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame zur farblichen Abhebung von Hintergrund
        cat_frame = CTkFrame(self.pop_up, width=300, height=120, fg_color=BLUE_COL, border_width=0)
        cat_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        cat_label = CTkLabel(cat_frame, text="Kategorie:", font=XL_FONT)
        cat_label.grid(row=0, column=0, padx=5, pady=5)

        cat_frame.columnconfigure(1, weight=1)

        # Dropdown Liste zur Auswahl der Kategorie
        cat_dropbox = CTkOptionMenu(cat_frame, font=L_FONT, width=158, values=list(self.category_map.keys()),
                                    fg_color=GREY_COL, dropdown_fg_color=GREY_COL, dropdown_font=L_FONT,
                                    button_color=GREY_COL, button_hover_color=HOVER_GREY,
                                    dropdown_hover_color=HOVER_GREY)
        cat_dropbox.grid(row=0, column=1, padx=5, pady=5)

        # Knopf zum Bestätigen
        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: self.add_task(name=name_entry.get(),
                                                            task_descr=description_entry.get("0.0", END),
                                                            category_item=self.category_map[cat_dropbox.get()]))
        ok_button.grid(row=4, column=1, padx=25, pady=5, sticky="e")

        # Knopf zum Abbrechen
        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=4, column=0, padx=25, pady=5, sticky="w")

        description_frame = CTkFrame(self.pop_up, width=260, height=180, fg_color=BLUE_COL, border_width=0)
        description_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        description_label = CTkLabel(description_frame, text="Beschreibung:", width=260, font=XL_FONT, anchor="w")
        description_label.grid(row=0, column=0, padx=5, columnspan=2)

        # Eingabefeld Aufgabenbeschreibung
        description_entry = CTkTextbox(description_frame, font=M_FONT, border_width=0, width=260, height=120,
                                       corner_radius=20, border_spacing=0)
        description_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        self.pop_up.after(1, name_entry.focus_set)

    # Erstellt mit Eingaben aus new_task_gui neues Task Item
    def add_task(self, name: str, task_descr: str, category_item: Category):
        # Fehlermeldung, wenn kein Name eingegeben
        if len(name) == 0:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Ihre Aufgabe hat keinen Namen!")
            return None

        self.enable_buttons()
        self.pop_up.destroy()

        # Neue Aufgabe anlegen
        new_task = Task(name=name, description=task_descr, category=category_item, id_input=self.task_id)
        # Zum Aufgabenspeicher der Kategorie hinzufügen
        category_item.tasks.append(new_task)
        # Zum generellen Aufgabenspeicher hinzufügen
        self.task_map[f"ID {new_task.id}: {new_task.name}"] = new_task
        self.task_scrollbar.insert(END, f"ID {new_task.id}: {new_task.name}")

        self.task_id += 1
        category_item.active_task_count += 1

    # Abhaken von der aktuell in Task-Liste ausgewählten Aufgabe
    def mark_task_as_done(self, task_str, index):
        # Wenn keine Aufgabe ausgewählt, Error
        if task_str is None:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte wählen Sie zuerst eine Aufgabe aus!")
            return None

        task_str = self.task_str_strip(task_str)
        selected_task = self.task_map[task_str]

        # Wenn abgehakte Aufgabe gerade laufende Aufgabe ist (also die Zeit für diese Aufgabe hochzählt), dies pausieren
        if selected_task == self.running_task:
            self.pause_running_task()

        # Attribut active der Aufgabe als falsch setzen
        selected_task.active = False

        # Aus generellem Aufgabenspeicher entfernen und aus Task-Liste löschen
        del self.task_map[task_str]
        self.task_scrollbar.delete(index)

    # Aktuell ausgewählte Aufgabe aus Task-Liste löschen
    def delete_task(self, task_str, index):
        # Error, wenn keine Aufgabe ausgewählt
        if task_str is None:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte wählen Sie zuerst eine Aufgabe aus!")
            return None

        task_str = self.task_str_strip(task_str)
        selected_task = self.task_map[task_str]

        # Wenn gelöschte Aufgabe gerade laufende Aufgabe ist (also die Zeit für diese Aufgabe hochzählt), dies pausieren
        if selected_task == self.running_task:
            self.pause_running_task()

        # Aus Aufgabenspeicher der Kategorie die Aufgabe entfernen
        selected_task.category.tasks.remove(selected_task)

        # Aus generellem Aufgabenspeicher entfernen
        self.task_map.pop(task_str, None)

        # Aus Task-Liste entfernen
        self.task_scrollbar.delete(index)

        del selected_task

    # Neben der Task-Liste Kategorie, Beschreibung und bereits genutzte Zeit der dort ausgewählten Aufgabe anzeigen
    def show_details(self, selected_task_str: str):
        selected_task_str = self.task_str_strip(selected_task_str)
        selected_task = self.task_map[selected_task_str]

        # Kategorie der Aufgabe
        self.task_category_info.delete("0.0", END)
        self.task_category_info.insert(END, f"Kategorie: {selected_task.category.name}")

        # Aufgabenbeschreibung
        self.task_description.delete("0.0", END)
        self.task_description.insert(END, f"Beschreibung: {selected_task.description}")

        # genutzte Zeit
        self.task_time_used_info.delete("0.0", END)
        used_time_str = (f"{int(selected_task.time_used // 3600)} h {int(selected_task.time_used % 3600) // 60} min "
                         f"{selected_task.time_used % 60} s")
        self.task_time_used_info.insert(END, f"genutzte Zeit: {used_time_str}")

    # GUI zum Wechseln der laufenden Aufgabe (aufgerufen durch Hotkey "ctrl+alt+a")
    def switch_active_task_gui(self):
        # Wenn keine aktiven Aufgaben existieren, Error anzeigen
        if not bool(self.task_map):
            CTkMessagebox(self.window, width=280, height=150, title="Error", font=M_FONT,
                          message="Es existieren aktuell keine Aufgaben zum Auswählen!")
            return None

        # Wenn Fenster nicht bereits offen
        elif not self.change_task_is_open:
            self.disable_buttons()
            # Variable zum Checken ob Fenster bereits offen ist, auf True setzen
            self.change_task_is_open = True

            # Nebenfenster
            self.pop_up = CTkToplevel()
            self.pop_up.title("Aufgabe wechseln")

            self.pop_up.grab_set()
            self.pop_up.focus()

            self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons(),
                                                                   self.enable_switch_active_task_gui])

            # Liste mit allen aktiven Aufgaben
            self.task_switch_bar = CTkListbox(self.pop_up, height=250, width=200, fg_color=BLUE_COL, border_width=0,
                                              corner_radius=20, font=M_FONT, button_color=GREY_COL,
                                              hover_color=HOVER_GREY, highlight_color=HOVER_GREY)
            self.task_switch_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

            for task_str, item in self.task_map.items():
                self.task_switch_bar.insert(END, f"{task_str}")

            self.task_switch_bar.select(0)

            # Knopf zum Bestätigen
            ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(),
                                                   self.set_active_task(self.task_switch_bar.get())])
            ok_button.grid(row=2, column=1, padx=5, pady=5)

            # Knopf zum Pausieren der aktiven Aufgabe
            pause_button = CTkButton(self.pop_up, text="Pausieren", width=100, height=30, corner_radius=8, font=M_FONT,
                                     command=lambda: [self.pop_up.destroy(), self.pause_running_task()])
            pause_button.grid(row=2, column=0, padx=5, pady=5)

    # Funktion zum Navigieren durch Liste zum Auswählen der laufenden Aufgabe mit Hotkeys (Pfeiltasten hoch und runter)
    def change_selection(self, up: bool):
        # Wenn Fenster zum Festlegen der laufenden Aufgabe offen ist
        if self.change_task_is_open:
            # Wenn Pfeiltaste nach oben gedrückt
            if up:
                self.task_switch_bar.select((self.task_switch_bar.curselection() - 1) % len(self.task_map))
            # Wenn Pfeiltaste nach unten gedrückt
            else:
                self.task_switch_bar.select((self.task_switch_bar.curselection() + 1) % len(self.task_map))

    # Fenster zum Wechseln der Aufgabe wieder zum Öffnen freischalten, wenn es geschlossen wurde
    def enable_switch_active_task_gui(self):
        self.change_task_is_open = False

    # Auswahl aus dem Pop-Up zum Wechseln der laufenden Aufgabe verarbeiten
    def set_active_task(self, task_str: str):
        self.enable_buttons()
        self.change_task_is_open = False

        # Timer zum Zählen der benutzten Zeit für laufende Aufgabe abbrechen
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

        # Laufende Aufgabe auf Auswahl einstellen
        print(self.task_map)
        print(task_str)
        task_str = self.task_str_strip(task_str)
        self.running_task = self.task_map[task_str]

        # Grüner Kreis hinter aktive Aufgabe
        self.task_scrollbar.delete(0, END)
        for key, value in self.task_map.items():
            if key == task_str:
                self.task_scrollbar.insert(END, f"{key} ⚫")
            else:
                self.task_scrollbar.insert(END, f"{key}")

        # Funktion zum Zählen der Zeit aufrufen
        self.count_time()

    # Funktion zum Zählen der genutzten Zeit für eine Aufgabe
    def count_time(self):
        # Rekursiver Aufruf, damit so lange gezählt wird, bis es stoppt
        self.timer = self.window.after(1000, self.count_time)
        self.running_task.time_used += 1

        task_str = self.task_str_strip(self.task_scrollbar.get())

        # Wenn Aufgabe heute noch nicht gelaufen ist, dem Speicher für den aktuellen Tag
        if f"ID {self.running_task.id}: {self.running_task.name}" not in self.day_data[self.current_date].keys():
            self.day_data[self.current_date][f"ID {self.running_task.id}: {self.running_task.name}"] = {
                "category": f"ID {self.running_task.category.id}: {self.running_task.category.name}",
                "time_used": 1
            }
        else:
            self.day_data[self.current_date][f"ID {self.running_task.id}: {self.running_task.name}"]["time_used"] += 1

        if task_str is not None:
            try:
                if self.running_task == self.task_map[task_str]:
                    self.show_details(task_str)
            except KeyError:
                pass

    @staticmethod
    def task_str_strip(task_str):
        if task_str is not None:
            if task_str[-2:] == " ⚫":
                return task_str.replace(" ⚫", "")
            else:
                return task_str

    def pause_running_task(self):
        self.enable_buttons()
        self.change_task_is_open = False

        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

    def daily_report_gui(self, selected_date: str):
        year = int(selected_date.split("-")[0])
        month = int(selected_date.split("-")[1])
        day = int(selected_date.split("-")[2])
        date = datetime(year, month, day).date()
        date_str = f"{day}.{month}.{year}"

        self.disable_buttons()

        self.pop_up = CTkToplevel()
        self.pop_up.title("Tagesbericht")

        self.pop_up.grab_set()
        self.pop_up.focus()

        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        date_headline = CTkLabel(self.pop_up, text=date_str, font=HEADLINE_FONT)
        date_headline.grid(row=0, column=0, columnspan=3)

        table_data = [["Kategorie", "Aufgabe", "genutzte Zeit"]]

        if selected_date in self.day_data.keys():
            for task_str, details in self.day_data[selected_date].items():
                time_str = (f"{details["time_used"] // 3600} h {(details["time_used"] % 3600) // 60} min "
                            f"{details["time_used"] % 60} s")

                new_row = [details["category"], task_str, time_str]
                table_data.append(new_row)

        if len(table_data) < 6:
            row_count = 6
        else:
            row_count = len(table_data)

        data_table = CTkTable(self.pop_up, column=3, row=row_count, values=table_data, width=200, font=L_FONT,
                              border_color=BLUE_COL, border_width=7, header_color=BLUE_COL)
        data_table.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        back_button = CTkButton(self.pop_up, text="Zurück", width=180, height=30, corner_radius=8, font=M_FONT,
                                command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        back_button.grid(row=2, column=1, padx=5, pady=5)

        next_button = CTkButton(self.pop_up, text="Nächster Tag", width=180, height=30, corner_radius=8, font=M_FONT,
                                command=lambda: [self.pop_up.destroy(),
                                                 self.daily_report_gui(str(date + timedelta(days=1)))])
        next_button.grid(row=2, column=2, padx=5, pady=5)

        prev_button = CTkButton(self.pop_up, text="Vorheriger Tag", width=180, height=30, corner_radius=8, font=M_FONT,
                                command=lambda: [self.pop_up.destroy(),
                                                 self.daily_report_gui(str(date - timedelta(days=1)))])
        prev_button.grid(row=2, column=0, padx=5, pady=5)

        # Set the size of the pop-up window
        pop_up_width = 640
        pop_up_height = 280 + (row_count - 6) * 30

        # Position the pop-up window over the main window
        main_window_x = self.window.winfo_x()
        main_window_y = self.window.winfo_y()

        # Center the pop-up window over the main window
        pop_up_x = main_window_x + (self.window.winfo_width() // 2) - (pop_up_width // 2)
        pop_up_y = main_window_y + (self.window.winfo_height() // 2) - (pop_up_height // 2)
        self.pop_up.geometry(f"{pop_up_width}x{pop_up_height}+{pop_up_x}+{pop_up_y}")

    def save_tasks(self):
        data = {"task_id": self.task_id,
                "category_id": self.category_id,
                "active_category_count": self.active_category_count,
                "category_map": {}
                }

        for category_str, item in self.category_map.items():
            data["category_map"][category_str] = {"name": item.name,
                                                  "id": item.id,
                                                  "active": item.active,
                                                  "active_task_count": item.active_task_count,
                                                  "tasks": []}
            for task_item in item.tasks:
                data["category_map"][category_str]["tasks"].append({"name": task_item.name,
                                                                    "description": task_item.description,
                                                                    "time_used": task_item.time_used,
                                                                    "category_id": f"{category_str}",
                                                                    "id": task_item.id,
                                                                    "active": task_item.active,
                                                                    })

        with open("data.json", "w") as file:
            json.dump(data, file)

    def save_day_data(self):
        with open("days.json", "w") as file:
            json.dump(self.day_data, file)

    def load_and_update(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.task_id = data["task_id"]
                self.category_id = data["category_id"]
                self.active_category_count = data["active_category_count"]
                for category_str, item in data["category_map"].items():
                    name, cat_id = item["name"], item["id"]
                    new_category = Category(name=name, cat_id=cat_id)
                    new_category.active = data["category_map"][category_str]["active"]
                    new_category.active_task_count = data["category_map"][category_str]["active_task_count"]
                    self.category_map[category_str] = new_category
                    for task_item in data["category_map"][category_str]["tasks"]:
                        task_name, task_id, description = task_item["name"], task_item["id"], task_item["description"]
                        new_task = Task(task_name, description, new_category, task_id)
                        new_task.time_used = task_item["time_used"]
                        new_task.active = task_item["active"]
                        new_category.tasks.append(new_task)
                        self.task_map[f"ID {new_task.id}: {new_task.name}"] = new_task
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
            pass

        for task_str, item in self.task_map.items():
            self.task_scrollbar.insert(END, task_str)

    def load_day_data(self):
        try:
            with open("days.json", "r") as file:
                self.day_data = json.load(file)
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
            pass

        if self.current_date not in self.day_data:
            self.day_data[self.current_date] = {}


app = TaskManager()
app.home_gui()
