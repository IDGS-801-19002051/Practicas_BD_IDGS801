from flask_sqlalchemy import SQLAlchemy
import datetime                         # funcion para crear tabla

db = SQLAlchemy()

class Empleado(db.Model):
  __tablename__ = 'empleados'                       # nombre a tabla
  id = db.Column(db.Integer, primary_key = True)
  nombre = db.Column(db.String(50))               # columnas varchar =  string
  direccion = db.Column(db.String(50))
  telefono = db.Column(db.String(50))
  correo = db.Column(db.String(50))
  sueldo = db.Column(db.Float(50))