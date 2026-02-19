#banco de dados
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connect():
    return mysql.connector.connect(
        host = os.environ.get("HOST"),
        user = os.environ.get("USER"),
        password = os.environ.get("PASSWORD")
    )