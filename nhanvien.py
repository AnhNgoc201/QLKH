class Nhanvien:
    def __init__(self, name, address, tell, email, password, employee_id):
        self.name = name
        self.address = address
        self.tell = tell
        self.email = email
        self.password = password
        self.employee_id = employee_id

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "tell": self.tell,
            "email": self.email,
            "password": self.password,
            "employee_id": self.employee_id
        }

    