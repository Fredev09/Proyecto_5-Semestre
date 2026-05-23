from flask_mysqldb import MySQL
from flask import current_app


def get_mysql():
    return MySQL(current_app)


def tabla_existe(mysql, tabla):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = %s
    """, (tabla,))
    existe = cur.fetchone()["total"] > 0
    cur.close()
    return existe


def columna_existe(mysql, tabla, columna):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = %s
        AND COLUMN_NAME = %s
    """, (tabla, columna))
    existe = cur.fetchone()["total"] > 0
    cur.close()
    return existe


def asegurar_columna(mysql, tabla, columna, definicion):
    if not tabla_existe(mysql, tabla):
        return

    if not columna_existe(mysql, tabla, columna):
        cur = mysql.connection.cursor()
        cur.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")
        mysql.connection.commit()
        cur.close()


def asegurar_auto_increment(mysql, tabla):
    if not tabla_existe(mysql, tabla):
        return

    if not columna_existe(mysql, tabla, "id"):
        return

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = %s
        AND COLUMN_NAME = 'id'
    """, (tabla,))
    fila = cur.fetchone()

    if fila and "auto_increment" not in (fila["EXTRA"] or "").lower():
        cur.execute(f"ALTER TABLE {tabla} MODIFY id INT NOT NULL AUTO_INCREMENT")
        mysql.connection.commit()

    cur.close()


def init_mysql_db(mysql):
    cur = mysql.connection.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            rol VARCHAR(20) NOT NULL DEFAULT 'usuario',
            email_confirmado TINYINT DEFAULT 0,
            activo TINYINT DEFAULT 1
        )
    """)

    mysql.connection.commit()
    cur.close()

    # Migraciones seguras: no borran datos
    asegurar_columna(mysql, "usuarios", "activo", "TINYINT DEFAULT 1")
    asegurar_columna(mysql, "ventas", "porcentaje_anticipo", "INT DEFAULT 0")
    asegurar_columna(mysql, "ventas", "fecha", "DATE NULL")
    asegurar_columna(mysql, "ventas", "metodo_pago", "VARCHAR(100) NULL")
    asegurar_columna(mysql, "ventas", "anticipo", "DECIMAL(15,2) DEFAULT 0")
    asegurar_columna(mysql, "ventas", "saldo", "DECIMAL(15,2) DEFAULT 0")
    asegurar_columna(mysql, "ventas", "estado_pago", "VARCHAR(50) DEFAULT 'Pendiente'")
    asegurar_columna(mysql, "inmuebles", "tipo_negocio", "VARCHAR(20) DEFAULT 'Venta'")
    asegurar_columna(mysql, "proyectos_constructora", "tipo_trabajo", "VARCHAR(150) NULL")
    asegurar_columna(mysql, "reservas", "estado", "VARCHAR(20) DEFAULT 'Activa'")
    asegurar_columna(mysql, "clientes_interesados", "fecha_contacto", "TIMESTAMP NULL")

    # Corregir IDs sin AUTO_INCREMENT
    tablas_con_id = [
        "usuarios",
        "clientes_constructora",
        "clientes_inmobiliaria",
        "clientes_interesados",
        "cliente_proyecto",
        "compras",
        "inmuebles",
        "inmueble_multimedia",
        "proyectos_constructora",
        "reservas",
        "ventas",
    ]

    for tabla in tablas_con_id:
        asegurar_auto_increment(mysql, tabla)


