import email
from tkinter import INSERT
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app
from flask_mysqldb import MySQL
import random
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import re
import uuid
from datetime import datetime
from dotenv import load_dotenv
import pymysql
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from io import BytesIO

from db_utils_mysql import (
    add_usuario_mysql,
    update_email_mysql,
    set_email_confirmado_mysql,
    get_usuario_by_username_mysql,
    get_usuario_by_email_mysql,
    init_mysql_db,
    get_proyectos_mysql,
    add_proyecto_mysql,
    init_contactos_mysql,
    add_contacto_mysql,
    get_contactos_mysql,
    actualizar_prioridades_mysql,
    marcar_contactado_mysql
)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template ('index.html')

# Configuración de MySQL (ajusta según tu XAMPP)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#Configuracion e-mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'False'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

UPLOAD_FOLDER = os.path.join('static', 'imagenes')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def imagen_permitida(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


with app.app_context():
    init_mysql_db(mysql)
    init_contactos_mysql(mysql)


def es_contrasena_segura(password):
    # Al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password)):
        return False
    return True

# def enviar_correo_simulado(destino, asunto, cuerpo):
#     print(f"\n--- Simulación de envío de correo ---\nPara: {destino}\nAsunto: {asunto}\nCuerpo: {cuerpo}\n------------------------------\n")

def enviar_codigo_correo(destinatario, codigo):
    msg = Message(
        subject='Verificación de cuenta - Constructora CiviWeb Manager',
        recipients=[destinatario]
    )
    msg.body = f"""
    Querido usuario,
    Te damos la bienvenida a Constructora CiviWeb Manager.
    
    Para completar tu registro y activar tu cuenta, utiliza el siguiente código de verificación:

--------------------------------------------------
        {codigo}
--------------------------------------------------

Este código es personal y tiene una validez limitada. 
Por favor, no lo compartas con nadie.

Si no realizaste este registro, puedes ignorar este mensaje.

Atentamente,
Equipo Constructora CiviWeb Manager
"""

    mail.send(msg)


def enviar_codigo_recuperacion(destinatario, codigo):
    msg = Message(
        subject='Recuperación de contraseña - CiviWeb Manager',
        recipients=[destinatario]
    )

    msg.body = f"""
    Hola,
    
    Recibimos una solicitud para restablecer tu contraseña en CiviWeb Manager.
    
    Tu código de recuperación es:
    ------------------------------
    
    {codigo}
    ------------------------------
    Ingresa este código en la plataforma para crear una nueva contraseña.
    
    Si no solicitaste este cambio, ignora este correo.
    
    Atentamente,
    
    Equipo CiviWeb Manager
    
    """

    mail.send(msg)

    

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = get_usuario_by_username_mysql(mysql, username)

        if user and check_password_hash(user['password_hash'], password):

            if not user['activo']:
                flash(
                    'Su cuenta ha sido deshabilitada por un administrador.',
                    'danger'
                )
                return render_template('login.html')

            if not es_contrasena_segura(password):
                flash(
                    'La contraseña no es segura. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.',
                    'danger'
                )
                return render_template('login.html')

            if not user['email_confirmado']:
                flash(
                    'Debes confirmar tu correo electrónico antes de acceder.',
                    'danger'
                )
                return render_template('login.html')

            session['usuario'] = username
            session['rol'] = user['rol']

            return redirect(url_for('dashboard'))

        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/desactivar_usuario/<int:id>')
def desactivar_usuario(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()

    # Evitar que el administrador se desactive a sí mismo
    cur.execute(
        "SELECT username FROM usuarios WHERE id = %s",
        (id,)
    )
    usuario_db = cur.fetchone()

    if usuario_db and usuario_db['username'] == session['usuario']:
        flash('No puedes desactivar tu propia cuenta.', 'danger')
        cur.close()
        return redirect(url_for('usuarios'))

    cur.execute(
        "UPDATE usuarios SET activo = 0 WHERE id = %s",
        (id,)
    )

    mysql.connection.commit()
    cur.close()

    flash('Usuario desactivado correctamente.', 'success')

    return redirect(url_for('usuarios'))

@app.route('/activar_usuario/<int:id>')
def activar_usuario(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para realizar esta acción.', 'danger')
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE usuarios SET activo = 1 WHERE id = %s",
        (id,)
    )

    mysql.connection.commit()
    cur.close()

    flash('Usuario activado correctamente.', 'success')

    return redirect(url_for('usuarios'))

# REGISTRO
@app.route('/register', methods=['GET', 'POST'])
def register():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para crear usuarios.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']

        if not es_contrasena_segura(password):
            flash('La contraseña no es segura. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.', 'danger')
            return render_template('register.html', form=request.form, 
                                   limpiar_password=True)

        if get_usuario_by_username_mysql(mysql, username):
            flash('El usuario ya existe.', 'danger')
            return render_template('register.html', form=request.form, 
                                   limpiar_username=True)
        
        if get_usuario_by_email_mysql(mysql, email):
            flash('El correo ya está registrado.', 'danger')
            return render_template('register.html', form=request.form, 
                                   limpiar_email=True)
        
        password_hash = generate_password_hash(password)
        add_usuario_mysql(mysql, username, password_hash, email, rol)

        #  envío de correo de confirmación por codigo

        import random
        codigo = str(random.randint(100000, 999999))
        session['codigo_confirmacion'] = codigo
        session['correo_confirmacion'] = email
        
        enviar_codigo_correo(email, codigo)


        flash('Registro exitoso. Hemos enviado un código a tu correo.', 'success')
        return redirect(url_for('confirmar_codigo'))
    return render_template('register.html')

# CONFIRMAR CORREO
@app.route('/confirmar_codigo', methods=['GET', 'POST'])
def confirmar_codigo():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']

        if codigo_ingresado == session.get('codigo_confirmacion'):
            email = session.get('correo_confirmacion')

            set_email_confirmado_mysql(mysql, email)

            session.pop('codigo_confirmacion', None)
            session.pop('correo_confirmacion', None)

            flash('Correo confirmado correctamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Código incorrecto.', 'danger')

    return render_template('confirmar_codigo.html')


# RECUPERAR CONTRASEÑA (simulado)
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        email = request.form['email']
        user = get_usuario_by_email_mysql(mysql, email)

        if user:
            codigo = str(random.randint(100000, 999999))

            session['codigo_recuperacion'] = codigo
            session['correo_recuperacion'] = email
            session['usuario_recuperacion'] = user['username']

            enviar_codigo_recuperacion(email, codigo)

            flash('Hemos enviado un código de recuperación a tu correo.', 'success')
            return redirect(url_for('verificar_codigo_recuperacion'))
        else:
            flash('Correo no encontrado.', 'danger')

    return render_template('recover.html')

@app.route('/verificar_codigo_recuperacion', methods=['GET', 'POST'])
def verificar_codigo_recuperacion():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']

        if codigo_ingresado == session.get('codigo_recuperacion'):
            flash('Código verificado correctamente. Ahora puedes cambiar tu contraseña.', 'success')
            return redirect(url_for('reset_password_codigo'))
        else:
            flash('Código incorrecto.', 'danger')

    return render_template('verificar_codigo_recuperacion.html')

# RESTABLECER CONTRASEÑA NO ES SIMULADO
@app.route('/reset_password_codigo', methods=['GET', 'POST'])
def reset_password_codigo():
    if 'usuario_recuperacion' not in session:
        flash('Primero debes verificar tu correo.', 'danger')
        return redirect(url_for('recover'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('reset_password.html')

        if not es_contrasena_segura(password):
            flash('La contraseña no es segura. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.', 'danger')
            return render_template('reset_password.html')

        password_hash = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE usuarios SET password_hash = %s WHERE username = %s',
            (password_hash, session['usuario_recuperacion'])
        )
        mysql.connection.commit()
        cur.close()

        session.pop('codigo_recuperacion', None)
        session.pop('correo_recuperacion', None)
        session.pop('usuario_recuperacion', None)

        flash('Contraseña restablecida correctamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/modificar_correo', methods=['GET', 'POST'])
def modificar_correo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nuevo_email = request.form['nuevo_email']
        username = session['usuario']

        usuario_existente = get_usuario_by_email_mysql(mysql, nuevo_email)

        if usuario_existente:
            flash('Ese correo ya esta registrado. Usa otro correo.', 'danger')
            return render_template('modificar_correo.html')

        update_email_mysql(mysql, username, nuevo_email)

        flash('Correo actualizado correctamente.', 'success')
        return redirect(url_for('modificar_correo'))

    return render_template('modificar_correo.html')

@app.route('/mostrar_confirmacion')
def mostrar_confirmacion():
    return render_template('mostrar_confirmacion.html')

@app.route('/mostrar_recuperacion')
def mostrar_recuperacion():
    return render_template('mostrar_recuperacion.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE estado = 'Activo'")
    proyectos_activos = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    inmuebles_disponibles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM ventas")
    ventas_registradas = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM usuarios")
    usuarios_sistema = cur.fetchone()['total']

    cur.close()

    return render_template(
        'dashboard.html',
        usuario=session['usuario'],
        rol=session.get('rol', 'usuario'),
        proyectos_activos=proyectos_activos,
        inmuebles_disponibles=inmuebles_disponibles,
        ventas_registradas=ventas_registradas,
        usuarios_sistema=usuarios_sistema
    )

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada correctamente.', 'success')
    return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para ver usuarios.', 'danger')
        return redirect(url_for('dashboard'))

    buscar = request.args.get('buscar', '')
    rol = request.args.get('rol', '')

    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 10
    offset = (pagina - 1) * por_pagina

    query = """
        SELECT id, username, email, rol, email_confirmado, activo
        FROM usuarios
        WHERE 1=1
    """

    valores = []

    count_query = """
        SELECT COUNT(*) AS total
        FROM usuarios
        WHERE 1=1
    """

    count_valores = []

    if buscar:
        filtro_busqueda = """
            AND (
                username LIKE %s
                OR email LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        query += filtro_busqueda
        count_query += filtro_busqueda

        valores.extend([busqueda, busqueda])
        count_valores.extend([busqueda, busqueda])

    if rol:
        query += " AND rol = %s "
        count_query += " AND rol = %s "

        valores.append(rol)
        count_valores.append(rol)

    query += " ORDER BY id DESC LIMIT %s OFFSET %s "
    valores.extend([por_pagina, offset])

    cur = mysql.connection.cursor()

    cur.execute(count_query, count_valores)
    total_registros = cur.fetchone()['total']

    total_paginas = (total_registros + por_pagina - 1) // por_pagina

    cur.execute(query, valores)
    usuarios = cur.fetchall()

    cur.close()

    return render_template(
        'usuarios.html',
        usuarios=usuarios,
        buscar=buscar,
        rol=rol,
        pagina=pagina,
        total_paginas=total_paginas
    )


@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para eliminar usuarios.', 'danger')
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios'))


@app.route('/inmuebles')
def inmuebles():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    busqueda = request.args.get('busqueda', '')
    tipo = request.args.get('tipo', '')
    estado = request.args.get('estado', '')

    query = "SELECT * FROM inmuebles WHERE 1=1"
    valores = []

    if busqueda:
        query += " AND (titulo LIKE %s OR ubicacion LIKE %s OR descripcion LIKE %s)"
        valores.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])

    if tipo:
        query += " AND tipo = %s"
        valores.append(tipo)

    if estado:
        query += " AND estado = %s"
        valores.append(estado)

    query += " ORDER BY id DESC"

    cur = mysql.connection.cursor()
    cur.execute(query, valores)
    inmuebles = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles")
    total_inmuebles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    disponibles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Reservado'")
    reservados = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Vendido'")
    vendidos = cur.fetchone()['total']

    cur.close()

    return render_template(
        'inmuebles.html',
        inmuebles=inmuebles,
        total_inmuebles=total_inmuebles,
        disponibles=disponibles,
        reservados=reservados,
        vendidos=vendidos,
        busqueda=busqueda,
        tipo=tipo,
        estado=estado
    )

@app.route('/inmobiliaria_admin')
def inmobiliaria_admin():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template('inmobiliaria_admin.html')

@app.route('/registrar_inmueble', methods=['GET', 'POST'])
def registrar_inmueble():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        tipo = request.form['tipo']
        tipo_negocio = request.form['tipo_negocio']
        ubicacion = request.form['ubicacion'].strip()
        precio = request.form['precio']
        estado = request.form['estado']
        descripcion = request.form['descripcion'].strip()
        archivo_imagen = request.files.get('imagen')

        if not titulo or not tipo or not ubicacion or not precio or not estado:
            flash('Todos los campos obligatorios deben estar completos.', 'danger')
            return render_template('registrar_inmueble.html', form=request.form)

        try:
            precio = float(precio)
            if precio <= 0:
                flash('El precio debe ser mayor a cero.', 'danger')
                return render_template('registrar_inmueble.html', form=request.form)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('registrar_inmueble.html', form=request.form)

        nombre_imagen = ''

        if archivo_imagen and archivo_imagen.filename != '':
            if not imagen_permitida(archivo_imagen.filename):
                flash('Formato de imagen no permitido. Usa PNG, JPG, JPEG, WEBP o MP4.', 'danger')
                return render_template('registrar_inmueble.html', form=request.form)

            nombre_original = secure_filename(archivo_imagen.filename)
            extension = nombre_original.rsplit('.', 1)[1].lower()
            nombre_imagen = f"inmueble_{uuid.uuid4().hex}.{extension}"

            ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen)
            archivo_imagen.save(ruta_imagen)

        cur = mysql.connection.cursor()
        
        cur.execute("""
                    INSERT INTO inmuebles (titulo, tipo, tipo_negocio, ubicacion, precio, estado, descripcion, imagen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (titulo, tipo, tipo_negocio, ubicacion, precio, estado, descripcion, nombre_imagen))

        inmueble_id = cur.lastrowid

        archivos_galeria = request.files.getlist('galeria')

        for archivo in archivos_galeria:
            if archivo and archivo.filename != '':
                if imagen_permitida(archivo.filename):
                    nombre_original = secure_filename(archivo.filename)
                    extension = nombre_original.rsplit('.', 1)[1].lower()
                    nombre_archivo = f"inmueble_{uuid.uuid4().hex}.{extension}"

                    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                    archivo.save(ruta_archivo)

                    tipo_archivo = 'video' if extension == 'mp4' else 'imagen'

                    cur.execute("""
                        INSERT INTO inmueble_multimedia (inmueble_id, archivo, tipo)
                        VALUES (%s, %s, %s)
                    """, (inmueble_id, nombre_archivo, tipo_archivo))

        mysql.connection.commit()
        cur.close()

        flash('Inmueble publicado exitosamente con su galería multimedia.', 'success')
        return redirect(url_for('inmuebles'))

    return render_template('registrar_inmueble.html')


@app.route('/eliminar_multimedia/<int:id>/<int:inmueble_id>')
def eliminar_multimedia(id, inmueble_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT archivo FROM inmueble_multimedia WHERE id = %s", (id,))
    multimedia = cur.fetchone()

    if multimedia:
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], multimedia['archivo'])

        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        cur.execute("DELETE FROM inmueble_multimedia WHERE id = %s", (id,))
        mysql.connection.commit()

        flash('Archivo eliminado de la galería correctamente.', 'success')

    cur.close()

    return redirect(url_for('editar_inmueble', id=inmueble_id))

@app.route('/editar_inmueble/<int:id>', methods=['GET', 'POST'])
def editar_inmueble(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM inmuebles WHERE id = %s", (id,))
    inmueble = cur.fetchone()

    if not inmueble:
        cur.close()
        flash('El inmueble no existe.', 'danger')
        return redirect(url_for('inmuebles'))

    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        tipo = request.form['tipo']
        tipo_negocio = request.form['tipo_negocio']
        ubicacion = request.form['ubicacion'].strip()
        precio = request.form['precio']
        estado = request.form['estado']
        descripcion = request.form['descripcion'].strip()

        archivo_imagen = request.files.get('imagen')
        nombre_imagen = inmueble['imagen']

        if archivo_imagen and archivo_imagen.filename != '':
            if not imagen_permitida(archivo_imagen.filename):
                flash('Formato de imagen no permitido.', 'danger')
                return redirect(url_for('editar_inmueble', id=id))

            nombre_original = secure_filename(archivo_imagen.filename)
            extension = nombre_original.rsplit('.', 1)[1].lower()
            nombre_imagen = f"inmueble_{uuid.uuid4().hex}.{extension}"

            ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen)
            archivo_imagen.save(ruta_imagen)

        cur.execute("""
                    UPDATE inmuebles
                    SET titulo=%s, tipo=%s, tipo_negocio=%s, ubicacion=%s, precio=%s, estado=%s, descripcion=%s, imagen=%s
                    WHERE id=%s
                    """, (titulo, tipo, tipo_negocio, ubicacion, precio, estado, descripcion, nombre_imagen, id))

        archivos_galeria = request.files.getlist('galeria')

        for archivo in archivos_galeria:
            if archivo and archivo.filename != '':
                if imagen_permitida(archivo.filename):
                    nombre_original = secure_filename(archivo.filename)
                    extension = nombre_original.rsplit('.', 1)[1].lower()
                    nombre_archivo = f"inmueble_{uuid.uuid4().hex}.{extension}"

                    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                    archivo.save(ruta_archivo)

                    tipo_archivo = 'video' if extension == 'mp4' else 'imagen'

                    cur.execute("""
                        INSERT INTO inmueble_multimedia (inmueble_id, archivo, tipo)
                        VALUES (%s, %s, %s)
                    """, (id, nombre_archivo, tipo_archivo))

        mysql.connection.commit()

        flash('Inmueble actualizado correctamente.', 'success')
        cur.close()
        return redirect(url_for('inmuebles'))
    cur.execute("SELECT * FROM inmuebles WHERE id = %s", (id,))
    inmueble = cur.fetchone()
    cur.execute("""
                 SELECT *
                FROM inmueble_multimedia
                WHERE inmueble_id = %s
                """, (id,))
    galeria = cur.fetchall()
    cur.close()
    return render_template(
        'editar_inmueble.html',
        inmueble=inmueble,
        galeria=galeria
        )

@app.route('/eliminar_inmueble/<int:id>')
def eliminar_inmueble(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT archivo FROM inmueble_multimedia WHERE inmueble_id = %s", (id,))
    archivos = cur.fetchall()

    for item in archivos:
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], item['archivo'])
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

    cur.execute("DELETE FROM inmueble_multimedia WHERE inmueble_id = %s", (id,))

    cur.execute("DELETE FROM inmuebles WHERE id = %s", (id,))

    mysql.connection.commit()
    cur.close()

    flash('Inmueble eliminado correctamente.', 'success')
    return redirect(url_for('inmuebles'))

@app.route('/constructora')
def constructora_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('constructora_admin.html')

@app.route('/ventas_admin', methods=['GET', 'POST'])
def ventas_admin():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexion = mysql.connection
    cur = conexion.cursor()

    # =========================
    # PAGINACIÓN Y FILTROS
    # =========================
    pagina = request.args.get('page', 1, type=int)
    buscar = request.args.get('buscar', '')
    metodo_pago = request.args.get('metodo_pago', '')

    por_pagina = 10
    offset = (pagina - 1) * por_pagina

    # =========================
    # REGISTRAR VENTA
    # =========================
    if request.method == 'POST':

        inmueble_id = request.form['inmueble_id']
        cliente_id = request.form['cliente_id']
        valor_venta = float(request.form['valor_venta'])
        anticipo = float(request.form['anticipo'])

        metodo_pago = request.form['metodo_pago']

        observacion = request.form['observacion']

        saldo = valor_venta - anticipo

        if saldo <= 0:
            estado_pago = 'Pagado'
        elif anticipo > 0:
            estado_pago = 'Pendiente'
        else:
            estado_pago = 'Sin anticipo'

        cur.execute("""
            INSERT INTO ventas (
                inmueble_id,
                cliente_id,
                valor_venta,
                metodo_pago,
                anticipo,
                saldo,
                estado_pago,
                observacion
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            inmueble_id,
            cliente_id,
            valor_venta,
            metodo_pago,
            anticipo,
            saldo,
            estado_pago,
            observacion
        ))

        cur.execute("""
            UPDATE inmuebles
            SET estado = 'Vendido'
            WHERE id = %s
        """, (inmueble_id,))

        conexion.commit()

        flash('Venta registrada correctamente.', 'success')

        return redirect(url_for('ventas_admin'))

    # =========================
    # INMUEBLES DISPONIBLES
    # =========================
    cur.execute("""
        SELECT *
        FROM inmuebles
        WHERE estado = 'Disponible'
        ORDER BY id DESC
    """)
    inmuebles_disponibles = cur.fetchall()

    # =========================
    # CLIENTES
    # =========================
    cur.execute("""
        SELECT *
        FROM clientes_inmobiliaria
        ORDER BY nombre ASC
    """)
    clientes = cur.fetchall()

    # =========================
    # CONSULTA VENTAS PAGINADAS
    # =========================
    sql_ventas = """
        SELECT SQL_CALC_FOUND_ROWS
            v.id,
            v.valor_venta,
            v.fecha,
            v.observacion,
            v.metodo_pago,
            v.anticipo,
            v.saldo,
            v.estado_pago,
            i.titulo AS inmueble,
            i.ubicacion,
            c.nombre AS cliente,
            c.documento
        FROM ventas v
        INNER JOIN inmuebles i
            ON v.inmueble_id = i.id
        INNER JOIN clientes_inmobiliaria c
            ON v.cliente_id = c.id
        WHERE 1=1
    """

    valores = []

    # BUSCADOR
    if buscar:

        sql_ventas += """
            AND (
                c.nombre LIKE %s
                OR i.titulo LIKE %s
                OR i.ubicacion LIKE %s
                OR c.documento LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        valores.extend([
            busqueda,
            busqueda,
            busqueda,
            busqueda
        ])

    # FILTRO MÉTODO DE PAGO
    if metodo_pago:

        sql_ventas += """
            AND v.metodo_pago = %s
        """

        valores.append(metodo_pago)

    sql_ventas += """
        ORDER BY v.fecha DESC
        LIMIT %s OFFSET %s
    """

    valores.extend([por_pagina, offset])

    cur.execute(sql_ventas, valores)

    ventas = cur.fetchall()

    # =========================
    # TOTAL PARA PAGINACIÓN
    # =========================
    cur.execute("SELECT FOUND_ROWS() AS total")

    total = cur.fetchone()['total']

    total_paginas = (total + por_pagina - 1) // por_pagina

    # =========================
    # ESTADÍSTICAS
    # =========================
    cur.execute("""
        SELECT COALESCE(SUM(valor_venta), 0) AS total
        FROM ventas
    """)
    total_vendido = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM ventas
    """)
    total_ventas = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM ventas
        WHERE MONTH(fecha) = MONTH(CURDATE())
        AND YEAR(fecha) = YEAR(CURDATE())
    """)
    ventas_mes = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM inmuebles
        WHERE estado = 'Vendido'
    """)
    inmuebles_vendidos = cur.fetchone()['total']

    # =========================
    # ÚLTIMAS VENTAS
    # =========================
    cur.execute("""
        SELECT
            v.id,
            c.nombre AS cliente,
            v.valor_venta,
            v.fecha,
            i.titulo
        FROM ventas v
        INNER JOIN inmuebles i
            ON v.inmueble_id = i.id
        INNER JOIN clientes_inmobiliaria c
            ON v.cliente_id = c.id
        ORDER BY v.fecha DESC
        LIMIT 5
    """)

    ultimas_ventas = cur.fetchall()

    # =========================
    # GRÁFICO
    # =========================
    cur.execute("""
        SELECT MONTH(fecha) AS mes,
               COUNT(*) AS total
        FROM ventas
        WHERE YEAR(fecha) = YEAR(CURDATE())
        GROUP BY MONTH(fecha)
        ORDER BY MONTH(fecha)
    """)

    ventas_grafico = cur.fetchall()

    cur.close()

    return render_template(
        'ventas_admin.html',
        inmuebles_disponibles=inmuebles_disponibles,
        clientes=clientes,
        ventas=ventas,
        total_vendido=total_vendido,
        total_ventas=total_ventas,
        ventas_mes=ventas_mes,
        inmuebles_vendidos=inmuebles_vendidos,
        ultimas_ventas=ultimas_ventas,
        ventas_grafico=ventas_grafico,
        pagina=pagina,
        total_paginas=total_paginas,
        buscar=buscar,
        metodo_pago=metodo_pago
    )



@app.route('/completar_pago/<int:id>')
def completar_pago(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE ventas
        SET anticipo = valor_venta,
            saldo = 0,
            estado_pago = 'Pagado'
        WHERE id = %s
    """, (id,))

    mysql.connection.commit()
    cur.close()

    flash('Pago completado correctamente.', 'success')
    return redirect(url_for('ventas_admin'))

@app.route('/factura_venta/<int:id>')
def factura_venta(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT 
            v.id,
            v.fecha,
            v.valor_venta,
            v.metodo_pago,
            v.anticipo,
            v.saldo,
            v.estado_pago,
            v.observacion,
            i.titulo AS inmueble,
            i.ubicacion,
            c.nombre AS cliente,
            c.documento,
            c.telefono,
            c.email
        FROM ventas v
        INNER JOIN inmuebles i ON v.inmueble_id = i.id
        INNER JOIN clientes_inmobiliaria c ON v.cliente_id = c.id
        WHERE v.id = %s
    """, (id,))

    venta = cur.fetchone()
    cur.close()

    if not venta:
        flash('La venta no existe.', 'danger')
        return redirect(url_for('ventas_admin'))

    return render_template('factura_venta.html', venta=venta)

@app.route('/clientes_admin', methods=['GET', 'POST'])
def clientes_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        documento = request.form['documento'].strip()
        telefono = request.form['telefono'].strip()
        email = request.form['email'].strip()
        direccion = request.form['direccion'].strip()
        tipo_interes = request.form['tipo_interes']
        observacion = request.form['observacion'].strip()

        if not nombre or not telefono:
            flash('El nombre y el teléfono son obligatorios.', 'danger')
            return redirect(url_for('clientes_admin'))

        cur.execute("""
            INSERT INTO clientes_inmobiliaria
            (nombre, documento, telefono, email, direccion, tipo_interes, observacion)

            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            nombre,
            documento,
            telefono,
            email,
            direccion,
            tipo_interes,
            observacion
        ))

        mysql.connection.commit()
        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes_admin'))

    # FILTROS
    buscar = request.args.get('buscar', '')
    tipo_interes = request.args.get('tipo_interes', '')

    query = """
        SELECT *
        FROM clientes_inmobiliaria
        WHERE 1=1
    """

    valores = []

    if buscar:

        query += """
            AND (
                nombre LIKE %s
                OR telefono LIKE %s
                OR email LIKE %s
            )
        """
        busqueda = f"%{buscar}%"
        valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    if tipo_interes:

        query += " AND tipo_interes = %s "
        valores.append(tipo_interes)
    query += " ORDER BY id DESC "

    # ESTADÍSTICAS
    cur.execute("SELECT COUNT(*) AS total FROM clientes_inmobiliaria")
    total_clientes = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM clientes_inmobiliaria
        WHERE tipo_interes = 'Compra'
    """)

    clientes_compra = cur.fetchone()['total']

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM clientes_inmobiliaria
        WHERE tipo_interes = 'Arriendo'
    """)

    clientes_arriendo = cur.fetchone()['total']

    # PAGINACIÓN
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 10
    offset = (pagina - 1) * por_pagina

    count_query = """
        SELECT COUNT(*) AS total
        FROM clientes_inmobiliaria
        WHERE 1=1
    """

    count_valores = []

    if buscar:

        count_query += """
            AND (
                nombre LIKE %s
                OR telefono LIKE %s
                OR email LIKE %s
            )
        """

        busqueda = f"%{buscar}%"
        count_valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    if tipo_interes:
        count_query += " AND tipo_interes = %s "
        count_valores.append(tipo_interes)

    cur.execute(count_query, count_valores)
    total_registros = cur.fetchone()['total']

    # CONSULTA FINAL PAGINADA
    query += " LIMIT %s OFFSET %s "
    valores.extend([por_pagina, offset])
    cur.execute(query, valores)
    clientes = cur.fetchall()
    total_paginas = (total_registros + por_pagina - 1) // por_pagina
    cur.close()

    return render_template(
        'clientes_admin.html',
        clientes=clientes,
        total_clientes=total_clientes,
        clientes_compra=clientes_compra,
        clientes_arriendo=clientes_arriendo,
        buscar=buscar,
        tipo_interes=tipo_interes,
        pagina=pagina,
        total_paginas=total_paginas
    )


