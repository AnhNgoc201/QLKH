class Khachhang:
    def __init__(self, makh, name, address, tel, email):
        self.makh = makh
        self.name = name
        self.address = address
        self.tel = tel
        self.email = email


    def to_dict(self):
        return {
            "mahd": self.mahd,
            "name": self.name,
            "address": self.address,
            "tel": self.tel,
            "email": self.email
        }
