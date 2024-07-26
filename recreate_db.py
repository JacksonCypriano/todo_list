import psycopg2
from psycopg2 import sql

def recreate_database():
    # Conecte-se ao banco de dados padrão 'postgres' com o usuário 'admin'
    conn = psycopg2.connect(
        dbname="postgres",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(sql.SQL("DROP DATABASE IF EXISTS tasks"))

    cursor.execute(sql.SQL("CREATE DATABASE tasks WITH ENCODING 'UTF8' TEMPLATE template0"))

    cursor.close()
    conn.close()

if __name__ == "__main__":
    recreate_database()