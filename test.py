
imgframe = Frame(tab_image, width=400, height=200, borderwidth=1, relief=RIDGE)
imgframe.pack(fill="both", expand=True)

imgbuttonframe = Frame(tab_image, width=400, height=200, borderwidth=1, relief=RIDGE)
imgbuttonframe.pack(fill="both", expand=True)

imgtextframe = Frame(tab_image, width=400, height=660, borderwidth=1, relief=RIDGE)
imgtextframe.pack(fill="both", expand=True)

bottomframe = Frame(window, width=400, height=200, borderwidth=1, relief=RIDGE)
bottomframe.grid(row=2, column=0, sticky=N, pady=2)



progress_var = DoubleVar()
progress_var.set(0)

progressbar = ttk.Progressbar(
    master=acqframe, orient=HORIZONTAL, length=400, mode='determinate', variable=progress_var)
progressbar_label = Label(acqframe, text="Progress")
progressbar.grid(row=1, column=2, sticky=W, pady=2, padx=100)
progressbar_label.grid(row=0, column=2, sticky=W, pady=2, padx=100)

acq_button = Button(
    master=acqbuttonframe,
    text="Generate CSV",
    command=lambda: acquisition_thread(
        progressbar, progress_var, acqtextbox,
        brain_region_menu.get(), species_choice_menu.get(), cell_type_choice_menu.get())
)
acq_button.pack(fill="none", expand=True, side="left")

acq_entry_label = Label(acqbuttonframe, text="Name of file to generate:")
acq_entry_label.pack(fill="none", expand=True, side="left")

acq_entry_var = StringVar()
acq_entry_var.set('NM_All_All_All.csv')

acq_entry = Entry(acqbuttonframe, textvariable=acq_entry_var)
acq_entry.pack(fill="none", expand=True, side="left", ipadx=100)

acqtextbox = ScrolledText(acqtextframe, height=25, width=text_width)
acqtextbox.pack(side="left", fill="both", expand=True)

imgtextbox = ScrolledText(imgtextframe, height=25, width=text_width)
imgtextbox.pack(side="left", fill="both", expand=True)

about_textbox = Text(tab_about, height=25, width=text_width, background="silver")
about_textbox.pack(side="left", fill="both", expand=True)
about_textbox.insert(1.0, about_text)
about_textbox.configure(state="disabled")

os.makedirs('./output', exist_ok=True)

image_csv_choice_list = get_filenames(path='./output', suffix='.csv')
if not image_csv_choice_list:
    image_csv_choice_list = ["None"]
image_csv_choice = ttk.Combobox(imgframe, values=image_csv_choice_list, state='readonly',
                                postcommand=lambda: update_combobox_list(image_csv_choice))
image_csv_choice_label = Label(imgframe, text="CSV file:")
image_csv_choice_label.pack(fill="x", expand=False, side='top')
image_csv_choice.set(image_csv_choice_list[0])
image_csv_choice.pack(fill="x", expand=True)

imgprogress_var = DoubleVar()
imgprogress_var.set(0)

imgprogressbar = ttk.Progressbar(
    master=imgframe, orient=HORIZONTAL, length=400, mode='determinate', variable=imgprogress_var)
imgprogressbar_label = Label(imgframe, text="Progress")
imgprogressbar_label.pack(fill="x", expand=True)
imgprogressbar.pack(fill="both", expand=True)

image_button = Button(
    master=imgbuttonframe,
    text="Get Images",
    command=lambda: get_images_thread(
        imgprogressbar, imgprogress_var, imgtextbox,
        path='./output/', csv_file=image_csv_choice.get())
)
image_button.pack(fill="none", expand=True)

exit_button = Button(bottomframe, text="Quit", command=window.destroy)
exit_button.pack(fill="none", expand=True)

window.mainloop()
