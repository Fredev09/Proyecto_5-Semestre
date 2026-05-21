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

def init_contactos_mysql(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clientes_interesados (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            telefono VARCHAR(30) NOT NULL,
            correo VARCHAR(120) NOT NULL,
            servicio VARCHAR(100) NOT NULL,
            mensaje TEXT NOT NULL,
            fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado ENUM('Pendiente','Contactado','Prioridad Alta') DEFAULT 'Pendiente',
            fecha_contacto TIMESTAMP NULL
        )
    ''')
    mysql.connection.commit()
    cur.close()

def add_contacto_mysql(mysql, nombre, telefono, correo, servicio, mensaje):
    try:
        cur = mysql.connection.cursor()

        sql = """
            INSERT INTO clientes_interesados
            (nombre, telefono, correo, servicio, mensaje)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            nombre.strip(),
            telefono.strip(),
            correo.strip(),
            servicio.strip(),
            mensaje.strip()
        )

        print("===================================")
        print("GUARDANDO CLIENTE EN MYSQL")
        print("SQL:", sql)
        print("VALORES:", valores)
        print("===================================")

        cur.execute(sql, valores)

        mysql.connection.commit()

        print("CLIENTE GUARDADO CORRECTAMENTE")

        cur.close()

    except Exception as e:
        print("ERROR EN add_contacto_mysql():", e)
        raise


def get_contactos_mysql(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT id, nombre, telefono, correo, servicio, mensaje,
               fecha_envio, estado, fecha_contacto
        FROM clientes_interesados
        ORDER BY fecha_envio ASC
    ''')
    contactos = cur.fetchall()
    cur.close()
    return contactos


def actualizar_prioridades_mysql(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''
        UPDATE clientes_interesados
        SET estado = 'Prioridad Alta'
        WHERE estado = 'Pendiente'
        AND TIMESTAMPDIFF(HOUR, fecha_envio, NOW()) >= 24
    ''')
    mysql.connection.commit()
    cur.close()


def marcar_contactado_mysql(mysql, contacto_id):
    cur = mysql.connection.cursor()
    cur.execute('''
        UPDATE clientes_interesados
        SET estado = 'Contactado',
            fecha_contacto = NOW()
        WHERE id = %s
    ''', (contacto_id,))
    mysql.connection.commit()
    cur.close()

def get_proyectos_mysql(mysql):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, nombre, tipo_trabajo, descripcion, estado
        FROM proyectos_constructora
        ORDER BY id DESC
    """)

    proyectos = cur.fetchall()
    cur.close()

    return proyectos