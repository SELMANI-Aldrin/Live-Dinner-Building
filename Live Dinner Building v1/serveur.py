from flask import Flask, render_template, request, redirect, session, url_for

import datetime

from random import randint

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'Borigo'

Food2Price = {
	"Oeuf":4.00,
	"Salade":7.50,
	"Tomates": 3.50,
	"Carrotes": 4.00,
	"Pizza": 8.50,
	"Sushi": 9.00,
	"Poisson" : 8.00,
	"Spaghetti" : 7.00,
	"Brie":5.00,
	"Gouda":3.50,
	"Camenbert":3.00,
	"Riccota":4.50,
	"Citron":8.50,
	"Coupe":6.50,
	"Eclairs":5.00,
	"Tiramisu": 6.00
}


@app.route('/')
def index():
	session['Starter'] = None
	session['Main'] = None
	session['Cheese'] = None
	session['Dessert'] = None
	return render_template("index.html")

@app.route('/Recipes')
def Recipes():
	return render_template("recipe.html")

@app.route('/Description')
def Description():
	return render_template('description.html')

@app.route('/SetName', methods=['GET'])
def SetName():
	result = request.args
	session['username'] = result['nom']
	return redirect(url_for('Starter'))

@app.route('/Rand')
def Rand():
	l=['Carrotes','Oeuf','Salade','Tomates', 'Poisson', 'Pizza', 'Sushi', 'Spaghetti','Brie','Camenbert','Gouda', 'Riccota', 'Tiramisu', 'Eclairs', 'Coupe', 'Citron']
	aa = randint(0,3)
	bb = randint(4,7)
	cc = randint(8,11)
	dd = randint(12,15)
	session['Starter'] = l[aa]
	session['Main'] = l[bb]
	session['Cheese'] = l[cc]
	session['Dessert'] = l[dd]
	return redirect(url_for('Bill'))
@app.route('/Step1', methods=['GET','POST'])
def Starter():
	user = session['username']
	starter = request.args.get('Starter')
	deselect = request.args.get('Désélectionner')
	if not type(starter) == 'NoneType': 
		session['Starter'] = starter
		stylename = str(starter) + ".css"
	if not deselect == None:
		session['Starter'] = None
	return render_template("Step1.html",username = user, Which_Starter=stylename)

@app.route('/Step2')
def Main():
	main = request.args.get('Main')
	deselect = request.args.get('Désélectionner')
	if not type(main) == 'Nonetype':
		session['Main'] = main
		stylename2 = str(main) + ".css"
	if not deselect == None:
		session['Main'] = None
	return render_template("Step2.html", Which_Main= stylename2)

@app.route('/Step3')
def Cheese():
	cheese = request.args.get('Cheese')
	deselect = request.args.get('Désélectionner')
	if not type(cheese) == 'NoneType':
		session['Cheese'] = cheese
		stylename3 = str(cheese) + ".css"
	if not deselect == None:
		session['Cheese'] = None
	return render_template("Step3.html", Which_Cheese= stylename3)

@app.route('/Step4')
def Dessert():
	dessert = request.args.get('Dessert')
	deselect = request.args.get('Désélectionner')
	if not type(dessert) == 'NoneType':
		session['Dessert'] = dessert
		stylename4 = str(dessert) + ".css"
	if not deselect == None:
		session['Dessert'] = None
	return render_template("Step4.html", Which_Dessert= stylename4)

@app.route('/Bill')
def Bill():
	date = datetime.datetime.now()
	d = datetime.date.today()
	h = date.hour
	m = date.minute

	if session['Main'] == None:
		main = "..."
		MainP = 0.0
	else:
		main = session['Main']
		MainP = Food2Price[main]
	if session['Starter'] == None:
		starter = "..."
		StarterP = 0.0
	else:	
		starter = session['Starter']
		StarterP = Food2Price[starter]
	if session['Dessert'] == None:
		dessert = "..."
		DessertP = 0.0
	else:
		dessert = session['Dessert']
		DessertP = Food2Price[dessert]
	if session['Cheese'] == None:
		cheese = "..."
		CheeseP = 0.0
	else:
		cheese = session['Cheese']
		CheeseP = Food2Price[cheese]

	Total = MainP + StarterP + DessertP + CheeseP
	if Total == 0.0 : 
		return redirect(url_for('index'))
	return render_template("Bill.html", FStarter=starter, FMain = main, FCheese = cheese, FDessert = dessert, FStarterPrice = StarterP, FMainPrice = MainP, FCheesePrice = CheeseP, FDessertPrice = DessertP, TotalPrice = Total, heure= h, minute= m, date = d )

if __name__ == '__main__':
	app.run(debug=True)