import json

from customtkinter import *
from CTkListbox import *
from category import Category
from task import Task
from CTkMessagebox import *
import keyboard
from CTkTable import CTkTable

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

        self.category_map = {}
        self.task_map = {}

        self.change_task_is_open = False
        self.running_task = None
        self.task_is_running = False
        self.selection_index = 0
        self.timer = None
        self.day_data = None

        keyboard.add_hotkey("ctrl+alt+a", self.switch_active_task_gui)

    def home_gui(self):
        self.window = CTk()
        self.window.title("Zeiterfassungstool")
        self.window.config(padx=20, pady=20)
        self.window.grid_columnconfigure(1, weight=3)
        self.window.grid_columnconfigure(0, weight=1)

        self.done_button = CTkButton(self.window, text="✔", font=M_FONT, height=40, width=40, corner_radius=8,
                                     command=lambda: self.mark_task_as_done(task_str=self.task_scrollbar.get(),
                                                                            index=self.task_scrollbar.curselection()))
        self.done_button.grid(row=0, column=4, padx=5, pady=5)

        self.add_button = CTkButton(self.window, text="+", font=XL_FONT, height=40, width=40, corner_radius=8,
                                    command=self.new_task_gui)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

        self.delete_button = CTkButton(self.window, text="➖", font=S_FONT, height=40, width=40, corner_radius=8,
                                       command=lambda: self.delete_task(task_str=self.task_scrollbar.get(),
                                                                        index=self.task_scrollbar.curselection()))
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.headline = CTkLabel(self.window, text="Aktuelle Aufgaben", font=HEADLINE_FONT)
        self.headline.grid(row=0, column=0, columnspan=1)

        self.task_scrollbar = CTkListbox(self.window, height=310, width=250, fg_color=BLUE_COL, border_width=0,
                                         corner_radius=20, font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY,
                                         highlight_color=HOVER_GREY, command=self.show_details)
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
                                      text="Tagesbericht", command=self.daily_report_gui)
        self.day_info_btn.grid(row=2, column=0, padx=5, sticky="w")

        self.new_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                                     text="Neue Kategorie", command=self.add_category_gui)
        self.new_cat_btn.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.archive_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                         font=M_FONT, text="Kategorien archivieren", command=self.archive_category_gui)
        self.archive_cat_btn.grid(row=2, column=2, pady=10, columnspan=3)

        self.buttons = [self.new_cat_btn, self.archive_cat_btn, self.delete_button, self.done_button,
                        self.day_info_btn, self.add_button]

        self.load_and_update()

        self.window.mainloop()

        self.save()

    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state=DISABLED)

    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state="normal")
        self.change_task_is_open = False

    def add_category_gui(self):
        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.configure(padx=10, pady=10)
        self.pop_up.title("Neue Kategorie anlegen")

        self.pop_up.grab_set()
        self.pop_up.focus()

        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

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
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=1, column=0, padx=5, pady=5)

        self.pop_up.after(1, name_entry.focus_set)

    def add_category(self, name):
        self.enable_buttons()
        new_category = Category(name=name, cat_id=self.category_id)
        self.category_map[f"ID {new_category.id}: {new_category.name}"] = new_category
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

        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        category_dropbox = CTkOptionMenu(self.pop_up, font=L_FONT, width=170, values=list(self.category_map.keys()),
                                         fg_color=GREY_COL, dropdown_fg_color=GREY_COL, dropdown_font=L_FONT,
                                         button_color=GREY_COL, button_hover_color=HOVER_GREY,
                                         dropdown_hover_color=HOVER_GREY)

        category_dropbox.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: self.archive_category(category_dropbox.get()))
        ok_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def archive_category(self, category_str: str):
        self.enable_buttons()
        self.pop_up.destroy()

        selected_category = self.category_map[category_str]

        if selected_category.active_task_count > 0:
            msg = CTkMessagebox(self.window, width=280, height=150, title="Confirm", font=M_FONT, option_1="OK",
                                option_2="Abbrechen", message="Diese Kategorie hat noch aktive Aufgaben. Wollen"
                                                              "sie diese als erledigt markieren und die "
                                                              "Kategorie archivieren?", icon="question")

            response = msg.get()
            if response == "Abbrechen":
                return None

        selected_category.active = False

        tasks_to_delete = []
        for task_str, item in self.task_map.items():
            if item.category == selected_category:
                item.active = False
                tasks_to_delete.append(task_str)

        for task_str in tasks_to_delete:
            del self.task_map[task_str]

        self.task_scrollbar.delete(0, END)
        for task_str in self.task_map.keys():
            self.task_scrollbar.insert(END, task_str)

        del self.category_map[category_str]

    def new_task_gui(self):
        if self.active_category_count == 0:
            CTkMessagebox(self.pop_up, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte legen Sie zuerst eine Kategorie an!")
            return None

        self.disable_buttons()
        self.pop_up = CTkToplevel()
        self.pop_up.title("Neue Aufgabe anlegen")

        self.pop_up.protocol("WM_DELETE_WINDOW", func=lambda: [self.pop_up.destroy(), self.enable_buttons()])

        self.pop_up.grab_set()
        self.pop_up.focus()

        name_frame = CTkFrame(self.pop_up, width=300, height=80, fg_color=BLUE_COL, border_width=0)
        name_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.pop_up.columnconfigure(0, weight=1)
        self.pop_up.columnconfigure(1, weight=1)

        name_label = CTkLabel(name_frame, text="Name:", font=XL_FONT)
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = CTkEntry(name_frame, font=L_FONT, border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        cat_frame = CTkFrame(self.pop_up, width=300, height=120, fg_color=BLUE_COL, border_width=0)
        cat_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        cat_label = CTkLabel(cat_frame, text="Kategorie:", font=XL_FONT)
        cat_label.grid(row=0, column=0, padx=5, pady=5)

        cat_frame.columnconfigure(1, weight=1)
        cat_dropbox = CTkOptionMenu(cat_frame, font=L_FONT, width=158, values=list(self.category_map.keys()),
                                    fg_color=GREY_COL, dropdown_fg_color=GREY_COL, dropdown_font=L_FONT,
                                    button_color=GREY_COL, button_hover_color=HOVER_GREY,
                                    dropdown_hover_color=HOVER_GREY)
        cat_dropbox.grid(row=0, column=1, padx=5, pady=5)

        ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: self.add_task(name=name_entry.get(),
                                                            task_descr=description_entry.get("0.0", END),
                                                            category_item=self.category_map[cat_dropbox.get()]))
        ok_button.grid(row=4, column=1, padx=25, pady=5, sticky="e")

        cancel_button = CTkButton(self.pop_up, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.enable_buttons()])
        cancel_button.grid(row=4, column=0, padx=25, pady=5, sticky="w")

        description_frame = CTkFrame(self.pop_up, width=260, height=180, fg_color=BLUE_COL, border_width=0)
        description_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        description_label = CTkLabel(description_frame, text="Beschreibung:", width=260, font=XL_FONT, anchor="w")
        description_label.grid(row=0, column=0, padx=5, columnspan=2)

        description_entry = CTkTextbox(description_frame, font=M_FONT, border_width=0, width=260, height=120,
                                       corner_radius=20, border_spacing=0)
        description_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        self.pop_up.after(1, name_entry.focus_set)

    def add_task(self, name: str, task_descr: str, category_item: Category):
        self.enable_buttons()
        self.pop_up.destroy()

        if len(name) == 0:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Ihre Aufgabe hat keinen Namen!")
            return None

        new_task = Task(name=name, description=task_descr, category=category_item, id_input=self.task_id)
        category_item.tasks.append(new_task)
        self.task_map[f"ID {new_task.id}: {new_task.name}"] = new_task
        self.task_scrollbar.insert(END, f"ID {new_task.id}: {new_task.name}")
        self.task_id += 1
        category_item.active_task_count += 1

    def mark_task_as_done(self, task_str, index):
        if task_str is None:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte wählen Sie zuerst eine Aufgabe aus!")
            return None

        selected_task = self.task_map[task_str]
        if selected_task == self.running_task:
            self.pause_running_task()

        selected_task.active = False
        del self.task_map[task_str]
        self.task_scrollbar.delete(index)

    def delete_task(self, task_str, index):

        if task_str is None:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=M_FONT,
                          message="Bitte wählen Sie zuerst eine Aufgabe aus!")
            return None

        selected_task = self.task_map[task_str]

        if selected_task == self.running_task:
            self.pause_running_task()

        selected_task.category.tasks.remove(selected_task)
        self.task_map.pop(task_str, None)
        self.task_scrollbar.delete(index)
        print(self.task_scrollbar.get)

        del selected_task

    def show_details(self, selected_task_str: str):
        selected_task = self.task_map[selected_task_str]

        self.task_category_info.delete("0.0", END)
        self.task_category_info.insert(END, f"Kategorie: {selected_task.category.name}")
        self.task_description.delete("0.0", END)
        self.task_description.insert(END, f"Beschreibung: {selected_task.description}")
        self.task_time_used_info.delete("0.0", END)
        used_time_str = (f"{int(selected_task.time_used // 3600)} h {int(selected_task.time_used % 3600) // 60} min "
                         f"{selected_task.time_used % 60} s")
        self.task_time_used_info.insert(END, f"genutzte Zeit: {used_time_str}")

    def switch_active_task_gui(self):

        if not bool(self.task_map):
            CTkMessagebox(self.window, width=280, height=150, title="Error", font=M_FONT,
                          message="Es existieren aktuell keine Aufgaben zum Auswählen!")
            return None

        elif not self.change_task_is_open:
            self.disable_buttons()
            self.change_task_is_open = True

            self.pop_up = CTkToplevel()
            self.pop_up.title("Aufgabe wechseln")
            self.pop_up.columnconfigure(0, weight=1)
            self.pop_up.columnconfigure(1, weight=1)

            self.pop_up.grab_set()
            self.pop_up.focus()

            task_switch_bar = CTkListbox(self.pop_up, height=260, width=200, fg_color=BLUE_COL, border_width=0,
                                         corner_radius=20,
                                         font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY,
                                         highlight_color=HOVER_GREY)
            task_switch_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            for task_str, item in self.task_map.items():
                task_switch_bar.insert(END, f"{task_str}")

            task_switch_bar.select(0)

            ok_button = CTkButton(self.pop_up, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                                  command=lambda: [self.pop_up.destroy(), self.set_active_task(task_switch_bar.get())])
            ok_button.grid(row=2, column=1, padx=5, pady=5)
            pause_button = CTkButton(self.pop_up, text="Pausieren", width=100, height=30, corner_radius=8, font=M_FONT,
                                     command=lambda: [self.pop_up.destroy(), self.pause_running_task()])
            pause_button.grid(row=2, column=0, padx=5, pady=5)

            keyboard.add_hotkey("down", lambda: task_switch_bar.select((task_switch_bar.curselection() + 1)
                                                                       % len(self.task_map)))
            keyboard.add_hotkey("up", lambda: task_switch_bar.select((task_switch_bar.curselection() - 1)
                                                                     % len(self.task_map)))

    def set_active_task(self, task_str: str):
        self.enable_buttons()
        self.change_task_is_open = False

        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

        self.running_task = self.task_map[task_str]
        self.count_time()

    def count_time(self):
        self.timer = self.window.after(1000, self.count_time)
        self.running_task.time_used += 1
        task_str = self.task_scrollbar.get()
        if task_str is not None:
            try:
                if self.running_task == self.task_map[task_str]:
                    self.show_details(task_str)
            except KeyError:
                pass

        print(self.running_task.time_used)

    def pause_running_task(self):
        self.enable_buttons()
        self.change_task_is_open = False

        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

    def daily_report_gui(self):
        self.disable_buttons()

        self.pop_up = CTkToplevel()
        self.pop_up.title("Tagesbericht")

        self.pop_up.grab_set()
        self.pop_up.focus()

        table_header = ["Kategorie", "Aufgabe", "genutzte Zeit"]
        data_table = CTkTable(self.pop_up, row=1, column=3, values=table_header)
        data_table.grid(row=0, column=0, padx=10, pady=10)

    def save(self):
        data = {"task_id": self.task_id,
                "category_id": self.category_id,
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

    def load_and_update(self):
        with open("data.json", "r") as file:
            data = json.load(file)
            self.task_id = data["task_id"]
            self.category_id = data["category_id"]
            for category_str, item in data["category_map"].items():
                name, cat_id = item["name"], item["id"]
                new_category = Category(name=name, cat_id=cat_id)
                new_category.active = data["category_map"][category_str]["active"]
                new_category.active_task_count = data["category_map"][category_str]["active_task_count"]
                print(new_category.name, new_category.id, new_category.active, new_category.active_task_count)
                self.category_map[category_str] = new_category
                for task_item in data["category_map"][category_str]["tasks"]:
                    task_name, task_id, description= task_item["name"], task_item["id"], task_item["description"]
                    new_task = Task(name=task_name, description=description, category=new_category, id_input=task_id)
                    new_task.time_used = task_item["time_used"]
                    new_task.active = task_item["active"]
                    new_category.tasks.append(new_task)
                    print(new_task.name, new_task.description, new_task.time_used, new_task.active)
                    self.task_map[f"ID {new_task.id}: {new_task.name}"] = new_task

        for task_str, item in self.task_map.items():
            self.task_scrollbar.insert(END, task_str)


app = TaskManager()
app.home_gui()
