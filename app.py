
import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# CONEXIÓN A MYSQL (RAILWAY)
def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", os.getenv("DB_HOST", "localhost")),
        user=os.getenv("MYSQLUSER", os.getenv("DB_USER", "root")),
        password=os.getenv("MYSQLPASSWORD", os.getenv("DB_PASSWORD", "")),
        database=os.getenv("MYSQLDATABASE", os.getenv("DB_NAME", "institucion")),
        port=int(os.getenv("MYSQLPORT", os.getenv("DB_PORT", "3306")))
    )


# PÁGINA PRINCIPAL
@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM aprendices")
    aprendices = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("index.html", aprendices=aprendices)


# REGISTRAR APRENDIZ
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"]
    correo = request.form["correo"]

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO aprendices (nombre, correo)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (nombre, correo))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio"))


# ELIMINAR APRENDIZ
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM aprendices WHERE id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio"))


# INICIAR APLICACIÓN
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=puerto)
