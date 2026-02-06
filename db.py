#banco de dados
import mysql.connector
import os
from dotenv import load_dotenv
import crud

load_dotenv()

def get_connect():
    return mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD")
    )