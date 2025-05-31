import tkinter as tk
import re
from tkinter import ttk, messagebox
from doc_ghi_file import load_json_data, save_to_json, check_existing_email, check_existing_id_customer, check_existing_id_employee
import requests
from datetime import datetime
import random
from PIL import Image, ImageTk


# === Mở cửa sổ quản lý (chỉ hiển thị 2 nút) ===
# open_window_sumit.py (partial update for UI)
def open_quanly_window():
    window = tk.Toplevel()
    window.title("Quản lý")
    window.geometry("500x400")
    window.configure(bg="#f5f6fa")
    
    # Add header with image
    header = tk.Frame(window, bg="#3498db", height=80)
    header.pack(fill=tk.X)
    
    try:
        icon_img = Image.open("HUIT.jpg").resize((40, 20), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label = tk.Label(header, image=icon_photo, bg="#3498db")
        icon_label.image = icon_photo
        icon_label.pack(side=tk.LEFT, padx=10)
    except:
        pass
        
    tk.Label(header, text="Trang Quản Lý", bg="#3498db", fg="white", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10)
    
    button_frame = tk.Frame(window, bg="#f5f6fa")
    button_frame.pack(expand=True, pady=20)
    
    # Modern button style
    button_style = {
        "font": ("Arial", 12, "bold"),
        "width": 20,
        "height": 2,
        "bd": 0,
        "highlightthickness": 0,
        "relief": tk.FLAT
    }
    
    tk.Button(button_frame, text="Quản lý khách hàng", 
             bg="#2ecc71", fg="white", activebackground="#27ae60",
             command=open_customer_management, **button_style).pack(pady=15)
             
    tk.Button(button_frame, text="Quản lý nhân viên", 
             bg="#e74c3c", fg="white", activebackground="#c0392b",
             command=open_employee_management, **button_style).pack(pady=15)
# === Giao diện quản lý khách hàng ===
def open_customer_management():
    window = tk.Toplevel()
    window.title("Quản lý khách hàng")
    window.geometry("900x600")
    window.configure(bg="#ADD8E6")

    # Search frame
    search_frame = tk.Frame(window, bg="#ADD8E6")
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(search_frame, text="Tìm kiếm:", bg="#ADD8E6").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    def perform_search():
        keyword = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        customers = load_json_data("khachhang.json")
        for customer in customers:
            if (keyword in customer.get("makh", "").lower() or 
                keyword in customer.get("name", "").lower() or
                keyword in customer.get("email", "").lower()):
                tree.insert("", tk.END, values=(
                    customer.get("makh", ""),
                    customer.get("name", ""),
                    customer.get("address", ""),
                    customer.get("tel", ""),
                    customer.get("email", "")))
    
    search_button = tk.Button(search_frame, text="Tìm", command=perform_search, bg="#4CAF50", fg="white")
    search_button.pack(side=tk.LEFT, padx=5)
    reset_button = tk.Button(search_frame, text="Hiển thị tất cả", command=lambda: refresh_data(tree), bg="#4CAF50", fg="white")
    reset_button.pack(side=tk.LEFT)

    # Treeview khách hàng
    tree = ttk.Treeview(window, columns=("MaKH", "Name", "Address", "Tel", "Email"), show="headings")
    for col, title in zip(tree["columns"], ["Mã khách hàng", "Họ tên", "Địa chỉ", "Số điện thoại", "Email"]):
        tree.heading(col, text=title)
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    button_frame = tk.Frame(window, bg="#ADD8E6")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Thêm khách hàng", command=lambda: add_customer(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Sửa", command=lambda: edit_customer(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Xóa", command=lambda: delete_customer(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cập nhật", command=lambda: refresh_data(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Tạo hóa đơn", command=lambda: tao_hoa_don(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Xem hóa đơn", command=lambda: quanli_hoadon(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    refresh_data(tree)

# === Giao diện quản lý nhân viên ===
def open_employee_management():
    window = tk.Toplevel()
    window.title("Quản lý nhân viên")
    window.geometry("900x600")
    window.configure(bg="#E1F5FE")

    # Search frame
    search_frame = tk.Frame(window, bg="#E1F5FE")
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(search_frame, text="Tìm kiếm:", bg="#E1F5FE").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    def perform_search():
        keyword = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        employees = load_json_data("quanli.json")
        for emp in employees:
            if emp.get("role") == "employee" and (
                keyword in emp.get("employee_id", "").lower() or 
                keyword in emp.get("name", "").lower() or
                keyword in emp.get("email", "").lower()):
                tree.insert("", tk.END, values=(
                    emp.get("employee_id", ""),
                    emp.get("name", ""),
                    emp.get("address", ""),
                    emp.get("tel", ""),
                    emp.get("email", ""),
                    emp.get("role", "")))
    
    search_button = tk.Button(search_frame, text="Tìm", command=perform_search, bg="#4CAF50", fg="white")
    search_button.pack(side=tk.LEFT, padx=5)
    reset_button = tk.Button(search_frame, text="Hiển thị tất cả", command=lambda: refresh_employee_data(tree), bg="#4CAF50", fg="white")
    reset_button.pack(side=tk.LEFT)

    # Treeview nhân viên
    tree = ttk.Treeview(window, columns=("Mã NV", "Tên", "Địa chỉ", "SĐT", "Email", "Quyền"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

    button_frame = tk.Frame(window, bg="#E1F5FE")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Thêm nhân viên", command=lambda: add_employee(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Sửa", command=lambda: edit_employee(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Xóa", command=lambda: delete_employee(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cập nhật", command=lambda: refresh_employee_data(tree), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    refresh_employee_data(tree)
    

# === Làm mới dữ liệu nhân viên ===
def refresh_employee_data(tree):
    for item in tree.get_children():
        tree.delete(item)
    nhanviens = load_json_data("quanli.json")
    for nv in nhanviens:
        if nv.get("role") == "employee":
            tree.insert("", tk.END, values=(
                nv.get("employee_id", ""),
                nv.get("name", ""),
                nv.get("address", ""),
                nv.get("tel", ""),
                nv.get("email", ""),
                nv.get("role", "")
            ))

# === Thêm nhân viên mới ===
def add_employee(tree):
    add_window = tk.Toplevel()
    add_window.title("Thêm nhân viên mới")
    add_window.geometry("400x350")
    add_window.configure(bg="#ADD8E6")

    labels = ["Mã nhân viên", "Họ tên", "Địa chỉ", "Số điện thoại", "Email", "Mật khẩu"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(add_window, text=label, bg="#ADD8E6").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(add_window, width=30, show="*" if label == "Mật khẩu" else None)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    def save_employee():
        employee_id = entries["Mã nhân viên"].get()
        name = entries["Họ tên"].get()
        address = entries["Địa chỉ"].get()
        phone = entries["Số điện thoại"].get()
        email = entries["Email"].get()
        password = entries["Mật khẩu"].get()

        # Kiểm tra định dạng
        if not employee_id:
            messagebox.showerror("Lỗi", "Mã nhân viên không được để trống!")
            return
        if not re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]+$", name):
            messagebox.showerror("Lỗi", "Họ tên không hợp lệ!")
            return
        if not re.match(r"^\d{9,11}$", phone):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ!")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        if not password:
            messagebox.showerror("Lỗi", "Mật khẩu không được để trống!")
            return
        
        if check_existing_id_employee("quanli.json", employee_id):
            messagebox.showerror("Lỗi", "Mã nhân viên đã tồn tại!")
            return
        # Kiểm tra email trùng lặp
        if check_existing_email("quanli.json", email):
            messagebox.showerror("Lỗi", "Email đã tồn tại!")
            return

        new_employee = {
            "employee_id": employee_id,
            "name": name,
            "address": address,
            "tel": phone,
            "email": email,
            "password": password,
            "role": "employee"
        }

        employees = load_json_data("quanli.json")
        employees.append(new_employee)
        save_to_json("quanli.json", employees)
        messagebox.showinfo("Thành công", "Đã thêm nhân viên mới!")
        refresh_employee_data(tree)
        add_window.destroy()

    tk.Button(add_window, text="Lưu", command=save_employee, bg="#2196F3", fg="white").grid(row=len(labels), columnspan=2, pady=10)

# === Sửa thông tin nhân viên ===
def edit_employee(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần sửa!")
        return

    item = tree.item(selected_item[0])
    employee_data = item['values']

    edit_window = tk.Toplevel()
    edit_window.title("Sửa thông tin nhân viên")
    edit_window.geometry("400x350")
    edit_window.configure(bg="#ADD8E6")

    labels = ["Họ tên", "Địa chỉ", "Số điện thoại", "Email", "Mật khẩu"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(edit_window, text=label, bg="#ADD8E6").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(edit_window, width=30, show="*" if label == "Mật khẩu" else None)
        entry.insert(0, employee_data[i + 1] if label != "Mật khẩu" else "")  # Không hiển thị mật khẩu cũ
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    def update_employee():
        if not re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]+$", entries["Họ tên"].get()):
            messagebox.showerror("Lỗi", "Họ tên không hợp lệ!")
            return
        if not re.match(r"^\d{9,11}$", entries["Số điện thoại"].get()):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ!")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", entries["Email"].get()):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        
        employees = load_json_data("quanli.json")
        new_email = entries["Email"].get()

        # Kiểm tra email trùng lặp (trừ email hiện tại)
        for emp in employees:
            if emp['email'] != employee_data[4] and emp['email'] == new_email:
                messagebox.showerror("Lỗi", "Email đã tồn tại!")
                return

        for emp in employees:
            if emp['email'] == employee_data[4]:
                emp.update({
                    "name": entries["Họ tên"].get(),
                    "address": entries["Địa chỉ"].get(),
                    "tel": entries["Số điện thoại"].get(),
                    "email": new_email,
                    "password": entries["Mật khẩu"].get() if entries["Mật khẩu"].get() else emp['password']
                })
                break

        save_to_json("quanli.json", employees)
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
        refresh_employee_data(tree)
        edit_window.destroy()

    tk.Button(edit_window, text="Cập nhật", command=update_employee, bg="#2196F3", fg="white").grid(row=len(labels), columnspan=2, pady=10)

# === Xóa nhân viên ===
def delete_employee(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần xóa!")
        return

    item = tree.item(selected_item[0])
    employee_email = item['values'][4]

    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhân viên này?"):
        employees = load_json_data("quanli.json")
        employees = [e for e in employees if e['email'] != employee_email]
        save_to_json("quanli.json", employees)
        refresh_employee_data(tree)
        messagebox.showinfo("Thành công", "Đã xóa nhân viên!")

# === Các hàm xử lý khách hàng ===
def refresh_data(tree):
    for item in tree.get_children():
        tree.delete(item)
    customers = load_json_data("khachhang.json")
    for customer in customers:
        tree.insert("", tk.END, values=(
            customer.get("makh", ""),
            customer.get("name", ""),
            customer.get("address", ""),
            customer.get("tel", ""),
            customer.get("email", "")))

def add_customer(tree):
    add_window = tk.Toplevel()
    add_window.title("Thêm khách hàng mới")
    add_window.geometry("400x300")
    add_window.configure(bg="#ADD8E6")

    labels = ["Mã khách hàng", "Họ tên", "Địa chỉ", "Số điện thoại", "Email"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(add_window, text=label, bg="#ADD8E6").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(add_window, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    def save_customer():
        makh = entries["Mã khách hàng"].get()
        name = entries["Họ tên"].get()
        address = entries["Địa chỉ"].get()
        phone = entries["Số điện thoại"].get()
        email = entries["Email"].get()

        if not makh:
            messagebox.showerror("Lỗi", "Mã khách hàng không được để trống!")
            return
        if not re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]+$", name):
            messagebox.showerror("Lỗi", "Họ tên không hợp lệ!")
            return
        if not re.match(r"^\d{9,11}$", phone):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ!")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        
        #Kiểm tra mã khách hàng trùng lặp
        if check_existing_id_customer("khachhang.json", makh):
            messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại!")
            return

        # Kiểm tra email trùng lặp
        if check_existing_email("khachhang.json", email):
            messagebox.showerror("Lỗi", "Email đã tồn tại!")
            return

        new_customer = {
            "makh": makh,
            "name": name,
            "address": address,
            "tel": phone,
            "email": email
        }

        customers = load_json_data("khachhang.json")
        customers.append(new_customer)
        save_to_json("khachhang.json", customers)
        messagebox.showinfo("Thành công", "Đã thêm khách hàng mới!")
        refresh_data(tree)
        add_window.destroy()

    tk.Button(add_window, text="Lưu", command=save_customer, bg="#2196F3", fg="white").grid(row=len(labels), columnspan=2, pady=10)

def edit_customer(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần sửa!")
        return

    item = tree.item(selected_item[0])
    customer_data = item['values']

    edit_window = tk.Toplevel()
    edit_window.title("Sửa thông tin khách hàng")
    edit_window.geometry("400x300")
    edit_window.configure(bg="#ADD8E6")

    labels = ["Họ tên", "Địa chỉ", "Số điện thoại", "Email"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(edit_window, text=label, bg="#ADD8E6").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(edit_window, width=30)
        entry.insert(0, customer_data[i + 1])  # Bỏ qua cột Mã khách hàng
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry
        
    def update_customer():
        if not re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]+$", entries["Họ tên"].get()):
            messagebox.showerror("Lỗi", "Họ tên không hợp lệ!")
            return
        if not re.match(r"^\d{9,11}$", entries["Số điện thoại"].get()):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ!")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", entries["Email"].get()):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return
        
        customers = load_json_data("khachhang.json")
        new_email = entries["Email"].get()

        # Kiểm tra email trùng lặp (trừ email hiện tại)
        for customer in customers:
            if customer['email'] != customer_data[4] and customer['email'] == new_email:
                messagebox.showerror("Lỗi", "Email đã tồn tại!")
                return

        for customer in customers:
            if customer['email'] == customer_data[4]:
                customer.update({
                    "name": entries["Họ tên"].get(),
                    "address": entries["Địa chỉ"].get(),
                    "tel": entries["Số điện thoại"].get(),
                    "email": new_email
                })
                break

        save_to_json("khachhang.json", customers)
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
        refresh_data(tree)
        edit_window.destroy()
        
    tk.Button(edit_window, text="Cập nhật", command=update_customer, bg="#2196F3", fg="white").grid(row=len(labels), columnspan=2, pady=10)

def delete_customer(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa!")
        return

    item = tree.item(selected_item[0])
    customer_email = item['values'][4]

    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?"):
        customers = load_json_data("khachhang.json")
        customers = [c for c in customers if c['email'] != customer_email]
        save_to_json("khachhang.json", customers)
        refresh_data(tree)
        messagebox.showinfo("Thành công", "Đã xóa khách hàng!")

def open_nhanvien_window():
    window = tk.Toplevel()
    window.title("Nhân viên - Khách hàng")
    window.geometry("900x600")
    window.configure(bg="#ADD8E6")

    # Thêm khung tìm kiếm
    search_frame = tk.Frame(window, bg="#ADD8E6")
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(search_frame, text="Tìm khách hàng:", bg="#ADD8E6").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    def perform_search():
        keyword = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        customers = load_json_data("khachhang.json")
        for customer in customers:
            if (keyword in customer.get("makh", "").lower() or 
                keyword in customer.get("name", "").lower() or
                keyword in customer.get("email", "").lower() or
                keyword in customer.get("tel", "").lower()):
                tree.insert("", tk.END, values=(
                    customer.get("makh", ""),
                    customer.get("name", ""),
                    customer.get("address", ""),
                    customer.get("tel", ""),
                    customer.get("email", "")))
    
    search_button = tk.Button(search_frame, text="Tìm", command=perform_search, 
                            bg="#4CAF50", fg="white")
    search_button.pack(side=tk.LEFT, padx=5)
    
    reset_button = tk.Button(search_frame, text="Hiển thị tất cả", 
                           command=lambda: refresh_data(tree), 
                           bg="#4CAF50", fg="white")
    reset_button.pack(side=tk.LEFT)

    # Treeview khách hàng
    tree = ttk.Treeview(window, columns=("MaKH", "Name", "Address", "Tel", "Email"), show="headings")
    for col, title in zip(tree["columns"], ["Mã KH", "Họ tên", "Địa chỉ", "Số ĐT", "Email"]):
        tree.heading(col, text=title)
        tree.column(col, width=120 if col == "MaKH" else 150)
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    button_frame = tk.Frame(window, bg="#ADD8E6")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Thêm khách hàng", 
             command=lambda: add_customer(tree), 
             bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
             
    tk.Button(button_frame, text="Xem hóa đơn", 
             command=lambda: quanli_hoadon(tree), 
             bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
             
    tk.Button(button_frame, text="Tạo hóa đơn", 
             command=lambda: tao_hoa_don(tree), 
             bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    # Thêm nút làm mới dữ liệu
    tk.Button(button_frame, text="Làm mới", 
             command=lambda: refresh_data(tree), 
             bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    refresh_data(tree)
def quanli_hoadon(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xem hóa đơn!")
        return

    item = tree.item(selected_item[0])
    customer_email = item['values'][4]
    customer_name = item['values'][1]

    hoadons = load_json_data("hoadon.json")
    user_hoadons = [hd for hd in hoadons if hd["email"] == customer_email]

    invoice_window = tk.Toplevel()
    invoice_window.title(f"Hóa đơn của {customer_name}")
    invoice_window.geometry("600x500")
    invoice_window.configure(bg="#E1F5FE")

    tk.Label(invoice_window, text=f"Hóa đơn của khách hàng: {customer_name}", bg="#E1F5FE", font=("Arial", 14, "bold")).pack(pady=10)

    if not user_hoadons:
        tk.Label(invoice_window, text="Không có hóa đơn nào.", bg="#E1F5FE", fg="red").pack(pady=20)
        return

    for hd in user_hoadons:
        tk.Label(invoice_window, text=f"Ngày mua: {hd['ngaymua']}", bg="#E1F5FE", font=("Arial", 10, "bold")).pack(anchor='w', padx=10)
        for item in hd["items"]:
            text = f"- {item['name']} x{item['soluong']} - {item['price']}đ"
            tk.Label(invoice_window, text=text, bg="#E1F5FE").pack(anchor='w', padx=20)
        tk.Label(invoice_window, text=f"Tổng tiền: {hd['tongtien']}đ", bg="#E1F5FE", fg="red").pack(anchor='w', padx=10, pady=(0, 10))
        
        
def tao_hoa_don_ngau_nhien_tu_api(api_url_sp, selected_kh):
    if not selected_kh:
        messagebox.showerror("Lỗi", "Không có khách hàng được chọn.")
        return

    hoadons = load_json_data("hoadon.json")

    try:
        response = requests.get(api_url_sp)
        response.raise_for_status()
        danh_sach_san_pham = response.json()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể gọi API sản phẩm: {e}")
        return

    if not danh_sach_san_pham:
        messagebox.showerror("Lỗi", "API không trả về sản phẩm nào.")
        return

    so_san_pham_muon_chon = random.randint(1, len(danh_sach_san_pham))
    san_pham_duoc_chon = random.sample(danh_sach_san_pham, so_san_pham_muon_chon)


    for sp in san_pham_duoc_chon:
        sp["so_luong"] = random.randint(1, 3)

    tong_tien = sum(sp["so_luong"] * sp["price"] for sp in san_pham_duoc_chon)

    hoa_don = {
        "mahd": f"HD{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}",
        "ngaymua": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": selected_kh["email"],
        "items": [
            {
                "name": sp["name"],
                "description": sp.get("description", ""),
                "soluong": sp["so_luong"],
                "price": sp["price"]
            } for sp in san_pham_duoc_chon
        ],
        "tongtien": tong_tien
    }

    hoadons.append(hoa_don)
    save_to_json("hoadon.json", hoadons)
    messagebox.showinfo("Thành công", "Đã tạo thành công hóa đơn ngẫu nhiên từ API.")
    

def tao_hoa_don(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xem hóa đơn!")
        return
    
    item_id = selected_item[0]
    item_values = tree.item(item_id, "values")

    selected_kh = {
        "makh": item_values[0],
        "name": item_values[1],
        "address": item_values[2],
        "tel": item_values[3],
        "email": item_values[4]
    }
    
    tao_hoa_don_ngau_nhien_tu_api("https://thongthai.work/simple_api/200123410", selected_kh)








    