from wtforms import Form
from wtforms import StringField,TelField, IntegerField
from flask_wtf import FlaskForm
from wtforms import EmailField

from wtforms import validators

class UserForm(Form):
  id = IntegerField('id', [validators.number_range(min=1, max=20, message='Valor no valido')])
  nombre = StringField('nombre', validators=[
    validators.DataRequired(message='El nombre es requerido'),
    validators.length(min=4, max=20, message='Requiere min=4, max=10')
  ])
  direccion = StringField('direccion', validators=[
    validators.DataRequired(message='la direccion es requerida')
  ])
  telefono = StringField('telefono', validators=[ 
    validators.Email(message='El telefono es requerido')
  ])
  email = EmailField('correo', validators=[ 
    validators.Email(message='El email es requerido')
  ])
  sueldo = IntegerField('sueldo', validators=[ 
    validators.Email(message='El sueldo es requerido')
  ])