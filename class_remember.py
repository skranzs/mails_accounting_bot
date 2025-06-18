class Remember_id:
    def __init__(self):
        self.name_cntragnt = ''
        self.contract_id = 0
        self.topic_of_letter = ''
        self.FIO = ''
        self.from_us = True
        self.type_letter = ''
        self.name_user = ''
        self.tg_id_user = ''

    def set_name_cntragnt(self, new_name):
        self.name_cntragnt = new_name
        print(f"Имя установлено: {self.name_cntragnt}")

    def get_name_cntragnt(self):
        return self.name_cntragnt
    
    def set_contract_id(self, new_id):
        self.contract_id = new_id
        print(f"ID установлен: {self.contract_id}")

    def get_contract_id(self):
        return self.contract_id

    def set_topic(self, new_topic):
        self.topic_of_letter = new_topic
        print(f"Тема установлеа: {self.topic_of_letter}")

    def get_topic(self):
        return self.topic_of_letter
    
    def set_FIO(self, new_FIO):
        self.FIO = new_FIO
        print(f"ФИО установлено: {self.FIO}")

    def get_FIO(self):
        return self.FIO
    
    def set_from_us(self, new_bool):
        self.from_us = new_bool
        print(f"Фlag установлен: {self.from_us}")

    def get_from_us(self):
        return self.from_us
    
    def set_type(self, new_type):
        self.type_letter= new_type
        print(f"Тип установлен: {self.type_letter}")

    def get_type(self):
        return self.type_letter
    
    def set_user(self, new_name, new_tg_id):
        self.name_user = new_name
        self.tg_id_user = new_tg_id

    def get_user(self):
        return self.name_user, self.tg_id_user

    def reset(self):
        self.name_cntragnt = ''
        self.contract_id = 0
        self.topic_of_letter = ''
        self.FIO = ''
        self.from_us = True
        self.type_letter
        print("Все данные сброшены.")

remember = Remember_id()