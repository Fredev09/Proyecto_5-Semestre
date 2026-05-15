import email
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

app = Flask(__name__)
app.secret_key = 'contraseña01'

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
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_final'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#Configuracion e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'camila2001super@gmail.com'
app.config['MAIL_PASSWORD'] = 'sctagkciisazqpua'
app.config['MAIL_DEFAULT_SENDER'] = 'camila2001super@gmail.com'

mail = Mail(app)

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

    

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_usuario_by_username_mysql(mysql, username)
        if user and check_password_hash(user['password_hash'], password):
            if not es_contrasena_segura(password):
                flash('La contraseña no es segura. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.', 'danger')
                return render_template('login.html')
            if not user['email_confirmado']:
                flash('Debes confirmar tu correo electrónico antes de acceder.', 'danger')
                return render_template('login.html')
            session['usuario'] = username
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

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

    # Usuarios normales van a su propio dashboard
    if session.get('rol') == 'usuario':
        return redirect(url_for('dashboard_usuario'))

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

@app.route('/dashboard_usuario')
def dashboard_usuario():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Solo usuarios normales acceden aquí
    if session.get('rol') == 'admin':
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    inmuebles_disponibles = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM proyectos_constructora WHERE estado = 'Activo'")
    proyectos_activos = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles")
    total_inmuebles = cur.fetchone()['total']

    cur.execute("""
        SELECT id, titulo, tipo, ubicacion, precio, estado, imagen
        FROM inmuebles
        WHERE estado = 'Disponible'
        ORDER BY id DESC
        LIMIT 6
    """)
    inmuebles_recientes = cur.fetchall()

    cur.execute("""
        SELECT id, nombre, estado, ubicacion, fecha_inicio, fecha_fin
        FROM proyectos_constructora
        WHERE estado = 'Activo'
        ORDER BY id DESC
        LIMIT 3
    """)
    proyectos_recientes = cur.fetchall()

    cur.execute("SELECT email FROM usuarios WHERE username = %s", (session['usuario'],))
    user_row = cur.fetchone()
    email_usuario = user_row['email'] if user_row else ''

    cur.execute("""
        SELECT id, nombre, servicio, mensaje, fecha_envio, estado
        FROM clientes_interesados
        WHERE correo = %s
        ORDER BY fecha_envio DESC
        LIMIT 5
    """, (email_usuario,))
    mis_solicitudes = cur.fetchall()

    cur.close()

    return render_template(
        'dashboard_usuario.html',
        usuario=session['usuario'],
        email_usuario=email_usuario,
        inmuebles_disponibles=inmuebles_disponibles,
        proyectos_activos=proyectos_activos,
        total_inmuebles=total_inmuebles,
        inmuebles_recientes=inmuebles_recientes,
        proyectos_recientes=proyectos_recientes,
        mis_solicitudes=mis_solicitudes
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

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, rol, email_confirmado FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()

    return render_template('usuarios.html', usuarios=usuarios)


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

    cur.execute("SELECT * FROM inmueble_multimedia WHERE inmueble_id = %s", (id,))
    galeria = cur.fetchall()

    cur.close()

    return render_template('editar_inmueble.html', inmueble=inmueble)

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

@app.route('/ventas_admin')
def ventas_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COALESCE(SUM(valor_venta), 0) AS total FROM ventas")
    total_vendido = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE())")
    ventas_mes = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM ventas")
    inmuebles_vendidos = cur.fetchone()['total']

    cur.execute("""
        SELECT v.id, v.cliente, v.valor_venta, v.fecha, i.titulo
        FROM ventas v
        INNER JOIN inmuebles i ON v.inmueble_id = i.id
        ORDER BY v.fecha DESC
        LIMIT 5
    """)
    ultimas_ventas = cur.fetchall()

    cur.execute("""
        SELECT MONTH(fecha) AS mes, COUNT(*) AS total
        FROM ventas
        WHERE YEAR(fecha) = YEAR(CURDATE())
        GROUP BY MONTH(fecha)
        ORDER BY MONTH(fecha)
    """)
    ventas_grafico = cur.fetchall()

    cur.close()

    return render_template(
        'ventas_admin.html',
        total_vendido=total_vendido,
        ventas_mes=ventas_mes,
        inmuebles_vendidos=inmuebles_vendidos,
        ultimas_ventas=ultimas_ventas,
        ventas_grafico=ventas_grafico
    )

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

    cur.execute("""
        SELECT id, concepto, proveedor, valor, fecha,
               COALESCE(categoria, '') AS categoria,
               COALESCE(notas, '') AS notas
        FROM compras
        ORDER BY fecha DESC
    """)
    todas_compras = cur.fetchall()

    cur.close()

    return render_template(
        'compras_admin.html',
        total_compras=total_compras,
        total_proveedores=total_proveedores,
        compras_mes=compras_mes,
        ultimas_compras=ultimas_compras,
        compras_grafico=compras_grafico,
        todas_compras=todas_compras
    )

