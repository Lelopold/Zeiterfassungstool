import json

from customtkinter import *
from CTkListbox import *
from category import Category
from task import Task
from CTkMessagebox import *
import datetime as dt
import keyboard


def add_second():
    global time_active_task
    time_active_task += 1


def change_active_task():
    pass


def disable_buttons():
    for button in buttons:
        button.configure(state="disabled")


def enable_buttons():
    for button in buttons:
        button.configure(state="normal")


def add_task_gui():
    if len(active_cats) == 0:
        CTkMessagebox(window, width=250, height=150, title="Error", font=M_FONT,
                      message="Bitte legen Sie zuerst eine Kategorie an!")
        return None

    disable_buttons()
    new_window = CTkToplevel()
    new_window.geometry("320x340")
    new_window.title("Neue Aufgabe anlegen")

    new_window.grab_set()
    new_window.focus()

    name_frame = CTkFrame(new_window, width=300, height=80, fg_color=BLUE_COL, border_width=0)
    name_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    new_window.columnconfigure(0, weight=1)
    new_window.columnconfigure(1, weight=1)

    name_label = CTkLabel(name_frame, text="Name:", font=XL_FONT)
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = CTkEntry(name_frame, font=L_FONT, border_width=0, width=190)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    cat_frame = CTkFrame(new_window, width=300, height=120, fg_color=BLUE_COL, border_width=0)
    cat_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    cat_label = CTkLabel(cat_frame, text="Kategorie:", font=XL_FONT)
    cat_label.grid(row=0, column=0, padx=5, pady=5)

    cat_names = [cat.name for cat in active_cats]

    cat_frame.columnconfigure(1, weight=1)
    cat_dropbox = CTkOptionMenu(cat_frame, font=L_FONT, width=158, values=cat_names, fg_color=GREY_COL,
                                dropdown_fg_color=GREY_COL, dropdown_font=L_FONT, button_color=GREY_COL,
                                button_hover_color=HOVER_GREY, dropdown_hover_color=HOVER_GREY)
    cat_dropbox.grid(row=0, column=1, padx=5, pady=5)

    ok_button = CTkButton(new_window, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                          command=lambda: add_task(name=name_entry.get(), task_descr=description_entry.get("0.0", END),
                                                   cat_name=cat_dropbox.get(), root=new_window))
    ok_button.grid(row=4, column=1, padx=25, pady=5, sticky="e")

    cancel_button = CTkButton(new_window, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: destroy_pop_ups(new_window))
    cancel_button.grid(row=4, column=0, padx=25, pady=5, sticky="w")

    description_frame = CTkFrame(new_window, width=260, height=180, fg_color=BLUE_COL, border_width=0)
    description_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    description_label = CTkLabel(description_frame, text="Beschreibung:", width=260, font=XL_FONT, anchor="w")
    description_label.grid(row=0, column=0, padx=5, columnspan=2)

    description_entry = CTkTextbox(description_frame, font=M_FONT, border_width=0, width=260, height=120,
                                   corner_radius=20, border_spacing=0)
    description_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    new_window.after(1, name_entry.focus_set)


def add_task(name, cat_name, task_descr, root):
    global task_id
    enable_buttons()

    if len(name) == 0:
        destroy_pop_ups(root)
        CTkMessagebox(window, width=250, height=150, title="Error", font=M_FONT,
                      message="Ihre Aufgabe hat keinen Namen!")
        return None

    new_task = Task(name, task_descr, cat_name, task_id)
    for cat in active_cats:
        if cat.name == cat_name:
            cat.active_tasks.append(new_task)
            active_tasks.append(new_task)

    task_scrollbar.insert(END, f"ID {new_task.id}: {new_task.name}")
    destroy_pop_ups(root)
    task_id += 1


def mark_task_as_done(listbox_name, index_selected):
    id_selected_task = int(listbox_name.split()[1].replace(":", ""))

    for task in active_tasks:
        if task.id == id_selected_task:
            active_tasks.remove(task)
            for cat in active_cats:
                if cat.name == task.category:
                    cat.active_tasks.remove(task)
                    cat.done_tasks.append(task)

            task_scrollbar.delete(index_selected)


def add_category_gui():
    disable_buttons()
    new_window = CTkToplevel()
    new_window.geometry("320x100")
    new_window.title("Neue Kategorie anlegen")

    new_window.grab_set()
    new_window.focus()

    frame = CTkFrame(new_window, width=300, height=80, fg_color=BLUE_COL, border_width=0)
    frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    new_window.columnconfigure(0, weight=1)
    new_window.columnconfigure(1, weight=1)

    name_label = CTkLabel(frame, text="Name:", font=XL_FONT)
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = CTkEntry(frame, font=L_FONT, border_width=0, width=190)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ok_button = CTkButton(new_window, text="OK", width=100, height=30, corner_radius=8, font=M_FONT,
                          command=lambda: add_category(name=name_entry.get(), root=new_window))
    ok_button.grid(row=1, column=1, padx=5, pady=5)

    cancel_button = CTkButton(new_window, text="Abbrechen", width=100, height=30, corner_radius=8, font=M_FONT,
                              command=lambda: destroy_pop_ups(new_window))
    cancel_button.grid(row=1, column=0, padx=5, pady=5)

    new_window.after(1, name_entry.focus_set)


