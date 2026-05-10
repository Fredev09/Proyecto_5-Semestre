from flask_mysqldb import MySQL
from flask import current_app

def get_mysql():
    return MySQL(current_app)

def init_mysql_db(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        rol VARCHAR(20) NOT NULL DEFAULT 'usuario',
        email_confirmado TINYINT DEFAULT 0
    )''')
    mysql.connection.commit()
    cur.close()

def add_usuario_mysql(mysql, username, password_hash, email, rol='usuario'):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuarios (username, password_hash, email, rol) VALUES (%s, %s, %s, %s)',
                (username, password_hash, email, rol))
    mysql.connection.commit()
    cur.close()

def update_email_mysql(mysql, username, nuevo_email):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE usuarios SET email = %s WHERE username = %s', (nuevo_email, username))
    mysql.connection.commit()
    cur.close()

def set_email_confirmado_mysql(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE usuarios SET email_confirmado = 1 WHERE email = %s', (email,))
    mysql.connection.commit()
    cur.close()

def get_usuario_by_username_mysql(mysql, username):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    return user

def get_usuario_by_email_mysql(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    return user

def add_proyecto_mysql(mysql, nombre, descripcion, estado):
    cur = mysql.connection.cursor()
    cur.execute(
        '''INSERT INTO proyectos_constructora 
        (nombre, descripcion, estado) 
        VALUES (%s, %s, %s)''',
        (nombre, descripcion, estado)
    )
    mysql.connection.commit()
    cur.close()

def get_proyectos_mysql(mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre, descripcion, estado FROM proyectos_constructora')
    proyectos = cur.fetchall()
    cur.close()
    return proyectos