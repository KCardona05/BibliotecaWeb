# routes/user.py
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from config.conexion import conectar_db
import MySQLdb.cursors

user_bp = Blueprint('user', __name__)
mysql = conectar_db()

@user_bp.route('/')
def inicio_usuario():
    return redirect(url_for('user.dashboard_usuario'))

@user_bp.route('/dashboard')
def dashboard_usuario():
    if 'id_usuario' in session and session['usu_rol'] == 'usuario':
        return render_template('usuario/dashboard_usuario.html')
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for('auth.login'))


# ✅ Ver libros disponibles
@user_bp.route('/libros')
def ver_libros():
    if 'id_usuario' in session and session['usu_rol'] == 'usuario':
        cursor = mysql.cursor()
        cursor.execute("SELECT id_libro, lib_titulo, lib_autor, lib_disponible FROM libros WHERE lib_disponible = 1")
        libros = cursor.fetchall()
        cursor.close()
        print(libros)
        return render_template('usuario/libros.html', libros=libros)
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for('auth.login'))


# ✅ Solicitar préstamo
@user_bp.route('/solicitar_prestamo/<int:libro_id>')
def solicitar_prestamo(libro_id):
    if 'id_usuario' in session and session['usu_rol'] == 'usuario':
        usuario_id = session['id_usuario']
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO prestamos (usuario_id, libro_id, estado) VALUES (%s, %s, %s)", (usuario_id, libro_id, 'pendiente'))
        cursor.execute("UPDATE libros SET lib_disponible = 0 WHERE id_libro = %s", (libro_id,))
        mysql.commit()
        cursor.close()
        flash("Préstamo solicitado con éxito. Espera aprobación del administrador.", "success")
        return redirect(url_for('user.ver_libros'))
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for('auth.login'))


# ✅ Ver mis préstamos
@user_bp.route('/mis_prestamos')
def mis_prestamos():
    if 'id_usuario' in session and session['usu_rol'] == 'usuario':
        usuario_id = session['id_usuario']
        cursor = mysql.cursor()
        cursor.execute("""
            SELECT p.id_prestamo, l.lib_titulo, l.lib_autor, p.estado
            FROM prestamos p
            JOIN libros l ON p.libro_id = l.id_libro
            WHERE p.usuario_id = %s
        """, (usuario_id,))
        prestamos = cursor.fetchall()
        cursor.close()
        return render_template('usuario/prestamos.html', prestamos=prestamos)
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for('auth.login'))
