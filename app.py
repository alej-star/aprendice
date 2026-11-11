import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "institucion"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aprendice")
    aprendices = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("index.html", aprendices=aprendices)

@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO aprendice (nombre, correo)
        VALUES (%s, %s)
    """
    cursor.execute(sql, (nombre, correo))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect("/")

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM aprendice WHERE id = %s",
        (id,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
