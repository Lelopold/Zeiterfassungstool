from tkinter import *

BG = "#0d2042"
FG = "white"
SMALL_FONT = ("Helvetica", 10, "bold")
FONT = ("Helvetica", 16, "bold")


class RoundedButton(Canvas):
    def __init__(self, master=None, text: str = "", radius=25, btn_foreground="#000000", btn_background="#ffffff",
                 clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btn_background = btn_background
        self.clicked = clicked

        self.radius = radius

        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btn_background)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btn_foreground, font=("Times", 30),
                                     justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)

        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2] - text_rect[0]:
            self["width"] = (text_rect[2] - text_rect[0]) + 10

        if int(self["height"]) < text_rect[3] - text_rect[1]:
            self["height"] = (text_rect[3] - text_rect[1]) + 10

    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False,
                        **kwargs):  # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)

        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2] - text_bbox[0]:
            width = text_bbox[2] - text_bbox[0] + 30

        if event.height < text_bbox[3] - text_bbox[1]:
            height = text_bbox[3] - text_bbox[1] + 30

        self.round_rectangle(5, 5, width - 5, height - 5, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2] - bbox[0]) / 2) - ((text_bbox[2] - text_bbox[0]) / 2)
        y = ((bbox[3] - bbox[1]) / 2) - ((text_bbox[3] - text_bbox[1]) / 2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="#d2d6d3")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.btn_background)


def func():
    print("Button pressed")


root = Tk()
btn = RoundedButton(text="This is a \n rounded button", radius=100, btn_background="#0078ff", btn_foreground="#ffffff",
                    clicked=func)
btn.pack(expand=True, fill="both")
root.mainloop()

def _on_release(self, event):
    self.configure(relief="raised")
    if self.command is not None:
        self.command()


window = Tk()
window.geometry("500x500")
window.title("Übersicht")
window.config(bg=BG)

canvas = Canvas(window, height=500, width=500, bg=BG)
canvas.pack()

button = RoundedButton(window, width=25, height=25, corner_radius=8, command=lambda: print("hello world"))
button.place(relx=.1, rely=.1)

headline = Label(window, text="Aktuelle Aufgaben", font=FONT, bg=BG, fg=FG)
headline.place(x=110, y=20, anchor="center")

done_button = Button(window, text="✔", font=SMALL_FONT, bg="white", fg="green",
                     activeforeground="dark green", width=1, height=1)
done_button.place(x=450, y=20, anchor="center")

add_button = Button(window, text="+", font=SMALL_FONT, bg="light grey", activebackground="dark grey", fg="green",
                    activeforeground="green", width=1, height=1)

window.mainloop()
