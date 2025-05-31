import json
import os
from tkinter import messagebox



def load_json_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        return []
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file {file_path}: {str(e)}")
        return []
    
    
def save_to_json(file_path, data):# Lưu dữ liệu vào file Json
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể ghi file {file_path}: {str(e)}")
        return False
    
    
def check_existing_email(file_path, email):#Kiểm tra xem email đã tồn tại trong tệp JSON chưa
    data = load_json_data(file_path)
    return any(user.get('email') == email for user in data)

def check_existing_id_customer(file_path, makh):
    data = load_json_data(file_path)
    return any(user.get('makh') == makh for user in data)

def check_existing_id_employee(file_path, employee_id):
    data = load_json_data(file_path)
    return any(user.get('employee_id') == employee_id for user in data)

