from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from sqlalchemy import extract, func
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from datetime import datetime
from models import db                                 # crear instancia de clase bd
from models import Empleado, Pizza, Registro
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

@app.route("/eliminar",methods={"GET","POST"})
def eliminar():
  create_form=forms.UserForm(request.form)
  if request.method=="GET":
    id=request.args.get("id")
    emp1 = db.session.query(Empleado).filter(Empleado.id == id).first()
    create_form.id.data=request.args.get("id")
    create_form.nombre.data=emp1.nombre
    create_form.direccion.data=emp1.direccion
    create_form.telefono.data=emp1.telefono
    create_form.email.data=emp1.correo
    create_form.sueldo.data=emp1.sueldo
  if request.method=='POST':
    id=create_form.id.data
    emp=Empleado.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for("ABCompleto"))
  return render_template("eliminar.html", form=create_form)

@app.route("/modificar",methods={"GET","POST"})
def modificar():
  create_form=forms.UserForm(request.form)
  if request.method=="GET":
    id=request.args.get("id")
    emp1 = db.session.query(Empleado).filter(Empleado.id == id).first()
    create_form.id.data=request.args.get("id")
    create_form.nombre.data=emp1.nombre
    create_form.direccion.data=emp1.direccion
    create_form.telefono.data=emp1.telefono
    create_form.email.data=emp1.correo
    create_form.sueldo.data=emp1.sueldo
  if request.method=='POST':
    id=create_form.id.data
    emp1 = db.session.query(Empleado).filter(Empleado.id == id).first()
    emp1.nombre=create_form.nombre.data
    emp1.direccion=create_form.direccion.data
    emp1.telefono=create_form.telefono.data
    emp1.correo=create_form.email.data
    emp1.sueldo=create_form.sueldo.data
    db.session.add(emp1)
    db.session.commit()
    return redirect(url_for("ABCompleto"))
  return render_template("modificar.html", form=create_form)

@app.route("/ABC_Completo",methods={"GET","POST"})
def ABCompleto():
  emp_form=forms.UserForm(request.form)
  empleado=Empleado.query.all()
  
  return render_template("ABC_Completo.html", empleado=empleado)



@app.route("/eliminarpizza",methods={"GET","POST"})
def eliminarpizza():
  if request.method=="GET":
    id=request.args.get("id")
    pizzaq=Pizza.query.get(id)
    db.session.delete(pizzaq)
    db.session.commit()
  return redirect(url_for("pizzas"))

@app.route("/pizzasguardar",methods={"GET","POST"})
def pizzasguardar():
  if request.method=='POST':
    create_form=forms.RegistroForm(request.form)
    reg = Registro(
      nombre = create_form.nombre.data,
      total = create_form.total.data,
      created_date = create_form.fecha.data
      )
    # insert alumnos() values()
    db.session.add(reg)
    db.session.commit()
    Pizza.query.delete()
    db.session.commit()
  return redirect(url_for("pizzas"))

@app.route("/pizzas",methods={"GET","POST"})
def pizzas():
  if request.args.get("tiempo") == None :
    tiempo = "checked"
    tiempo2 = ""
  elif request.args.get("tiempo") == "1": 
    tiempo = "checked"
    tiempo2 = ""
  else:
    tiempo = ""
    tiempo2 = "checked"
  
  if request.args.get("dia") == None :
    dia = ""
  else: 
    dia = request.args.get("dia")
    
  if request.args.get("mes") == None :
    mes = ""
  else: 
    mes = request.args.get("mes")
    
  fechas = {"":0, "domingo":1, "lunes":2, "martes":3, "miercoles":4, "jueves":5, "viernes":6, "sabado":7}
  meses = {"":0, "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}
  create_form=forms.PizzaForm(request.form)
  create_form2=forms.RegistroForm(request.form)
  pizzaq=Pizza.query.all()
  reg = Registro.query.filter(func.dayofweek(Registro.created_date) == fechas.get(dia,0)).all()
  reg2 = Registro.query.filter(extract('month', func.date(Registro.created_date)) == meses.get(mes, 0)).all()
  total = sum((pizza.tamaño + pizza.ingredientes)*pizza.numpizzas for pizza in pizzaq)
  total2 = sum(r.total for r in reg)
  total3 = sum(r.total for r in reg2)
  nombre=""
  id=request.args.get("id")
  if request.method=="GET":
    if id == None:
      pizzaqf=db.session.query(Pizza).first()
      create_form.id.data=0
      if pizzaqf is not None:
        create_form.nombre.data = pizzaqf.nombre
        nombre = pizzaqf.nombre
        create_form.direccion.data = pizzaqf.direccion
        create_form.telefono.data = pizzaqf.telefono
      else:
        create_form.nombre.data = ''
        nombre = ""
        create_form.direccion.data = ''
        create_form.telefono.data = ''
    else:
      pizzaqf = db.session.query(Pizza).filter(Pizza.id == id).first()
      create_form.id.data=request.args.get("id")
      create_form.nombre.data = pizzaqf.nombre
      create_form.direccion.data = pizzaqf.direccion
      create_form.telefono.data = pizzaqf.telefono
      valores = {40:0,80:1,120:2}
      create_form.tamaño.data = valores[pizzaqf.tamaño]
      create_form.numero.data = pizzaqf.numpizzas
      create_form.numero.data = pizzaqf.numpizzas
  if request.method=='POST':
    valores={0:40,1:80,2:120}
    mapeo = {0: "jamon", 1: "piña", 2: "champiñones"}
    idf=create_form.id.data
    matriz_nueva = [mapeo[i] for i in create_form.ingredientes.data]
    if idf=="0":
      pizza = Pizza(
      nombre = create_form.nombre.data,
      direccion = create_form.direccion.data,
      telefono = create_form.telefono.data,
      tamaño = valores[create_form.tamaño.data],
      ingredientes = len(create_form.ingredientes.data)*10,
      numpizzas = create_form.numero.data,
      ingredientesv = ', '.join(matriz_nueva)
      )
    else:
      pizza = db.session.query(Pizza).filter(Pizza.id == idf).first()
      pizza.nombre = create_form.nombre.data,
      pizza.direccion = create_form.direccion.data,
      pizza.telefono = create_form.telefono.data,
      pizza.tamaño = valores[create_form.tamaño.data],
      pizza.ingredientes = len(create_form.ingredientes.data)*10,
      pizza.numpizzas = create_form.numero.data,
      pizza.ingredientesv = ', '.join(matriz_nueva)
    # insert alumnos() values()
    db.session.add(pizza)
    db.session.commit()
    return redirect(url_for("pizzas"))
  return render_template("pizzas.html",form=create_form,form2=create_form2,pizzaq=pizzaq,reg=reg,reg2=reg2, total=total,total2=total2,total3=total3, nombre=nombre, dia=dia, mes=mes, tiempo=tiempo, tiempo2=tiempo2)

if __name__ =="__main__":
  csrf.init_app(app)
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
  app.run(debug=True)   # Cambios en tiempo real 