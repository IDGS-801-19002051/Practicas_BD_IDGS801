from flask import Flask, render_template, request
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from models import db                                 # crear instancia de clase bd
from models import Empleado 
import forms

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
 return render_template("404.html"),404

@app.route("/")
def indexado():
  create_form = forms.UserForm(request.form)
  return render_template("index.html", form=create_form)

@app.route("/index", methods=['GET', 'POST'])
def index():
  create_form = forms.UserForm(request.form)
  if request.method == 'POST':
    emp = Empleado(
      nombre = create_form.nombre.data,
      direccion = create_form.direccion.data,
      telefono = create_form.telefono.data,
      correo = create_form.email.data,
      sueldo = create_form.sueldo.data
      )
    # insert alumnos() values()
    db.session.add(emp)
    db.session.commit()
  return render_template("index.html", form=create_form)

@app.route("/ABC_Completo",methods={"GET","POST"})
def ABCompleto():
  emp_form=forms.UserForm(request.form)
  empleado=Empleado.query.all()
  
  return render_template("ABC_Completo.html", empleado=empleado)

if __name__ =="__main__":
  csrf.init_app(app)
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
  app.run(debug=True)   # Cambios en tiempo real 