# search_window.py
import tkinter as tk
from tkinter import messagebox
from doc_ghi_file import load_json_data

def open_search_window(parent, json_file, search_fields=["name", "email"]):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.title("Tìm kiếm thông tin")
    
    label = tk.Label(parent, text="Nhập từ khóa cần tìm:", font=("Arial", 14))
    label.pack(pady=10)

    entry = tk.Entry(parent, font=("Arial", 12), width=40)
    entry.pack(pady=5)

    result_box = tk.Text(parent, height=20, width=80, font=("Arial", 11))
    result_box.pack(pady=10)

    def search():
        keyword = entry.get().lower()
        result_box.delete("1.0", tk.END)
        if not keyword:
            messagebox.showwarning("Thông báo", "Vui lòng nhập từ khóa để tìm!")
            return

        data = load_json_data(json_file)
        found = False
        for item in data:
            for field in search_fields:
                if keyword in str(item.get(field, "")).lower():
                    result_box.insert(tk.END, f"{item}\n\n")
                    found = True
                    break

        if not found:
            result_box.insert(tk.END, "Không tìm thấy kết quả nào.")

    tk.Button(parent, text="Tìm", command=search, font=("Arial", 12),
              bg="#2ecc71", fg="white", padx=10, pady=5).pack(pady=5)

    tk.Button(parent, text="Quay lại", command=parent.destroy, font=("Arial", 12),
              bg="#95a5a6", fg="white", padx=10, pady=5).pack(pady=5)
