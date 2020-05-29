import tkinter as tk
import csv
from tkinter import ttk
import requests
from PIL import ImageTk, Image

HEIGHT=500
WIDTH=500



class MasCine(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Mas Cine")
        self.minsize(width=WIDTH, height=HEIGHT)
        self.wm_iconbitmap("images/logo_1.ico")

        #Canvas
        canvas=tk.Canvas(self, width=WIDTH, height=HEIGHT)
        canvas.pack(expand = True, fill = "both")

        img = ImageTk.PhotoImage(Image.open("images/background_image.jpg"), Image.ANTIALIAS)
        canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

        frame=tk.Frame(self)
        frame.place(relx=0.15, rely=0.15,relwidth=0.15, relheight=0.05, anchor="n")

        lower_frame=tk.Frame(self, bg="#2F2C3B", bd=2)
        lower_frame.place(relx=0.3, rely=0.25, relwidth=0.5, relheight=0.6, anchor="n")
        label=tk.Label(lower_frame, text="Mejores Peliculas Netflix ",font=("Courier", 10), anchor="nw", justify="left", bd=4)
        label.place(relwidth=1, relheight=1)

        button = tk.Button(frame, text= "Ver peliculas", bg="black", foreground="white",font=("Helvetica",8,"bold"), command=lambda: get_weather(entry.get()))
        button.place(relx=0, relwidth=1, relheight=1)



class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand=False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor="nw")

if __name__=="__main__":
    #pass
    a=MasCine()
    a.mainloop()
