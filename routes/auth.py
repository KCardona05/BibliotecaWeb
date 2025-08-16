from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config.conexion import conectar_db
from flask import current_app as app

auth_bp = Blueprint('auth', __name__)
mysql = conectar_db()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('txtemail')
            password = data.get('txtpassword')
        else:
            email = request.form['txtemail']
            password = request.form['txtpassword']

        conn = mysql.cursor()
        conn.execute("SELECT id_usuario, usu_nombre, password, usu_rol FROM usuarios WHERE usu_correo = %s", (email,))
        usuario = conn.fetchone()
        conn.close()
        print(usuario)

        if usuario:
            session['id_usuario'] = usuario[0]
            session['usu_nombre'] = usuario[1]
            session['usu_rol'] = usuario[3]

            redir = url_for('admin.dashboard_admin') if usuario[3] == 'administrador' else url_for('user.dashboard_usuario')

            if request.is_json:
                return jsonify({'success': True, 'redirect_url': redir})
            return redirect(redir)
        else:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos'})
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('auth.login'))

    return render_template('admin/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrarusu():
    mensaje = None
    if request.method == 'POST':
        Nombreusu = request.form['txtname']
        Emailusu = request.form['txtemail']
        Passwordusu = request.form['txtpassword']
        pencrytado = generate_password_hash(Passwordusu, method='pbkdf2:sha256')

        conn = mysql.cursor()
        conn.execute("SELECT id_usuario FROM usuarios WHERE usu_correo = %s", (Emailusu,))
        existe = conn.fetchone()

        if existe:
            mensaje = "El correo ya está registrado"
        else:
            conn.execute("INSERT INTO usuarios(usu_nombre, usu_correo, password) VALUES (%s, %s, %s)",
                         (Nombreusu, Emailusu, pencrytado))
            mysql.commit()
            mensaje = "Usuario registrado con éxito"
        conn.close()
        return redirect(url_for('auth.registrarusu'))

    conn = mysql.cursor()
    conn.execute("SELECT id_usuario, usu_nombre, usu_correo, usu_rol FROM usuarios")
    usu = conn.fetchall()
    conn.close()
    return render_template('admin/registrar.html', usu=usu)
