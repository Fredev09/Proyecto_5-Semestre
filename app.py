from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re
import uuid
from db_utils_mysql import (
    add_usuario_mysql, update_email_mysql, set_email_confirmado_mysql,
    get_usuario_by_username_mysql, get_usuario_by_email_mysql, init_mysql_db
)


app = Flask(__name__)
app.secret_key = 'contraseña01'

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

def enviar_correo_simulado(destino, asunto, cuerpo):
    print(f"\n--- Simulación de envío de correo ---\nPara: {destino}\nAsunto: {asunto}\nCuerpo: {cuerpo}\n------------------------------\n")


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
            return render_template('register.html')
        if get_usuario_by_username_mysql(mysql, username):
            flash('El usuario ya existe.', 'danger')
            return render_template('register.html')
        if get_usuario_by_email_mysql(mysql, email):
            flash('El correo ya está registrado.', 'danger')
            return render_template('register.html')
        password_hash = generate_password_hash(password)
        add_usuario_mysql(mysql, username, password_hash, email, rol)
        # Simular envío de correo de confirmación
        token = str(uuid.uuid4())
        session['email_token'] = token
        session['email_to_confirm'] = email
        enlace = url_for('confirm_email', token=token, _external=True)
        enviar_correo_simulado(email, 'Confirma tu correo', f'Verifica tu correo haciendo clic aquí: {enlace}')
        flash('Registro exitoso. Confirma tu correo haciendo clic en el siguiente enlace:', 'success')
        flash(enlace, 'info')
        return redirect(url_for('mostrar_confirmacion'))
    return render_template('register.html')

# CONFIRMAR CORREO
@app.route('/confirm_email/<token>')
def confirm_email(token):
    if 'email_token' in session and session['email_token'] == token:
        set_email_confirmado_mysql(mysql, session['email_to_confirm'])
        mensaje = 'Correo confirmado correctamente. Ya puedes iniciar sesión.'
        session.pop('email_token', None)
        session.pop('email_to_confirm', None)
    else:
        mensaje = 'Enlace inválido o expirado.'
    return render_template('confirm_email.html', mensaje=mensaje)

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
            enviar_correo_simulado(email, 'Recupera tu contraseña', f'Restablece tu contraseña aquí: {enlace}')
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
        update_email_mysql(mysql, username, nuevo_email)
        flash('Correo actualizado correctamente.', 'success')
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
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
