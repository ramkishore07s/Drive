from app import DB

class Temp(DB.Model):
    __table_args__ = {'extend_existing': True}
    id = DB.Column('student_id', DB.Integer, primary_key = True)
    name = DB.Column(DB.String(100))
    city = DB.Column(DB.String(50))  
    addr = DB.Column(DB.String(200))
    pin = DB.Column(DB.String(10))

    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

        