@app.route('/registrar_compra', methods=['POST'])
def registrar_compra():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    concepto  = request.form.get('concepto', '').strip()
    proveedor = request.form.get('proveedor', '').strip()
    valor     = request.form.get('valor', '0').strip()
    categoria = request.form.get('categoria', 'Otro').strip()
    fecha     = request.form.get('fecha', '').strip()
    notas     = request.form.get('notas', '').strip()

    if not concepto or not proveedor or not valor or not fecha:
        flash('Completa todos los campos obligatorios.', 'danger')
        return redirect(url_for('compras_admin'))

    try:
        valor = float(valor)
    except ValueError:
        flash('El valor ingresado no es válido.', 'danger')
        return redirect(url_for('compras_admin'))

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO compras (concepto, proveedor, valor, categoria, fecha, notas) VALUES (%s, %s, %s, %s, %s, %s)",
            (concepto, proveedor, valor, categoria, fecha, notas)
        )
        mysql.connection.commit()
        flash('Compra registrada correctamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al registrar la compra: {str(e)}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('compras_admin'))

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
def eliminar_compra(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM compras WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Compra eliminada correctamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar la compra: {str(e)}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('compras_admin'))

@app.route('/reportes_admin')
def reportes_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COALESCE(SUM(valor_venta), 0) AS total FROM ventas")
    ingresos = cur.fetchone()['total']

    cur.execute("SELECT COALESCE(SUM(valor), 0) AS total FROM compras")
    egresos = cur.fetchone()['total']

    utilidad = ingresos - egresos

    cur.execute("SELECT COUNT(*) AS total FROM inmuebles WHERE estado = 'Disponible'")
    inmuebles_disponibles = cur.fetchone()['total']

    cur.execute("""
        SELECT 
            SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END) AS disponibles,
            SUM(CASE WHEN estado = 'Reservado' THEN 1 ELSE 0 END) AS reservados,
            SUM(CASE WHEN estado = 'Vendido' THEN 1 ELSE 0 END) AS vendidos
        FROM inmuebles
    """)
    estado_inmuebles = cur.fetchone()

    cur.execute("""
        SELECT MONTH(fecha) AS mes, COALESCE(SUM(valor_venta), 0) AS ingresos
        FROM ventas
        WHERE YEAR(fecha) = YEAR(CURDATE())
        GROUP BY MONTH(fecha)
        ORDER BY MONTH(fecha)
    """)
    ingresos_grafico = cur.fetchall()

    cur.execute("""
        SELECT MONTH(fecha) AS mes, COALESCE(SUM(valor), 0) AS egresos
        FROM compras
        WHERE YEAR(fecha) = YEAR(CURDATE())
        GROUP BY MONTH(fecha)
        ORDER BY MONTH(fecha)
    """)
    egresos_grafico = cur.fetchall()

    cur.execute("""
        SELECT v.cliente, v.valor_venta, v.fecha, i.titulo
        FROM ventas v
        INNER JOIN inmuebles i ON v.inmueble_id = i.id
        ORDER BY v.fecha DESC
        LIMIT 8
    """)
    ultimas_ventas = cur.fetchall()

    cur.execute("""
        SELECT concepto, proveedor, valor, fecha
        FROM compras
        ORDER BY fecha DESC
        LIMIT 8
    """)
    ultimas_compras = cur.fetchall()

    cur.close()

    return render_template(
        'reportes_admin.html',
        ingresos=ingresos,
        egresos=egresos,
        utilidad=utilidad,
        inmuebles_disponibles=inmuebles_disponibles,
        estado_inmuebles=estado_inmuebles,
        ingresos_grafico=ingresos_grafico,
        egresos_grafico=egresos_grafico,
        ultimas_ventas=ultimas_ventas,
        ultimas_compras=ultimas_compras
    )

@app.route('/proyectos')
def proyectos_admin():
    proyectos = get_proyectos_mysql(mysql)
    return render_template('Proyectos_confi.html', proyectos=proyectos)


@app.route('/crear_proyecto', methods=['POST'])
def crear_proyecto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    estado = request.form['estado']

    add_proyecto_mysql(mysql, nombre, descripcion, estado)

    return redirect('/proyectos')


@app.route('/editar_proyecto/<int:id>')
def editar_proyecto(id):
    return render_template('editarPro.html')

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

@app.route('/reservas_admin')
def reservas_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template('reservas_admin.html')

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

    actualizar_prioridades_mysql(mysql)
    contactos = get_contactos_mysql(mysql)

    contactos_procesados = []

    for c in contactos:
        fecha_envio = c['fecha_envio']
        fecha_contacto = c['fecha_contacto']
        estado = c['estado']

        if estado == "Contactado" and fecha_contacto:
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
            "estado": estado,
            "tiempo": f"{tiempo.days} días"
        })

    return render_template(
        'admin_contactos.html',
        contactos=contactos_procesados
    )

@app.route('/marcar_contactado/<int:id>')
def marcar_contactado(id):
    marcar_contactado_mysql(mysql, id)
    flash("Cliente marcado como contactado", "success")
    return redirect(url_for('admin_contactos'))

if __name__ == '__main__':
    app.run(debug=True)
