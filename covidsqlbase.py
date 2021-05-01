import sqlite3
from sqlite3 import Error
import os

class CovidDataBase():
    def __init__(self):
        self.con = sqlite3.connect('base.sqlite')
        self.con.execute("PRAGMA foreign_keys = OFF")
        self.cursor = self.con.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.con.close()

    def close(self):
        self.con.close()
        
    ###############
    #### USERS ####
    ###############-
    def addUser(self,id):
        self.cursor.execute(f"INSERT INTO users(id) VALUES({id})")
        self.con.commit()
        #return true if len(self.getUser(id)) >0 else False

    def removeUser(self,id):
        try:
            self.cursor.execute(f"DELETE FROM users WHERE id ={id}")
            self.con.commit()
        except Error:
            print(Error)

    def getUsers(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def getUser(self,id):
        self.cursor.execute(f"SELECT * FROM users WHERE id={id}")
        return self.cursor.fetchall()

    


    ###############
    ### comunas ###
    ###############
    def addComuna(self,name):
        self.cursor.execute(f'INSERT INTO comunas(nombre) VALUES("{name}")')
        self.con.commit()
    
    def removeComuna(self,id):
        try:
            self.cursor.execute(f"DELETE FROM comunas WHERE id={id}" )
            self.con.commit()
        except Error:
            print(Error)
    
    def getComunas(self):
        self.cursor.execute(f"SELECT * FROM comunas")
        return self.cursor.fetchall()

    ################################
    ### suscripciones a datosEPI ###
    ################################
    def addSuscriptionoOption(self,id,name):
        self.cursor.execute(f'INSERT INTO datosEPI(id,nombre) VALUES({id},"{name}")')
        self.con.commit()

    def removeSuscriptionOption(self,id):
        self.cursor.execute(f"DELETE FROM datosEPI WHERE id={id}")
        self.con.commit()

    def getSuscriptionsOptions(self):
        self.cursor.execute(f"SELECT * FROM datosEPI")
        return self.cursor.fetchall()


    #### create suscriptions Comunas
    def suscribe2Comuna(self,user_id,nombre_comuna,fase):
        self.cursor.execute(f'INSERT INTO users_comunas_fases(user_id,nombre_comuna,fase) VALUES({user_id},"{nombre_comuna}",{fase})')
        self.con.commit()

    def unsuscribeComuna(self,user_id,nombre_comuna):
        self.cursor.execute(f'DELETE FROM users_comunas_fases WHERE user_id={user_id} AND nombre_comuna="{nombre_comuna}"')
        self.con.commit()

    def getUserComunas(self,user_id):
        self.cursor.execute(f'SELECT nombre_comuna FROM users_comunas_fases WHERE user_id={user_id}')
        return self.cursor.fetchall()

    #### create suscriptions datosEPI
    def suscribe2Dato(self,user_id,nombre_dato):
        self.cursor.execute(f'INSERT INTO user_datos(user_id,nombre_dato) VALUES({user_id},"{nombre_dato}")')
        self.con.commit()

    def unsuscribeDato(self,user_id,nombre_dato):
        self.cursor.execute(f'DELETE FROM user_datos WHERE user_id={user_id} AND nombre_dato="{nombre_dato}"')
        self.con.commit()
    
    def getUserDatos(self,user_id):
        self.cursor.execute(f'SELECT nombre_dato FROM user_datos WHERE user_id={user_id}')
        return self.cursor.fetchall()

if __name__ == "__main__":
    os.system('clear')
    db = Db()
