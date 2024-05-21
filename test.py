import json
from customtkinter import *
from CTkListbox import *
from category import Category
from task import Task
from CTkMessagebox import *
from datetime import *
import keyboard


class TaskManager:
    def __init__(self):
        self.active_cats = []
        self.done_cats = []
        self.active_tasks = []
        self.task_id = 1
        self.running_task = None
        self.selection_index = 0
        self.timer = None
        self.current_date = str(date.today())
        self.day_data = None

        self.init_ui()
        self.load_and_update()

    def init_ui(self):
        self.window = CTk()
        self.window.title("Zeiterfassungstool")
        self.window.config(padx=20, pady=20)
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        self.init_widgets()
        self.init_hotkeys()

        self.window.mainloop()
        self.save()

    def init_widgets(self):
        self.headline = CTkLabel(self.window, text="Aktuelle Aufgaben", font=("Helvetica", 30, "bold"))
        self.headline.grid(row=0, column=0, columnspan=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.task_scrollbar = CTkListbox(self.window, height=310, width=250, fg_color="#1c538c", border_width=0,
                                         corner_radius=20, font=("Helvetica", 13, "bold"), button_color="#343434",
                                         hover_color="#4b4b4b", highlight_color="#4b4b4b", command=self.show_details)
        self.task_scrollbar.grid(row=1, column=0, columnspan=1, padx=5, pady=10)

        self.detail_frame = CTkScrollableFrame(self.window, height=310, width=300, corner_radius=20, border_width=0,
                                               fg_color="#1c538c")
        self.detail_frame.grid(row=1, column=1, columnspan=4, padx=5, pady=10)
        self.window.grid_columnconfigure(1, weight=3)

        self.detail_headline = CTkLabel(self.detail_frame, text="Details", font=("Helvetica", 22, "bold"))
        self.detail_headline.grid(row=0, column=0)
        self.detail_frame.grid_rowconfigure(0, weight=10)
        self.detail_frame.grid_columnconfigure(0, weight=10)

        self.description = CTkTextbox(self.detail_frame, width=300, height=160, corner_radius=15, border_width=0,
                                      font=("Helvetica", 13, "bold"))
        self.description.grid(row=1, column=0, pady=5)
        self.description.insert(END, text="Beschreibung:")

        self.category_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                        font=("Helvetica", 13, "bold"))
        self.category_info.grid(row=2, column=0, pady=5)
        self.category_info.insert(END, text="Kategorie:")

        self.used_time_info = CTkTextbox(self.detail_frame, width=300, height=20, corner_radius=15, border_width=0,
                                         font=("Helvetica", 13, "bold"))
        self.used_time_info.grid(row=3, column=0, pady=5)
        self.used_time_info.insert(END, text="genutzte Zeit:")

        self.day_info = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                  font=("Helvetica", 13, "bold"), text="Tagesbericht", command=self.show_daily_report)
        self.day_info.grid(row=2, column=0, padx=5, sticky="w")

        self.new_cat_btn = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                     font=("Helvetica", 13, "bold"), text="Neue Kategorie", command=self.add_category_gui)
        self.new_cat_btn.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.archive_cat = CTkButton(self.window, width=100, height=40, corner_radius=15, border_width=0,
                                     font=("Helvetica", 13, "bold"), text="Kategorien archivieren",
                                     command=self.archive_category_gui)
        self.archive_cat.grid(row=2, column=2, pady=10, columnspan=3)

        self.done_button = CTkButton(self.window, text="✔", font=("Helvetica", 13, "bold"), height=40, width=40,
                                     corner_radius=8, command=lambda: self.mark_task_as_done(selected_name=self.task_scrollbar.get(),
                                                                                              index_selected=self.task_scrollbar.curselection()))
        self.done_button.grid(row=0, column=4, padx=5, pady=5)

        self.add_button = CTkButton(self.window, text="+", font=("Helvetica", 18, "bold"), height=40, width=40,
                                    corner_radius=8, command=self.add_task_gui)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

        self.delete_button = CTkButton(self.window, text="➖", font=("Helvetica", 12, "bold"), height=40, width=40,
                                       corner_radius=8, command=lambda: self.delete_task(selected_name=self.task_scrollbar.get(),
                                                                                        index_selected=self.task_scrollbar.curselection()))
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.buttons = [self.new_cat_btn, self.day_info, self.archive_cat, self.done_button, self.add_button, self.delete_button]

    def init_hotkeys(self):
        keyboard.add_hotkey("ctrl+alt+a", self.switch_tasks_gui)

    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state="disabled")

    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state="normal")

    def add_task_gui(self):
        if len(self.active_cats) == 0:
            CTkMessagebox(self.window, width=250, height=150, title="Error", font=("Helvetica", 13, "bold"),
                          message="Bitte legen Sie zuerst eine Kategorie an!")
            return None

        self.disable_buttons()
        new_window = CTkToplevel()
        new_window.geometry("320x340")
        new_window.title("Neue Aufgabe anlegen")

        new_window.grab_set()
        new_window.focus()

        name_frame = CTkFrame(new_window, width=300, height=80, fg_color="#1c538c", border_width=0)
        name_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        new_window.columnconfigure(0, weight=1)
        new_window.columnconfigure(1, weight=1)

        name_label = CTkLabel(name_frame, text="Name:", font=("Helvetica", 18, "bold"))
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = CTkEntry(name_frame, font=("Helvetica", 16, "bold"), border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        cat_frame = CTkFrame(new_window, width=300, height=120, fg_color="#1c538c", border_width=0)
        cat_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        cat_label = CTkLabel(cat_frame, text="Kategorie:", font=("Helvetica", 18, "bold"))
        cat_label.grid(row=0, column=0, padx=5, pady=5)

        cat_names = [cat.name for cat in self.active_cats]

        cat_frame.columnconfigure(1, weight=1)
        cat_dropbox = CTkOptionMenu(cat_frame, font=("Helvetica", 16, "bold"), width=158, values=cat_names, fg_color="#343434",
                                    dropdown_fg_color="#343434", dropdown_font=("Helvetica", 16, "bold"), button_color="#343434",
                                    button_hover_color="#4b4b4b", dropdown_hover_color="#4b4b4b")
        cat_dropbox.grid(row=0, column=1, padx=5, pady=5)

        description_frame = CTkFrame(new_window, width=260, height=180, fg_color="#1c538c", border_width=0)
        description_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        description_label = CTkLabel(description_frame, text="Beschreibung:", width=260, font=("Helvetica", 18, "bold"), anchor="w")
        description_label.grid(row=0, column=0, padx=5, columnspan=2)

        description_entry = CTkTextbox(description_frame, font=("Helvetica", 13, "bold"), border_width=0, width=260, height=120,
                                       corner_radius=10)
        description_entry.grid(row=1, column=0, pady=5, padx=10, columnspan=2)

        def add_task():
            task_name = name_entry.get()
            task_description = description_entry.get("0.0", END)
            category_name = cat_dropbox.get()

            if task_name == "" or task_description == "":
                CTkMessagebox(new_window, width=250, height=150, title="Error", font=("Helvetica", 13, "bold"),
                              message="Bitte geben Sie einen Namen und eine Beschreibung ein!")
                return None
            if category_name == "":
                CTkMessagebox(new_window, width=250, height=150, title="Error", font=("Helvetica", 13, "bold"),
                              message="Bitte wählen Sie eine Kategorie aus!")
                return None

            category = self.find_category(category_name)
            task = Task(name=task_name, description=task_description, task_id=self.task_id, category=category,
                        start_time="", end_time="", is_running=False)
            category.tasks.append(task)
            self.active_tasks.append(task)
            self.task_scrollbar.insert(END, text=task.name)
            self.task_id += 1

            new_window.destroy()
            self.enable_buttons()

        add_btn = CTkButton(new_window, width=100, height=40, corner_radius=15, border_width=0, font=("Helvetica", 13, "bold"),
                            text="Hinzufügen", command=add_task)
        add_btn.grid(row=3, column=0, padx=5, pady=10)

        cancel_btn = CTkButton(new_window, width=100, height=40, corner_radius=15, border_width=0, font=("Helvetica", 13, "bold"),
                               text="Abbrechen", command=lambda: [self.enable_buttons(), new_window.destroy()])
        cancel_btn.grid(row=3, column=1, padx=5, pady=10)

    def find_category(self, name):
        for cat in self.active_cats:
            if cat.name == name:
                return cat

    def add_category_gui(self):
        self.disable_buttons()
        new_window = CTkToplevel()
        new_window.geometry("320x180")
        new_window.title("Neue Kategorie anlegen")
        new_window.grab_set()
        new_window.focus()

        name_frame = CTkFrame(new_window, width=300, height=80, fg_color="#1c538c", border_width=0)
        name_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        new_window.columnconfigure(0, weight=1)
        new_window.columnconfigure(1, weight=1)

        name_label = CTkLabel(name_frame, text="Name:", font=("Helvetica", 18, "bold"))
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = CTkEntry(name_frame, font=("Helvetica", 16, "bold"), border_width=0, width=190)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        def add_category():
            category_name = name_entry.get()
            if category_name == "":
                CTkMessagebox(new_window, width=250, height=150, title="Error", font=("Helvetica", 13, "bold"),
                              message="Bitte geben Sie einen Namen ein!")
                return None

            category = Category(name=category_name, tasks=[])
            self.active_cats.append(category)

            new_window.destroy()
            self.enable_buttons()

        add_btn = CTkButton(new_window, width=100, height=40, corner_radius=15, border_width=0, font=("Helvetica", 13, "bold"),
                            text="Hinzufügen", command=add_category)
        add_btn.grid(row=1, column=0, padx=5, pady=10)

        cancel_btn = CTkButton(new_window, width=100, height=40, corner_radius=15, border_width=0, font=("Helvetica", 13, "bold"),
                               text="Abbrechen", command=lambda: [self.enable_buttons(), new_window.destroy()])
        cancel_btn.grid(row=1, column=1, padx=5, pady=10)

    def show_details(self, *args):
        self.description.configure(state="normal")
        self.category_info.configure(state="normal")
        self.used_time_info.configure(state="normal")

        self.description.delete("0.0", END)
        self.category_info.delete("0.0", END)
        self.used_time_info.delete("0.0", END)

        selected_name = self.task_scrollbar.get()
        for task in self.active_tasks:
            if task.name == selected_name:
                task_selected = task

        self.description.insert(END, text=f"Beschreibung: {task_selected.description}")
        self.category_info.insert(END, text=f"Kategorie: {task_selected.category.name}")
        self.used_time_info.insert(END, text=f"genutzte Zeit: {task_selected.used_time}")

        self.description.configure(state="disabled")
        self.category_info.configure(state="disabled")
        self.used_time_info.configure(state="disabled")

    def mark_task_as_done(self, selected_name, index_selected):
        # The implementation goes here
        pass

    def delete_task(self, selected_name, index_selected):
        # The implementation goes here
        pass

    def archive_category_gui(self):
        # The implementation goes here
        pass

    def show_daily_report(self):
        # The implementation goes here
        pass

    def switch_tasks_gui(self):
        # The implementation goes here
        pass

    def save(self):
        with open("data.json", "w") as file:
            data = {
                "active_cats": [cat.to_dict() for cat in self.active_cats],
                "done_cats": [cat.to_dict() for cat in self.done_cats],
                "task_id": self.task_id,
                "current_date": self.current_date,
                "day_data": self.day_data
            }
            json.dump(data, file)

    def load_and_update(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.task_id = data.get("task_id", 1)
                self.current_date = data.get("current_date", str(date.today()))
                self.day_data = data.get("day_data", {})

                for cat_data in data.get("active_cats", []):
                    category = Category.from_dict(cat_data)
                    self.active_cats.append(category)
                    for task in category.tasks:
                        self.task_scrollbar.insert(END, text=task.name)
                        self.active_tasks.append(task)

                for cat_data in data.get("done_cats", []):
                    category = Category.from_dict(cat_data)
                    self.done_cats.append(category)
        except FileNotFoundError:
            self.save()


if __name__ == "__main__":
    TaskManager()