def destroy_pop_ups(pop_up):
    enable_buttons()

    pop_up.destroy()


def add_category(name, root):
    enable_buttons()

    new_cat = Category(name=name)
    active_cats.append(new_cat)

    destroy_pop_ups(root)


def archive_category_gui():
    pass
#     disable_buttons()
#     new_window = CTkToplevel()
#     new_window.geometry("320x340")
#     new_window.title("Neue Aufgabe anlegen")
#
#     new_window.grab_set()
#     new_window.focus()
#
#     cat_label = CTkLabel(cat_frame, text="Kategorie:", font=XL_FONT)
#     cat_label.grid(row=0, column=0, padx=5, pady=5)
#
#     cat_names = [cat.name for cat in active_cats]
#
#     cat_frame.columnconfigure(1, weight=1)
#     cat_dropbox = CTkOptionMenu(cat_frame, font=L_FONT, width=158, values=cat_names, fg_color=GREY_COL,
#                                 dropdown_fg_color=GREY_COL, dropdown_font=L_FONT, button_color=GREY_COL,
#                                 button_hover_color=HOVER_GREY, dropdown_hover_color=HOVER_GREY)
#     cat_dropbox.grid(row=0, column=1, padx=5, pady=5)


def show_details(selected_name: str):
    id_selected_task = int(selected_name.split()[1].replace(":", ""))

    for cat in active_cats:
        for task in cat.active_tasks:
            if task.id == id_selected_task:
                category_info.delete("0.0", END)
                category_info.insert(END, f"Kategorie: {task.category}")
                description.delete("0.0", END)
                description.insert(END, f"Beschreibung: {task.description}")


def extract_attributes(cat):
    category_dict = {"name": cat.name,
                     "time_used": cat.time_used,
                     "active_tasks": [],
                     "done_tasks": []}

    for task in cat.active_tasks:
        task_dict = {"name": task.name,
                     "description": task.description,
                     "time_used": task.time_used,
                     "category": task.category,
                     "id": task.id
                     }
        category_dict["active_tasks"].append(task_dict)

    for task in cat.done_tasks:
        task_dict = {"name": task.name,
                     "description": task.description,
                     "time_used": task.time_used,
                     "category": task.category,
                     "id": task.id
                     }
        category_dict["done_tasks"].append(task_dict)

    return category_dict


def import_attributes(category_dict):
    new_cat = Category(category_dict["name"])
    new_cat.time_used = category_dict["time_used"]

    for task in category_dict["active_tasks"]:
        new_task = Task(task["name"], task["description"], task["category"], task["id"])
        new_task.time_used = task["time_used"]

        new_cat.active_tasks.append(new_task)
        active_tasks.append(new_task)

    for task in category_dict["done_tasks"]:
        new_task = Task(task["name"], task["description"], task["category"], task["id"])
        new_task.time_used = task["time_used"]

        new_cat.done_tasks.append(new_task)

    return new_cat


def save():
    data = {"task_id": task_id,
            "active_cats": [],
            "done_cats": []
            }

    for cat in active_cats:
        data["active_cats"].append(extract_attributes(cat))

    for cat in done_cats:
        data["done_cats"].append(extract_attributes(cat))

    print(data)

    with open("data.json", "w") as file:
        json.dump(data, file)


def load_and_update():
    global task_id

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

            task_id = data["task_id"]

            for cat in data["active_cats"]:
                active_cats.append(import_attributes(cat))

            for cat in data["done_cats"]:
                done_cats.append(import_attributes(cat))

        for cat in active_cats:
            for task in cat.active_tasks:
                task_scrollbar.insert(END, f"ID {task.id}: {task.name}")
    except (FileNotFoundError, KeyError):
        pass


def delete_task(selected_name, index_selected):
    id_selected_task = int(selected_name.split()[1].replace(":", ""))

    for task in active_tasks:
        if task.id == id_selected_task:
            task_scrollbar.delete(index_selected)
            active_tasks.remove(task)
            for cat in active_cats:
                if task in cat.active_tasks:
                    cat.active_tasks.remove(task)
            del task


