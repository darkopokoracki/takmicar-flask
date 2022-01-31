class Takmicar:
    __id: int
    __broj_prijave: str
    __ime_prezime: str
    __email: str
    __sifra: str
    __poeni_informatika: int
    __poeni_matematika: int

    def __init__(self, id: int, broj_prijave: str, ime_prezime: str, email: str, sifra: str, poeni_informatika: int, poeni_matematika: int) -> None:
        self.__id = id
        self.__broj_prijave = broj_prijave
        self.__ime_prezime = ime_prezime
        self.__email = email
        self.__sifra = sifra
        self.__poeni_informatika = poeni_informatika
        self.__poeni_matematika = poeni_matematika
    
    #Geteri
    def get_id(self):
        return self.__id

    def get_broj_prijave(self):
        return self.__broj_prijave

    def get_ime_prezime(self):
        return self.__ime_prezime

    def get_email(self):
        return self.__email

    def get_sifra(self):
        return self.__sifra

    def get_poeni_informatika(self):
        return self.__poeni_informatika

    def get_poeni_matematika(self):
        return self.__poeni_matematika


    #Seteri
    def set_id(self, novi_id):
        self.__id = novi_id

    def set_broj_prijave(self, novi_broj_prijave):        
        self.__broj_prijave = novi_broj_prijave

    def set_ime_prezime(self, novo_ime_prezime):
        self.__ime_prezime = novo_ime_prezime

    def set_email(self, novi_email):
        self.__email = novi_email

    def set_sifra(self, nova_sifra):
        self.__sifra = nova_sifra

    def set_poeni_informatika(self, novi_poeni_informatika):
        self.__poeni_informatika = novi_poeni_informatika

    def set_poeni_matematika(self, novi_poeni_matematika):
        self.__poeni_matematika = novi_poeni_matematika

    
    def __str__(self) -> str:
        res = f"Broj prijave: {self.__broj_prijave}\n"
        res += f"Ime i prezime: {self.__ime_prezime}\n"
        res += f"Email: {self.__email}\n"
        res += f"Sifra: {self.__sifra}\n"
        res += f"Poeni informatika: {self.__poeni_informatika}\n"
        res += f"Poeni matematika: {self.__poeni_matematika}\n"

        return res

    
        