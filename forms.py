from wtforms import Form
from wtforms import StringField,TelField, IntegerField, RadioField, SelectMultipleField, widgets, HiddenField, DateField, DateTimeField
from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import NumberRange
from wtforms import validators

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
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
  
class PizzaForm(Form):
  id = HiddenField('', [validators.number_range(min=1, max=20, message='Valor no valido')])
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
  tamaño = RadioField('tamaño pizza', [validators.DataRequired("El campo es requerido")], choices=[(0,'Chica $40'), (1,'Mediana $80'), (2,'Grande $120')],default=1,coerce=int)
  ingredientes = MultiCheckboxField('Ingredientes', choices=[(0,'Jamon $10'), (1,'Piña $10'), (2,'Champiñones $10')],default=1,coerce=int)
  numero = StringField('num. pizzas', validators=[
    validators.DataRequired(message='el numero es requerido')
  ])
 
  
class RegistroForm(Form):
  nombre = HiddenField('', validators=[
    validators.DataRequired(message='El nombre es requerido'),
    validators.length(min=4, max=20, message='Requiere min=4, max=10')
  ])
  total = IntegerField('TOTAL: ', validators=[
    validators.DataRequired(message='el campo es requerido'),
    NumberRange(min=1, message='Intenta agregar algunos pedidos para obtener un total')
], render_kw={'readonly': True})
  
  fecha = DateField('fecha', validators=[ 
  validators.DataRequired(message='El campo es requerido')
  ])