def switch_tasks_gui():
    disable_buttons()

    new_window = CTkToplevel()
    new_window.geometry("280x340")
    new_window.title("Aufgabe wechseln")

    new_window.grab_set()
    new_window.focus()

    task_switch_bar = CTkListbox(new_window, height=210, width=250, fg_color=BLUE_COL, border_width=0, corner_radius=20,
                                 font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY, highlight_color=HOVER_GREY)
    task_switch_bar.grid(row=0, column=0, columnspan=1, padx=5, pady=10)

    for task in active_tasks:
        task_switch_bar.insert(END, f"ID {task.id}: {task.name} ({task.category})")


def set_active_task(selected_name: str):
    global running_task
    id_selected_task = int(selected_name.split()[1].replace(":", ""))

    for task in active_tasks:
        if task.id == id_selected_task:
            running_task = task


XS_FONT = ("Helvetica", 10, "bold")
S_FONT = ("Helvetica", 12, "bold")
M_FONT = ("Helvetica", 13, "bold")
L_FONT = ("Helvetica", 16, "bold")
XL_FONT = ("Helvetica", 18, "bold")
XXL_FONT = ("Helvetica", 22, "bold")
HEADLINE_FONT = ("Helvetica", 30, "bold")


BLUE_COL = "#1c538c"
GREY_COL = "#343434"
HOVER_GREY = "#4b4b4b"


active_cats = []
done_cats = []
active_tasks = []
task_id = 1
running_task = None
time_active_task = 0


window = CTk()
window.title("Zeiterfassungstool")
window.config(padx=20, pady=20)
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

done_button = CTkButton(window, text="✔", font=M_FONT, height=40, width=40, corner_radius=8,
                        command=lambda: mark_task_as_done(listbox_name=task_scrollbar.get(),
                                                          index_selected=task_scrollbar.curselection()))
done_button.grid(row=0, column=4, padx=5, pady=5)

add_button = CTkButton(window, text="+", font=XL_FONT, height=40, width=40, corner_radius=8, command=add_task_gui)
add_button.grid(row=0, column=3, padx=5, pady=5)

delete_button = CTkButton(window, text="➖", font=S_FONT, height=40, width=40, corner_radius=8,
                          command=lambda: delete_task(selected_name=task_scrollbar.get(),
                                                      index_selected=task_scrollbar.curselection()))
delete_button.grid(row=0, column=2, padx=5, pady=5)

headline = CTkLabel(window, text="Aktuelle Aufgaben", font=HEADLINE_FONT)
headline.grid(row=0, column=0, columnspan=1)
window.grid_columnconfigure(0, weight=1)

task_scrollbar = CTkListbox(window, height=310, width=250, fg_color=BLUE_COL, border_width=0, corner_radius=20,
                            font=M_FONT, button_color=GREY_COL, hover_color=HOVER_GREY, highlight_color=HOVER_GREY,
                            command=show_details)
task_scrollbar.grid(row=1, column=0, columnspan=1, padx=5, pady=10)

detail_frame = CTkScrollableFrame(window, height=310, width=300, corner_radius=20, border_width=0, fg_color=BLUE_COL)
detail_frame.grid(row=1, column=1, columnspan=4, padx=5, pady=10)
window.grid_columnconfigure(1, weight=3)

detail_headline = CTkLabel(detail_frame, text="Details", font=XXL_FONT)
detail_headline.grid(row=0, column=0)
detail_frame.grid_rowconfigure(0, weight=10)
detail_frame.grid_columnconfigure(0, weight=10)

description = CTkTextbox(detail_frame, width=300, height=200, corner_radius=15, border_width=0, font=M_FONT)
description.grid(row=1, column=0, pady=5)
description.insert(END, text="Beschreibung:\nLorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

category_info = CTkTextbox(detail_frame, width=300, height=30, corner_radius=15, border_width=0, font=M_FONT)
category_info.grid(row=2, column=0, pady=5)
category_info.insert(END, text="Kategorie: Lorem ipsum dolor sit amet")

day_info = CTkButton(window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT, text="Tagesbericht")
day_info.grid(row=2, column=0, padx=5, sticky="w")

new_cat_btn = CTkButton(window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                        text="Neue Kategorie", command=add_category_gui)
new_cat_btn.grid(row=2, column=1, padx=5, pady=10, sticky="w")

archive_cat = CTkButton(window, width=100, height=40, corner_radius=15, border_width=0, font=M_FONT,
                        text="Kategorien archivieren", command=archive_category_gui)
archive_cat.grid(row=2, column=2, pady=10, columnspan=3)

load_and_update()

buttons = [new_cat_btn, day_info, archive_cat, done_button, add_button, delete_button]

if running_task is not None:
    window.after(1000, func=add_second)

keyboard.add_hotkey("ctrl+alt+a", switch_tasks_gui)

window.mainloop()

save()