@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM clientes_inmobiliaria WHERE id = %s", (id,))

    mysql.connection.commit()
    cur.close()

    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes_admin'))

@app.route('/compras_admin')
def compras_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COALESCE(SUM(valor), 0) AS total FROM compras")
    total_compras = cur.fetchone()['total']

    cur.execute("SELECT COUNT(DISTINCT proveedor) AS total FROM compras")
    total_proveedores = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM compras WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE())")
    compras_mes = cur.fetchone()['total']

    cur.execute("""
        SELECT concepto, proveedor, valor, fecha
        FROM compras
        ORDER BY fecha DESC
        LIMIT 5
    """)
    ultimas_compras = cur.fetchall()

    cur.execute("""
        SELECT concepto, SUM(valor) AS total
        FROM compras
        GROUP BY concepto
        ORDER BY total DESC
        LIMIT 5
    """)
    compras_grafico = cur.fetchall()

    cur.close()

    return render_template(
        'compras_admin.html',
        total_compras=total_compras,
        total_proveedores=total_proveedores,
        compras_mes=compras_mes,
        ultimas_compras=ultimas_compras,
        compras_grafico=compras_grafico
    )

@app.route('/reportes_admin')
def reportes_admin():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # TOTAL INGRESOS
    cur.execute("SELECT COALESCE(SUM(valor_venta), 0) AS total FROM ventas")
    ingresos = cur.fetchone()['total']

    # TOTAL VENTAS REGISTRADAS
    cur.execute("SELECT COUNT(*) AS total FROM ventas")
    total_ventas = cur.fetchone()['total']

    # INMUEBLES DISPONIBLES
    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    inmuebles_disponibles = cur.fetchone()['total']

    # ESTADO DE INMUEBLES
    cur.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END), 0) AS disponibles,
            COALESCE(SUM(CASE WHEN estado = 'Reservado' THEN 1 ELSE 0 END), 0) AS reservados,
            COALESCE(SUM(CASE WHEN estado = 'Vendido' THEN 1 ELSE 0 END), 0) AS vendidos
        FROM inmuebles
    """)
    estado_inmuebles = cur.fetchone()

    # INGRESOS MENSUALES
    cur.execute("""
        SELECT MONTH(fecha) AS mes,
               COALESCE(SUM(valor_venta), 0) AS ingresos
        FROM ventas
        GROUP BY MONTH(fecha)
        ORDER BY mes
    """)
    ingresos_mensuales = cur.fetchall()

    cur.close()

    # Como no vas a usar compras, egresos queda vacío
    egresos_grafico = []

    return render_template(
        'reportes_admin.html',
        ingresos=ingresos,
        total_ventas=total_ventas,
        inmuebles_disponibles=inmuebles_disponibles,
        ingresos_mensuales=ingresos_mensuales,

        # Estos nombres los dejo para que el HTML no dé error con tojson
        estado_inmuebles=estado_inmuebles,
        ingresos_grafico=ingresos_mensuales,
        egresos_grafico=egresos_grafico
    )

@app.route('/editar_proyecto/<int:id>', methods=['GET', 'POST'])
def editar_proyecto(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Buscar proyecto
    cur.execute("""
        SELECT *
        FROM proyectos_constructora
        WHERE id = %s
    """, (id,))

    proyecto = cur.fetchone()

    if not proyecto:
        flash('Proyecto no encontrado.', 'danger')
        return redirect(url_for('proyectos_admin'))

    if request.method == 'POST':

        nombre = request.form['nombre']
        tipo_trabajo = request.form['tipo_trabajo']
        descripcion = request.form['descripcion']
        estado = request.form['estado']

        cur.execute("""
            UPDATE proyectos_constructora
            SET nombre=%s,
                tipo_trabajo=%s,
                descripcion=%s,
                estado=%s
            WHERE id=%s
        """, (
            nombre,
            tipo_trabajo,
            descripcion,
            estado,
            id
        ))

        mysql.connection.commit()
        cur.close()

        flash('Proyecto actualizado correctamente.', 'success')

        return redirect(url_for('proyectos_admin'))

    cur.close()

    return render_template(
        'editar_Proyecto.html',
        proyecto=proyecto
    )

@app.route('/eliminar_proyecto/<int:id>')
def eliminar_proyecto(id):

    if 'usuario' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()

    # Primero eliminar relación cliente-proyecto
    cur.execute("""
        DELETE FROM cliente_proyecto
        WHERE proyecto_id = %s
    """, (id,))

    # Luego eliminar proyecto
    cur.execute("""
        DELETE FROM proyectos_constructora
        WHERE id = %s
    """, (id,))

    mysql.connection.commit()
    cur.close()
    flash('Proyecto eliminado correctamente.', 'success')
    return redirect(url_for('proyectos_admin'))

@app.route('/inmobiliaria')
def inmobiliaria_publica():
        cur = mysql.connection.cursor()
        
        cur.execute("""
        SELECT * FROM inmuebles
        WHERE estado IN ('Disponible', 'Reservado')
        ORDER BY id DESC
    """)
        inmuebles_publicos = cur.fetchall()
        
        for inmueble in inmuebles_publicos:
            cur.execute("""
            SELECT * FROM inmueble_multimedia
            WHERE inmueble_id = %s
            ORDER BY id ASC
        """, (inmueble['id'],))

        inmueble['galeria'] = cur.fetchall()
        
        cur.close()
        
        return render_template(
        'inmobiliaria_publica.html',
        inmuebles_publicos=inmuebles_publicos
    )

@app.route('/reservas_admin', methods=['GET', 'POST'])
def reservas_admin():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if request.method == 'POST':

        inmueble_id = request.form['inmueble_id']
        cliente_id = request.form['cliente_id']
        fecha_limite = request.form['fecha_limite']
        valor_reserva = request.form['valor_reserva']
        observacion = request.form['observacion']

        cur.execute("""
            INSERT INTO reservas (
                inmueble_id,
                cliente_id,
                fecha_limite,
                valor_reserva,
                observacion
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (
            inmueble_id,
            cliente_id,
            fecha_limite,
            valor_reserva,
            observacion
        ))

        cur.execute("""
            UPDATE inmuebles
            SET estado = 'Reservado'
            WHERE id = %s
        """, (inmueble_id,))

        mysql.connection.commit()

        flash('Reserva registrada correctamente.', 'success')

        return redirect(url_for('reservas_admin'))

    # =========================
    # DATOS FORMULARIO
    # =========================

    cur.execute("""
        SELECT *
        FROM inmuebles
        WHERE estado = 'Disponible'
        ORDER BY id DESC
    """)

    inmuebles = cur.fetchall()

    cur.execute("""
        SELECT *
        FROM clientes_inmobiliaria
        ORDER BY nombre ASC
    """)

    clientes = cur.fetchall()

    # =========================
    # FILTROS
    # =========================

    buscar = request.args.get('buscar', '')
    estado = request.args.get('estado', '')

    # =========================
    # PAGINACIÓN
    # =========================

    pagina = request.args.get('pagina', 1, type=int)

    por_pagina = 5

    offset = (pagina - 1) * por_pagina

    query = """
        SELECT
            r.*,
            i.titulo AS inmueble,
            i.ubicacion,
            c.nombre AS cliente,
            c.telefono

        FROM reservas r

        INNER JOIN inmuebles i
            ON r.inmueble_id = i.id

        INNER JOIN clientes_inmobiliaria c
            ON r.cliente_id = c.id

        WHERE 1=1
    """

    valores = []

    if buscar:

        query += """
            AND (
                c.nombre LIKE %s
                OR i.titulo LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        valores.extend([
            busqueda,
            busqueda
        ])

    if estado:

        query += " AND r.estado = %s "

        valores.append(estado)

    query += " ORDER BY r.fecha_reserva DESC "

    # =========================
    # CONTAR REGISTROS
    # =========================

    count_query = """
        SELECT COUNT(*) AS total

        FROM reservas r

        INNER JOIN inmuebles i
            ON r.inmueble_id = i.id

        INNER JOIN clientes_inmobiliaria c
            ON r.cliente_id = c.id

        WHERE 1=1
    """

    count_valores = []

    if buscar:

        count_query += """
            AND (
                c.nombre LIKE %s
                OR i.titulo LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        count_valores.extend([
            busqueda,
            busqueda
        ])

    if estado:

        count_query += " AND r.estado = %s "

        count_valores.append(estado)

    cur.execute(count_query, count_valores)

    total_registros = cur.fetchone()['total']

    total_paginas = (
        total_registros + por_pagina - 1
    ) // por_pagina

    # =========================
    # CONSULTA FINAL
    # =========================

    query += " LIMIT %s OFFSET %s "

    valores.extend([
        por_pagina,
        offset
    ])

    cur.execute(query, valores)

    reservas = cur.fetchall()

    cur.close()

    return render_template(
        'reservas_admin.html',
        reservas=reservas,
        inmuebles=inmuebles,
        clientes=clientes,
        buscar=buscar,
        estado=estado,
        pagina=pagina,
        total_paginas=total_paginas
    )

@app.route('/cancelar_reserva/<int:id>/<int:inmueble_id>')
def cancelar_reserva(id, inmueble_id):

    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE reservas
        SET estado = 'Cancelada'
        WHERE id = %s
    """, (id,))

    cursor.execute("""
        UPDATE inmuebles
        SET estado = 'Disponible'
        WHERE id = %s
    """, (inmueble_id,))

    mysql.connection.commit()
    cursor.close()

    flash('Reserva cancelada.', 'success')

    return redirect(url_for('reservas_admin'))

@app.route('/guardar_contacto', methods=['POST'])
def guardar_contacto():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        servicio = request.form.get('servicio')
        mensaje = request.form.get('mensaje')

        # DEBUG EN CONSOLA
        print("FORMULARIO RECIBIDO:")
        print(nombre, telefono, correo, servicio, mensaje)

        if not all([nombre, telefono, correo, servicio, mensaje]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('index'))

        add_contacto_mysql(
            mysql,
            nombre,
            telefono,
            correo,
            servicio,
            mensaje
        )

        flash('Tu solicitud fue enviada correctamente.', 'success')

    except Exception as e:
        print("ERROR AL GUARDAR CONTACTO:", e)
        flash(f'Error al guardar: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/admin_contactos')
def admin_contactos():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    pagina = request.args.get('page', 1, type=int)
    buscar = request.args.get('buscar', '')
    estado = request.args.get('estado', '')
    por_pagina = 10
    offset = (pagina - 1) * por_pagina
    actualizar_prioridades_mysql(mysql)
    cur = mysql.connection.cursor()

    sql = """
        SELECT SQL_CALC_FOUND_ROWS
            id,
            nombre,
            telefono,
            correo,
            servicio,
            mensaje,
            fecha_envio,
            estado,
            fecha_contacto
        FROM clientes_interesados
        WHERE 1=1
    """

    valores = []
    if buscar:

        sql += """
            AND (
                nombre LIKE %s
                OR correo LIKE %s
                OR telefono LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    # FILTRO
    if estado:

        sql += " AND estado = %s "

        valores.append(estado)

    sql += """
        ORDER BY
        CASE
            WHEN estado = 'Prioridad Alta' THEN 1
            WHEN estado = 'Pendiente' THEN 2
            WHEN estado = 'Contactado' THEN 3
            ELSE 4
        END,
        fecha_envio DESC
        LIMIT %s OFFSET %s
    """

    valores.extend([por_pagina, offset])
    cur.execute(sql, valores)
    contactos = cur.fetchall()

    # TOTAL
    cur.execute("SELECT FOUND_ROWS() AS total")
    total = cur.fetchone()['total']
    total_paginas = (total + por_pagina - 1) // por_pagina
    cur.close()
    contactos_procesados = []

    for c in contactos:

        fecha_envio = c['fecha_envio']
        fecha_contacto = c['fecha_contacto']
        estado_actual = c['estado']

        if estado_actual == "Contactado" and fecha_contacto:
            tiempo = fecha_contacto - fecha_envio
        else:
            tiempo = datetime.now() - fecha_envio

        contactos_procesados.append({
            "id": c['id'],
            "nombre": c['nombre'],
            "telefono": c['telefono'],
            "correo": c['correo'],
            "servicio": c['servicio'],
            "mensaje": c['mensaje'],
            "fecha_envio": fecha_envio,
            "estado": estado_actual,
            "tiempo": f"{tiempo.days} días"
        })

    return render_template(
        'admin_contactos.html',
        contactos=contactos_procesados,
        pagina=pagina,
        total_paginas=total_paginas,
        buscar=buscar,
        estado=estado
    )

@app.route('/marcar_contactado/<int:id>')
def marcar_contactado(id):
    marcar_contactado_mysql(mysql, id)
    flash("Cliente marcado como contactado", "success")
    return redirect(url_for('admin_contactos'))

@app.route('/clientes_constructora')
def clientes_constructora():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    pagina = request.args.get('page', 1, type=int)
    buscar = request.args.get('buscar', '')
    tipo = request.args.get('tipo', '')
    por_pagina = 10
    offset = (pagina - 1) * por_pagina
    cur = mysql.connection.cursor()

    sql = """
        SELECT SQL_CALC_FOUND_ROWS
            c.id,
            c.nombre,
            c.tipo,
            c.telefono,
            c.correo,
            p.nombre AS proyecto

        FROM clientes_constructora c

        LEFT JOIN cliente_proyecto cp
            ON c.id = cp.cliente_id

        LEFT JOIN proyectos_constructora p
            ON cp.proyecto_id = p.id

        WHERE 1=1
    """

    valores = []
    if buscar:

        sql += """
            AND (
                c.nombre LIKE %s
                OR c.correo LIKE %s
                OR c.telefono LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    # FILTRO TIPO
    if tipo:

        sql += " AND c.tipo = %s "

        valores.append(tipo)

    sql += """
        ORDER BY c.nombre ASC
        LIMIT %s OFFSET %s
    """

    valores.extend([por_pagina, offset])
    cur.execute(sql, valores)
    resultados = cur.fetchall()

    # TOTAL
    cur.execute("SELECT FOUND_ROWS() AS total")
    total = cur.fetchone()['total']
    total_paginas = (total + por_pagina - 1) // por_pagina
    cur.close()

    clientes_dict = {}

    for fila in resultados:

        cliente_id = fila['id']

        if cliente_id not in clientes_dict:

            clientes_dict[cliente_id] = {
                "nombre": fila['nombre'],
                "tipo": fila['tipo'],
                "telefono": fila['telefono'],
                "correo": fila['correo'],
                "proyectos": []
            }

        if fila['proyecto']:

            clientes_dict[cliente_id]["proyectos"].append(
                fila['proyecto']
            )

    clientes = list(clientes_dict.values())

    return render_template(
        'clientes_constructora.html',
        clientes=clientes,
        pagina=pagina,
        total_paginas=total_paginas,
        buscar=buscar,
        tipo=tipo
    )

@app.route('/guardar_cliente_constructora', methods=['POST'])
def guardar_cliente_constructora():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO clientes_constructora
        (nombre, tipo, telefono, correo)

        VALUES (%s, %s, %s, %s)
    """, (
        nombre,
        tipo,
        telefono,
        correo
    ))

    mysql.connection.commit()
    cur.close()
    flash('Cliente agregado correctamente.', 'success')

    return redirect(url_for('clientes_constructora'))

@app.route('/servicios_constructivos')
def servicios_constructivos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora")
    total_proyectos = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE tipo_trabajo = 'Obras civiles'")
    obras_civiles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE tipo_trabajo = 'Diseño estructural'")
    diseño_estructural = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE tipo_trabajo = 'Consultoría'")
    consultoria = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE tipo_trabajo = 'Interventoría'")
    interventoria = cur.fetchone()['total']

    cur.execute("""
        SELECT tipo_trabajo, COUNT(*) AS total
        FROM proyectos_constructora
        GROUP BY tipo_trabajo
        ORDER BY total DESC
    """)

    resultados = cur.fetchall()
    cur.close()

    # ICONOS Y DESCRIPCIONES
    iconos = {
        "Obras civiles": "fa fa-helmet-safety",
        "Construcción residencial": "fa fa-house",
        "Construcción comercial": "fa fa-building",
        "Diseño estructural": "fa fa-drafting-compass",
        "Interventoría": "fa fa-list-check",
        "Consultoría": "fa fa-file-signature",
        "Remodelación": "fa fa-screwdriver-wrench",
        "Urbanismo": "fa fa-city"
    }

    descripciones = {
        "Obras civiles": "Infraestructura, vías, puentes y obras públicas.",
        "Construcción residencial": "Viviendas, conjuntos y desarrollos habitacionales.",
        "Construcción comercial": "Locales, oficinas y espacios empresariales.",
        "Diseño estructural": "Cálculo, planificación y seguridad estructural.",
        "Interventoría": "Supervisión técnica, financiera y administrativa.",
        "Consultoría": "Asesoría profesional en ingeniería y ejecución.",
        "Remodelación": "Mejoras, adecuaciones y renovación de espacios.",
        "Urbanismo": "Planeación urbana y desarrollo territorial."
    }

    servicios = []

    for r in resultados:
        tipo = r['tipo_trabajo']

        servicios.append({
            "tipo": tipo,
            "total": r['total'],
            "icono": iconos.get(tipo, "fa fa-briefcase"),
            "descripcion": descripciones.get(tipo, "Servicio constructivo especializado.")
        })

    return render_template(
        'servicios_constructivos.html',
        total_proyectos=total_proyectos,
        obras_civiles=obras_civiles,
        diseño_estructural=diseño_estructural,
        interventoria=interventoria,
        consultoria=consultoria,
        servicios=servicios
    )

@app.route('/proyectos')
def proyectos_admin():

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM clientes_constructora
        ORDER BY nombre ASC
    """)

    clientes = cur.fetchall()
    buscar = request.args.get('buscar', '')
    estado = request.args.get('estado', '')
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 10
    offset = (pagina - 1) * por_pagina

    query = """
        SELECT *
        FROM proyectos_constructora
        WHERE 1=1
    """

    valores = []

    if buscar:

        query += """
            AND (
                nombre LIKE %s
                OR descripcion LIKE %s
                OR tipo_trabajo LIKE %s
            )
        """

        busqueda = f"%{buscar}%"

        valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    if estado:
        query += " AND estado = %s "
        valores.append(estado)

    query += " ORDER BY id DESC "
    count_query = """
        SELECT COUNT(*) AS total
        FROM proyectos_constructora
        WHERE 1=1
    """

    count_valores = []

    if buscar:
        count_query += """
            AND (
                nombre LIKE %s
                OR descripcion LIKE %s
                OR tipo_trabajo LIKE %s
            )
        """

        busqueda = f"%{buscar}%"
        count_valores.extend([
            busqueda,
            busqueda,
            busqueda
        ])

    if estado:

        count_query += " AND estado = %s "
        count_valores.append(estado)

    cur.execute(count_query, count_valores)
    total_registros = cur.fetchone()['total']

    total_paginas = (
        total_registros + por_pagina - 1
    ) // por_pagina
    query += " LIMIT %s OFFSET %s "

    valores.extend([
        por_pagina,
        offset
    ])

    cur.execute(query, valores)
    proyectos = cur.fetchall()

    return render_template(
        'Proyectos_confi.html',
        proyectos=proyectos,
        clientes=clientes,
        buscar=buscar,
        estado=estado,
        pagina=pagina,
        total_paginas=total_paginas
        )

@app.route('/crear_proyecto', methods=['POST'])
def crear_proyecto():
    nombre = request.form['nombre']
    tipo_trabajo = request.form['tipo_trabajo']
    descripcion = request.form['descripcion']
    estado = request.form['estado']
    cliente_id = request.form['cliente_id']

    cur = mysql.connection.cursor()

    # Crear proyecto con tipo de trabajo
    cur.execute("""
        INSERT INTO proyectos_constructora (nombre, tipo_trabajo, descripcion, estado)
        VALUES (%s, %s, %s, %s)
    """, (nombre, tipo_trabajo, descripcion, estado))

    proyecto_id = cur.lastrowid

    cur.execute("""
        INSERT INTO cliente_proyecto (cliente_id, proyecto_id)
        VALUES (%s, %s)
    """, (cliente_id, proyecto_id))

    mysql.connection.commit()
    cur.close()

    flash('Proyecto creado y vinculado al cliente correctamente.', 'success')
    return redirect(url_for('proyectos_admin'))

@app.route('/reporte_pdf')
def reporte_pdf():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session.get('rol') != 'admin':
        flash('No tienes permisos para generar reportes.', 'danger')
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COALESCE(SUM(valor_venta), 0) AS ingresos FROM ventas")
    ingresos = cur.fetchone()['ingresos']

    cur.execute("SELECT COUNT(*) AS total FROM ventas")
    total_ventas = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    inmuebles_disponibles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Reservado'")
    inmuebles_reservados = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Vendido'")
    inmuebles_vendidos = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM clientes_inmobiliaria")
    total_clientes = cur.fetchone()['total']

    cur.execute("""
        SELECT 
            v.fecha,
            c.nombre AS cliente,
            c.documento,
            i.titulo AS inmueble,
            i.ubicacion,
            v.valor_venta,
            v.anticipo,
            v.saldo,
            v.estado_pago,
            v.metodo_pago
        FROM ventas v
        INNER JOIN clientes_inmobiliaria c ON v.cliente_id = c.id
        INNER JOIN inmuebles i ON v.inmueble_id = i.id
        ORDER BY v.fecha DESC
        LIMIT 10
    """)
    ventas = cur.fetchall()

    cur.close()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    ancho, alto = letter

    # Encabezado
    pdf.setFillColor(colors.HexColor("#111111"))
    pdf.rect(0, alto - 90, ancho, 90, fill=True, stroke=False)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(2 * cm, alto - 45, "CiviWeb Manager")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, alto - 65, "Reporte general del sistema inmobiliario")

    pdf.setFillColor(colors.HexColor("#981313"))
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(2 * cm, alto - 125, "Reportes Generales")

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, alto - 145, f"Fecha de generacion: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Indicadores
    y = alto - 190

    indicadores = [
        ("Ingresos por ventas", f"COP ${ingresos or 0:,.0f}"),
        ("Ventas registradas", str(total_ventas or 0)),
        ("Inmuebles disponibles", str(inmuebles_disponibles or 0)),
        ("Inmuebles reservados", str(inmuebles_reservados or 0)),
        ("Inmuebles vendidos", str(inmuebles_vendidos or 0)),
        ("Clientes registrados", str(total_clientes or 0)),
    ]

    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(colors.HexColor("#981313"))
    pdf.drawString(2 * cm, y, "Indicadores principales")

    y -= 25

    for titulo, valor in indicadores:
        pdf.setFillColor(colors.HexColor("#f4f4f4"))
        pdf.roundRect(2 * cm, y - 8, 17 * cm, 28, 8, fill=True, stroke=False)

        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2.4 * cm, y + 2, titulo)

        pdf.setFillColor(colors.HexColor("#981313"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawRightString(18.5 * cm, y + 2, valor)

        y -= 38

    # Ultimas ventas
    y -= 10
    pdf.setFillColor(colors.HexColor("#981313"))
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(2 * cm, y, "Ultimas ventas registradas")

    y -= 25

    pdf.setFillColor(colors.HexColor("#981313"))
    pdf.rect(2 * cm, y - 5, 17 * cm, 22, fill=True, stroke=False)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(2.2 * cm, y + 2, "Fecha")
    pdf.drawString(4.0 * cm, y + 2, "Cliente")
    pdf.drawString(7.2 * cm, y + 2, "Inmueble")
    pdf.drawString(11.0 * cm, y + 2, "Valor")
    pdf.drawString(14.0 * cm, y + 2, "Estado")

    y -= 24

    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.black)

    for venta in ventas:
        if y < 80:
            pdf.showPage()
            y = alto - 80

        fecha = venta['fecha'].strftime('%d/%m/%Y') if venta['fecha'] else 'Sin fecha'
        cliente = str(venta['cliente'])[:22]
        inmueble = str(venta['inmueble'])[:24]
        valor = f"${(venta['valor_venta'] or 0):,.0f}"
        estado = str(venta['estado_pago'] or 'Sin estado')

        pdf.drawString(2.2 * cm, y, fecha)
        pdf.drawString(4.0 * cm, y, cliente)
        pdf.drawString(7.2 * cm, y, inmueble)
        pdf.drawString(11.0 * cm, y, valor)
        pdf.drawString(14.0 * cm, y, estado)

        y -= 18

    # Pie
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(2 * cm, 35, "Reporte generado automaticamente por CiviWeb Manager.")

    pdf.save()

    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_general.pdf'

    return response


if __name__ == '__main__':
    app.run(debug=True)