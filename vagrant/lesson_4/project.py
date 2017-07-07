# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

'''
# Decorador
# Acrescentar ou remover responsabilidades a objetos individuais dinamicamente, de forma transparente.
@app.route('/')
@app.route('/hello')
def helloWorld():
	return "Hello World"
'''
	
'''
@app.route('/menu')
def menu():
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	output = ''
	for i in items:
		output += i.name
		output += '<br>'
		output += i.price
		output += '<br>'
		output += i.description
		output += '<br><br>'
	return output
'''

'''
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	output = ''
	for i in items:
		output += i.name
		output += '<br>'
		output += i.price
		output += '<br>'
		output += i.description
		output += '<br><br>'
	return output
'''

'''	
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = items)
'''

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)
	
@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("Restaurant %s created!" % newRestaurant.name)
		return redirect(url_for('restaurants'))
	else:
		return render_template('newRestaurant.html')
	
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant '%s' has been edited!" % editedRestaurant.name)
		return redirect(url_for('restaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        nameRestaurant = restaurantToDelete.name
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant '%s' has been deleted!" % nameRestaurant)
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, item = restaurantToDelete)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

'''
# Task 1: Create route for newMenuItem function here.
@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
	return "Page to create a new menu item. Task 1 complete!"
'''

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(restaurant_id = restaurant_id, name = request.form['name'], description = request.form['description'], 
			price = request.form['price'], course = request.form['course'])
		session.add(newItem)
		session.commit()
		flash("Menu item '%s' created!" % newItem.name)
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id)
	
'''
# Task 2: Create route for editMenuItem function here.
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "Page to edit a menu item. Task 2 complete!"
'''

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu item '%s' has been edited!" % editedItem.name)
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
	
'''
# Task 3: Create route for deleteMenuItem function here.
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "Page to delete a menu item. Task 3 complete!"
'''
	
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        nameItem = itemToDelete.name
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item '%s' has been deleted!" % nameItem)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = itemToDelete)
	
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)