# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from acquisition import *
from config import *


def decorator(func):
    def inner(inputStr):
        try:
            text.insert(INSERT, inputStr)
            text.see(END)
            text.update_idletasks()
            progressbar.update_idletasks()
            return func(inputStr)
        except:
            return func(inputStr)
    return inner


sys.stdout.write=decorator(sys.stdout.write)


if __name__ == "__main__":
    window = Tk()
    window.title('NeuroMorpho Access Tool')
    #window.geometry('800x600')

    frame = Frame(window, width=400,height=660,borderwidth=1,relief=RIDGE)
    frame.grid(row = 0, column = 0, sticky = W, pady = 2)

    bottomframe = Frame(window, width=400,height=660,borderwidth=1,relief=RIDGE)
    bottomframe.grid(row = 1, column = 0, sticky = W, pady = 2)

    brain_region_menu = ttk.Combobox(master=frame, width=20, values=brain_regions)
    brain_region_menu.set(brain_regions[0])
    brain_region_menu_label = Label(frame, text="Brain Region:")
    brain_region_menu.grid(row = 0, column = 1, sticky = W, pady = 2)
    brain_region_menu_label.grid(row = 0, column = 0, sticky = W, pady = 2)

    species_choice_menu = ttk.Combobox(master=frame, width=20, values=species_all)
    species_choice_menu.set(species_all[0])
    species_choice_menu_label = Label(frame, text="Species:")
    species_choice_menu.grid(row = 1, column = 1, sticky = W, pady = 2)
    species_choice_menu_label.grid(row = 1, column = 0, sticky = W, pady = 2)

    cell_type_choice_menu = ttk.Combobox(master=frame, width=20, values=cell_types)
    cell_type_choice_menu.set(cell_types[0])
    cell_type_choice_menu_label = Label(frame, text="Cell Type:")
    cell_type_choice_menu.grid(row = 2, column = 1, sticky = W, pady = 2)
    cell_type_choice_menu_label.grid(row = 2, column = 0, sticky = W, pady = 2)

    progress_var = DoubleVar()
    progress_var.set(0)

    progressbar = ttk.Progressbar(
        master=frame, orient=HORIZONTAL, length=400, mode='determinate', variable=progress_var)
    progressbar_label = Label(frame, text="Progress")
    progressbar.grid(row=1, column=2, sticky=W, pady=2, padx=100)
    progressbar_label.grid(row=0, column=2, sticky=W, pady=2, padx=100)

    execute_button = Button(
        master=bottomframe,
        text="Execute",
        command=lambda: acquisition_thread(
            progress_var, brain_region_menu.get(), species_choice_menu.get(), cell_type_choice_menu.get())
    )
    execute_button.pack()

    text = Text(bottomframe, height=25, width=100)
    text.pack()

    exit_button = Button(bottomframe, text="Quit", command=window.destroy)
    exit_button.pack()

    window.mainloop()