def add_usuario_mysql(mysql, username, password_hash, email, rol="usuario"):
    cur = mysql.connection.cursor()

    if columna_existe(mysql, "usuarios", "activo"):
        cur.execute("""
            INSERT INTO usuarios (username, password_hash, email, rol, activo)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, password_hash, email, rol, 1))
    else:
        cur.execute("""
            INSERT INTO usuarios (username, password_hash, email, rol)
            VALUES (%s, %s, %s, %s)
        """, (username, password_hash, email, rol))

    mysql.connection.commit()
    cur.close()


def update_email_mysql(mysql, username, nuevo_email):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE usuarios SET email = %s WHERE username = %s",
        (nuevo_email, username)
    )
    mysql.connection.commit()
    cur.close()


def set_email_confirmado_mysql(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE usuarios SET email_confirmado = 1 WHERE email = %s",
        (email,)
    )
    mysql.connection.commit()
    cur.close()


def get_usuario_by_username_mysql(mysql, username):
    cur = mysql.connection.cursor()

    activo_select = "activo" if columna_existe(mysql, "usuarios", "activo") else "1 AS activo"

    cur.execute(f"""
        SELECT id, username, password_hash, email, rol, email_confirmado, {activo_select}
        FROM usuarios
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()
    cur.close()
    return user


def get_usuario_by_email_mysql(mysql, email):
    cur = mysql.connection.cursor()

    activo_select = "activo" if columna_existe(mysql, "usuarios", "activo") else "1 AS activo"

    cur.execute(f"""
        SELECT id, username, password_hash, email, rol, email_confirmado, {activo_select}
        FROM usuarios
        WHERE email = %s
    """, (email,))

    user = cur.fetchone()
    cur.close()
    return user


def add_proyecto_mysql(mysql, nombre, descripcion, estado):
    cur = mysql.connection.cursor()

    if columna_existe(mysql, "proyectos_constructora", "tipo_trabajo"):
        cur.execute("""
            INSERT INTO proyectos_constructora (nombre, tipo_trabajo, descripcion, estado)
            VALUES (%s, %s, %s, %s)
        """, (nombre, "Sin clasificar", descripcion, estado))
    else:
        cur.execute("""
            INSERT INTO proyectos_constructora (nombre, descripcion, estado)
            VALUES (%s, %s, %s)
        """, (nombre, descripcion, estado))

    mysql.connection.commit()
    cur.close()


def get_proyectos_mysql(mysql):
    cur = mysql.connection.cursor()

    tipo_select = (
        "tipo_trabajo"
        if columna_existe(mysql, "proyectos_constructora", "tipo_trabajo")
        else "'Sin clasificar' AS tipo_trabajo"
    )

    cur.execute(f"""
        SELECT id, nombre, {tipo_select}, descripcion, estado
        FROM proyectos_constructora
        ORDER BY id DESC
    """)

    proyectos = cur.fetchall()
    cur.close()
    return proyectos


def init_contactos_mysql(mysql):
    cur = mysql.connection.cursor()

    cur.execute("""
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
    """)

    mysql.connection.commit()
    cur.close()

    asegurar_columna(mysql, "clientes_interesados", "fecha_contacto", "TIMESTAMP NULL")
    asegurar_auto_increment(mysql, "clientes_interesados")


def add_contacto_mysql(mysql, nombre, telefono, correo, servicio, mensaje):
    cur = mysql.connection.cursor()

    try:
        cur.execute("""
            INSERT INTO clientes_interesados
            (nombre, telefono, correo, servicio, mensaje)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nombre.strip(),
            telefono.strip(),
            correo.strip(),
            servicio.strip(),
            mensaje.strip()
        ))

        mysql.connection.commit()

    except Exception:
        mysql.connection.rollback()
        raise

    finally:
        cur.close()


def get_contactos_mysql(mysql):
    cur = mysql.connection.cursor()

    fecha_contacto_select = (
        "fecha_contacto"
        if columna_existe(mysql, "clientes_interesados", "fecha_contacto")
        else "NULL AS fecha_contacto"
    )

    cur.execute(f"""
        SELECT id, nombre, telefono, correo, servicio, mensaje,
               fecha_envio, estado, {fecha_contacto_select}
        FROM clientes_interesados
        ORDER BY fecha_envio ASC
    """)

    contactos = cur.fetchall()
    cur.close()
    return contactos


def actualizar_prioridades_mysql(mysql):
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE clientes_interesados
        SET estado = 'Prioridad Alta'
        WHERE estado = 'Pendiente'
        AND TIMESTAMPDIFF(HOUR, fecha_envio, NOW()) >= 24
    """)

    mysql.connection.commit()
    cur.close()


def marcar_contactado_mysql(mysql, contacto_id):
    cur = mysql.connection.cursor()

    if columna_existe(mysql, "clientes_interesados", "fecha_contacto"):
        cur.execute("""
            UPDATE clientes_interesados
            SET estado = 'Contactado',
                fecha_contacto = NOW()
            WHERE id = %s
        """, (contacto_id,))
    else:
        cur.execute("""
            UPDATE clientes_interesados
            SET estado = 'Contactado'
            WHERE id = %s
        """, (contacto_id,))

    mysql.connection.commit()
    cur.close()