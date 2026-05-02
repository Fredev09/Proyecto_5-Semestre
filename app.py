import email

from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app
from flask_mysqldb import MySQL
import random
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import re
import uuid
from db_utils_mysql import (
    add_usuario_mysql, update_email_mysql, set_email_confirmado_mysql,
    get_usuario_by_username_mysql, get_usuario_by_email_mysql, init_mysql_db
)


app = Flask(__name__)
app.secret_key = 'contraseña01'

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

# Inicializar tabla si no existe
with app.app_context():
    init_mysql_db(mysql)


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
            token = str(uuid.uuid4())
            session['recover_token'] = token
            session['recover_user'] = user['username']
            enlace = url_for('reset_password', token=token, _external=True)
           

            flash('Se ha enviado un enlace de recuperación. Haz clic en el siguiente enlace para restablecer tu contraseña:', 'success')
            flash(enlace, 'info')
            return redirect(url_for('mostrar_recuperacion'))
        else:
            flash('Correo no encontrado.', 'danger')
    return render_template('recover.html')

# RESTABLECER CONTRASEÑA
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if 'recover_token' not in session or session['recover_token'] != token:
        flash('Enlace inválido o expirado.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('reset_password.html')

        if not es_contrasena_segura(password):
            flash('La contraseña no es segura.', 'danger')
            return render_template('reset_password.html')
        password_hash = generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET password_hash = %s WHERE username = %s', (password_hash, session['recover_user']))
        mysql.connection.commit()
        cur.close()
        session.pop('recover_token', None)
        session.pop('recover_user', None)
        flash('Contraseña restablecida correctamente.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

# MODIFICAR CORREO (solo admin o el propio usuario)
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
    return render_template('dashboard.html', usuario=session['usuario'], rol=session.get('rol', 'usuario'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada correctamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
