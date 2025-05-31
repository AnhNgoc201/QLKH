from tkinter import messagebox
from doc_ghi_file import load_json_data
from open_window_sumit import open_quanly_window, open_nhanvien_window

def login(data, json_file, is_employee=False):
    try:
        user_data = load_json_data(json_file)
        email = data.get("Email", "").strip()
        password = data.get("Mật khẩu", "").strip()
        employee_code = data.get("Mã quản lý", "").strip() or data.get("Mã nhân viên", "").strip()

        # Kiểm tra đầu vào
        if not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập email!")
            return False
        if not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu!")
            return False
        if is_employee and not employee_code:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã nhân viên hoặc mã quản lý!")
            return False

        # Kiểm tra email tồn tại
        user = next((u for u in user_data if u.get('email') == email), None)
        if not user:
            messagebox.showerror("Lỗi", "Email không tồn tại!")
            return False

        # Kiểm tra mật khẩu
        if user.get('password') != password:
            messagebox.showerror("Lỗi", "Mật khẩu không đúng!")
            return False

        # Kiểm tra mã nhân viên/quản lý
        if is_employee:
            if user.get('employee_id') != employee_code:
                messagebox.showerror("Lỗi", "Mã nhân viên hoặc mã quản lý không đúng!")
                return False

            # Kiểm tra vai trò
            role = user.get('role')
            if role == 'admin':
                open_quanly_window()
                return True
            elif role == 'employee':
                open_nhanvien_window()
                return True
            else:
                messagebox.showerror("Lỗi", "Tài khoản không có quyền truy cập!")
                return False
        else:
            messagebox.showerror("Lỗi", "Tài khoản không hợp lệ!")
            return False

    except Exception as e:
        messagebox.showerror("Lỗi hệ thống", f"Có lỗi xảy ra: {str(e)}")
        return False