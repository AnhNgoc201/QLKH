# open_window.py
import tkinter as tk
from PIL import Image, ImageTk

def open_window(parent, title, json_file, fields, callback, back_callback=None, is_employee=False):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.title(title)
    
    # Add background image
    try:
        bg_img = Image.open("H01.jpg")
        bg_img = bg_img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(parent, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        pass

    form_frame = tk.LabelFrame(parent, text=title, padx=20, pady=20, 
                              bd=2, relief=tk.GROOVE, bg="white", font=("Arial", 14, "bold"))
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    mucluutru = {}
    for field in fields:
        row = tk.Frame(form_frame, bg="white")
        label = tk.Label(row, text=field, anchor='w', width=15, 
                         bg="white", font=("Arial", 12))
        entry = tk.Entry(row, show="*" if "Mật khẩu" in field else None,
                        font=("Arial", 12), bd=2, relief=tk.GROOVE)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=10)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, padx=10)
        mucluutru[field] = entry

    button_frame = tk.Frame(form_frame, bg="white")
    button_frame.pack(side=tk.BOTTOM, pady=10)

    def submit():
        data = {field: entry.get() for field, entry in mucluutru.items()}
        callback(data, json_file, is_employee=is_employee)

    submit_button = tk.Button(button_frame, text="Xác nhận", command=submit,
                             bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                             padx=15, pady=5, bd=0)
    submit_button.pack(side=tk.LEFT, padx=5)

    if back_callback:
        back_button = tk.Button(button_frame, text="Quay Lại", command=back_callback,
                               bg="#95a5a6", fg="white", font=("Arial", 12),
                               padx=15, pady=5, bd=0)
        back_button.pack(side=tk.RIGHT, padx=5)