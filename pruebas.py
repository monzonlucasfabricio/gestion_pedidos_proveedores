class user:
    def __init__(self,name,password):
        self.name = name
        self.password = password
    def get_data(self):
        print(self.name,self.password)