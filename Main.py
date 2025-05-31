# Main.py
from dangnhap import login
from open_window import open_window
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Trang chủ")
root.configure(bg="#f0f8ff")
root.geometry("900x600")

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Load hình nền và giữ tham chiếu
    bg_img = Image.open("H01.jpg").resize((900, 600), Image.LANCZOS)
    root.bg_photo = ImageTk.PhotoImage(bg_img)  # giữ tham chiếu tại root
    bg_label = tk.Label(root, image=root.bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load logo và giữ tham chiếu
    try:
        logo_img = Image.open("HUIT.jpg").resize((200, 120), Image.LANCZOS)
        root.logo_photo = ImageTk.PhotoImage(logo_img)  # giữ tham chiếu
        logo_label = tk.Label(root, image=root.logo_photo, bg="#f0f8ff")
        logo_label.pack(pady=(20, 10))
    except Exception as e:
        print("Không tìm thấy logo:", e)

    label = tk.Label(root, text="Chào mừng bạn đến với hệ thống quản lý khách hàng",
                     bg="#f0f8ff", fg="#2c3e50", font=("Arial", 18, "bold"))
    label.pack(pady=(0, 30))

    container = tk.Frame(root, bg="#f0f8ff")
    container.pack(expand=True)

    frame = tk.Frame(container, bg="#f0f8ff", bd=2, relief=tk.GROOVE, padx=20, pady=20)
    frame.pack(expand=True)

    button_style = {
        "font": ("Arial", 12, "bold"),
        "width": 20,
        "height": 2,
        "bd": 0,
        "highlightthickness": 0,
        "relief": tk.FLAT
    }

    nhanvien_button = tk.Button(frame, text="Đăng Nhập Nhân Viên",
                                bg="#3498db", fg="white", activebackground="#2980b9",
                                command=open_nhanvien_options, **button_style)
    nhanvien_button.pack(pady=10, ipadx=10)

    quanli_button = tk.Button(frame, text="Đăng Nhập Quản Lý",
                              bg="#2ecc71", fg="white", activebackground="#27ae60",
                              command=open_quanli_login, **button_style)
    quanli_button.pack(pady=10, ipadx=10)

    footer = tk.Label(root, text="© 2025 Hệ thống Quản lý Khách hàng",
                      bg="#f0f8ff", fg="#7f8c8d", font=("Arial", 10))
    footer.pack(side=tk.BOTTOM, pady=10)

def open_nhanvien_options():
    open_window(root, "Đăng nhập nhân viên", "quanli.json",
                ["Email", "Mật khẩu", "Mã nhân viên"],
                login, show_main_menu, is_employee=True)

def open_quanli_login():
    open_window(root, "Đăng nhập quản lý", "quanli.json",
                ["Email", "Mật khẩu", "Mã quản lý"],
                login, show_main_menu, is_employee=True)

show_main_menu()
root.mainloop()
