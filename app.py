from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.users import user_bp
#from routes.general import general_bp

app = Flask(__name__)
app.secret_key = "3158519352"

@app.route('/usuario/dashboard')
def usuario_dashboard():
    return render_template('usuario/usuario.html')

@app.route('/administrador/dashboard')
def administrador_dashboard():
    return render_template('admin/dashboard_admin.html')


# Blueprints
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/usuario')
#app.register_blueprint(general_bp, url_prefix='/')

# No cache
@app.after_request
def agregar_headers_no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response

# Correr app
if __name__ == '__main__':
    app.run(debug=True)
