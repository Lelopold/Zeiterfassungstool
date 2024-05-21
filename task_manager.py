import json

from customtkinter import *
from CTkListbox import *
from category import Category
from task import Task
from CTkMessagebox import *
from mapped_listbox import MappedListbox

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
        self.active_category_count = 1
        self.task_id = 1
        self.category_id = 1

        self.categories = []
        self.tasks = []
        self.change_task_is_open = False
        self.running_task: Task
        self.task_is_running = False
        self.selection_index = 0
        self.timer = None
        self.day_data = None

    def home_gui(self):
        self.window = CTk()
        self.window.title("Zeiterfassungstool")
        self.window.config(padx=20, pady=20)
        self.window.grid_columnconfigure(1, weight=3)
        self.window.grid_columnconfigure(0, weight=1)

        self.done_button = CTkButton(self.window, text="✔", font=M_FONT, height=40, width=40, corner_radius=8,
                                     command=lambda: mark_task_as_done(selected_name=task_scrollbar.get(),
                                                                       index_selected=task_scrollbar.curselection()))
        self.done_button.grid(row=0, column=4, padx=5, pady=5)

        self.add_button = CTkButton(self.window, text="+", font=XL_FONT, height=40, width=40, corner_radius=8,
                                    command=add_task_gui)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

        self.delete_button = CTkButton(self.window, text="➖", font=S_FONT, height=40, width=40, corner_radius=8,
                                       command=lambda: [delete_task(selected_name=self.task_scrollbar.get(),
                                                                    index_selected=self.task_scrollbar.curselection())])
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.headline = CTkLabel(self.window, text="Aktuelle Aufgaben", font=HEADLINE_FONT)
        self.headline.grid(row=0, column=0, columnspan=1)

        self.task_scrollbar = CTkListbox(self.window, height=310, width=250, fg_color=BLUE_COL, border_width=0,
                                         corner_radius=20, font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY,
                                         highlight_color=HOVER_GREY, command=show_details)
        self.task_scrollbar.grid(row=1, column=0, columnspan=1, padx=5, pady=10)

        self.detail_frame = CTkScrollableFrame(self.window, height=310, width=300, corner_radius=20, border_width=0,
                                               fg_color=BLUE_COL)
        self.detail_frame.grid(row=1, column=1, columnspan=4, padx=5, pady=10)

        self.detail_headline = CTkLabel(self.detail_frame, text="Details", font=XXL_FONT)
        self.detail_headline.grid(row=0, column=0)
        self.detail_frame.grid_rowconfigure(0, weight=10)
        self.detail_frame.grid_columnconfigure(0, weight=10)

        self.task_description = CTkTextbox(self.detail_frame, width=300, height=160, corner_radius=15, border_width=0,
                                           font=M_FONT)
        self.task_description.grid(row=1, column=0, pady=5)
        self.task_description.insert(END, text="Beschreibung:")

        self.task_category_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                             font=M_FONT)
        self.task_category_info.grid(row=2, column=0, pady=5)
        self.task_category_info.insert(END, text="Kategorie:")

        self.task_time_used_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                              font=M_FONT)
        self.task_time_used_info.grid(row=3, column=0, pady=5)
        self.task_time_used_info.insert(END, text="genutzte Zeit:")

        self.day_info_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                                      text="Tagesbericht")
        self.day_info_btn.grid(row=2, column=0, padx=5, sticky="w")

        self.new_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                                     text="Neue Kategorie", command=self.add_category_gui)
        self.new_cat_btn.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.archive_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                         font=M_FONT, text="Kategorien archivieren", command=archive_category_gui)
        self.archive_cat_btn.grid(row=2, column=2, pady=10, columnspan=3)

        self.buttons = [self.new_cat_btn, self.archive_cat_btn, self.delete_button, self.done_button,
                        self.day_info_btn, self.add_button]

    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state=DISABLED)

    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state=NORMAL)

    def add_category_gui(self):
        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.configure(padx=10, pady=10)
        self.pop_up.title("Neue Kategorie anlegen")

        self.pop_up.grab_set()
        self.pop_up.focus()

        self.pop_up.protocol("WM_DELETE_WINDOW", self.enable_buttons)

        frame = CTkFrame(self.pop_up, width=300, height=80, fg_color=BLUE_COL, border_width=0)
        frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.pop_up.columnconfigure(0, weight=1)
        self.pop_up.columnconfigure(1, weight=1)

        name_label = CTkLabel(frame, text="Name:", font=XL_FONT)
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = CTkEntry(frame, font=L_FONT, border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: [self.add_category(name=name_entry.get()), self.pop_up.destroy()])
        ok_button.grid(row=1, column=1, padx=5, pady=5)

        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: self.pop_up.destroy())
        cancel_button.grid(row=1, column=0, padx=5, pady=5)

        self.pop_up.after(1, name_entry.focus_set)

    def add_category(self, name):
        self.categories.append(Category(name=name, id=self.category_id))
        self.pop_up.destroy()
        self.active_category_count += 1
        self.category_id += 1

    def archive_category_gui(self):
        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.configure(padx=10, pady=10)
        self.pop_up.title("Kategorie archivieren")

        self.pop_up.grab_set()
        self.pop_up.focus()

        self.pop_up.protocol("WM_DELETE_WINDOW", self.enable_buttons)

        category_names = [f"ID {cat.id}: {cat.name}" for cat in self.categories if cat.active]

        category_dropbox = CTkOptionMenu(self.pop_up, font=L_FONT, width=170, values=category_names, fg_color=GREY_COL,
                                         dropdown_fg_color=GREY_COL, dropdown_font=L_FONT, button_color=GREY_COL,
                                         button_hover_color=HOVER_GREY, dropdown_hover_color=HOVER_GREY)

        category_dropbox.grid(row=0, column=0, padx=5, pady=5)

    def archive_category(self, category_name: str):
        self.pop_up.destroy()

        for cat in self.categories:
            if cat.id == category_name and cat.active:
                if cat.active_task_count > 0:
                    CTkMessagebox(self.window, width=280, height=150, title="Error", font=M_FONT,
                                  message="Diese Kategorie hat noch aktive Aufgaben. Bitte haken Sie diese erst ab!")
                else:
                    cat.active = False
