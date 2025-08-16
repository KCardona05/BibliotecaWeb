from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from config.conexion import conectar_db
from werkzeug.security import generate_password_hash
from flask import current_app as app
import MySQLdb

admin_bp = Blueprint('admin', __name__)
mysql = conectar_db()


@admin_bp.route('/admin')
def dashboard_admin():
    if session['usu_rol'] == 'administrador':
        conn = mysql.cursor()  # Usamos mysql.connection directamente
        conn.execute(
            "SELECT id_usuario, usu_nombre, usu_correo, usu_rol FROM usuarios")
        usuarios = conn.fetchall()
        conn.close()

        # Verificar el contenido de la variable usuarios
        # Esto te ayudará a verificar que se está recuperando correctamente
        print(usuarios)

        return render_template('admin/dashboard_admin.html', usuarios=usuarios)
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for('auth.login'))


@admin_bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    if  session['usu_rol'] == 'administrador':
        conn = mysql.cursor()
        conn.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        mysql.commit()
        conn.close()

        flash('Usuario actualizado exitosamente', 'success')

        return redirect(url_for('admin.dashboard_admin'))
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado'})


@admin_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_usuario(id):
    conn = mysql.cursor()
    conn.execute(
        "SELECT id_usuario, usu_nombre, usu_correo, password, usu_rol FROM usuarios WHERE id_usuario = %s", (id,))
    usuario_act = conn.fetchone()

    if not usuario_act:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    if request.method == 'POST':
        Nombreusu = request.form['txtname']
        Emailusu = request.form['txtemail']
        Passwordusu = request.form['txtpassword']
        Rolusu = request.form['txtrol']

        # Si no se cambia la contraseña, mantener la anterior
        if Passwordusu:
            pencrytado = generate_password_hash(
                Passwordusu, method='pbkdf2:sha256')
        else:
            pencrytado = usuario_act[3]  # Mantener la contraseña actual

        # Verificar si el correo ya existe
        conn.execute(
            "SELECT id_usuario FROM usuarios WHERE usu_correo = %s AND id_usuario != %s", (Emailusu, id))
        existe = conn.fetchone()

        if existe:
            conn.close()
            return jsonify({'success': False, 'message': 'El correo ya está registrado'}), 400

        try:
            conn.execute("UPDATE usuarios SET usu_nombre=%s, usu_correo=%s, password=%s, usu_rol=%s WHERE id_usuario=%s",
                         (Nombreusu, Emailusu, pencrytado, Rolusu, id))
            mysql.commit()
            conn.close()
            # Flash el mensaje de éxito y redirige al usuario
            flash('Usuario actualizado exitosamente', 'success')

            return redirect(url_for('admin.dashboard_admin'))
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': f'Error al actualizar: {str(e)}'}), 500

    # Si es un GET, mostrar el formulario con los datos actuales del usuario
    return render_template('admin/actualizar.html', usuario=usuario_act)


@admin_bp.route('/gestionar_prestamos')
def gestionar_prestamos():
    if session['usu_rol'] == 'administrador':
        conn = mysql.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("""
            SELECT p.id_prestamo, p.estado, u.usu_nombre, l.lib_titulo, p.fecha
            FROM prestamos p
            JOIN usuarios u ON p.usuario_id = u.id_usuario
            JOIN libros l ON p.libro_id = l.id_libro
        """)
        prestamos = conn.fetchall()
        conn.close()
        print(prestamos)
        return render_template('admin/gestionar_prestamos.html', prestamos=prestamos)
    else:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('auth.login'))


@admin_bp.route('/aprobar_prestamo/<int:idprestamo>', methods=['GET'])
def aprobar_prestamo(idprestamo):
    if  session['usu_rol'] == 'administrador':
        conn = mysql.cursor()
        conn.execute(
            "UPDATE prestamos SET estado = 'aprobado' WHERE id_prestamo = %s", (idprestamo,))
        mysql.commit()
        conn.close()
        return redirect(url_for('admin.gestionar_prestamos'))
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado'})


@admin_bp.route('/rechazar_prestamo/<int:idprestamo>', methods=['GET'])
def rechazar_prestamo(idprestamo):
    if  session['usu_rol'] == 'administrador':
        conn = mysql.cursor()
        conn.execute(
            "UPDATE prestamos SET estado = 'rechazado' WHERE id_prestamo = %s", (idprestamo,))
        mysql.commit()
        conn.close()
        return redirect(url_for('admin.gestionar_prestamos'))
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado'})


@admin_bp.route('/eliminar_prestamo/<int:idprestamo>', methods=['GET'])
def eliminar_prestamo(idprestamo):
    if  session['usu_rol'] == 'administrador':
        conn = mysql.cursor()

        # Obtenemos el ID del libro asociado al préstamo
        conn.execute(
            "SELECT libro_id FROM prestamos WHERE id_prestamo = %s", (idprestamo,))
        libro_id = conn.fetchone()
        
        # Verificamos si se encontró el libro
        if libro_id:
            # Actualizamos el estado del libro a disponible (lib_disponible = 1)
            conn.execute(
                "UPDATE libros SET lib_disponible = 1 WHERE id_libro = %s", (libro_id[0],))

            # Eliminamos el préstamo
            conn.execute(
                "DELETE FROM prestamos WHERE id_prestamo = %s", (idprestamo,))
            mysql.commit()
            conn.close()
            
            # Redirigimos a la página de gestión de préstamos
            return redirect(url_for('admin.gestionar_prestamos'))
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'Préstamo no encontrado'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado'})
