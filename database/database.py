import mysql.connector

class Database:
    @staticmethod
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="!mYSr4lge",
            database="distribuidora"
        )