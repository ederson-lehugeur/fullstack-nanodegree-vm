# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Making as API Endpoint (GET Request)
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = [menuItem.serialize])

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
		flash("New Restaurant Created!")
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
		flash("Restaurant Successfully Edited!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant Successfully Deleted!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, item = restaurantToDelete)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(restaurant_id = restaurant_id, name = request.form['name'], description = request.form['description'], 
			price = request.form['price'], course = request.form['course'])
		session.add(newItem)
		session.commit()
		flash("New Menu Item Created!")
		return redirect(url_for('menu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
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
		flash("Menu Item Successfully Edited!")
		return redirect(url_for('menu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
	
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item Successfully Deleted!")
        return redirect(url_for('menu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = itemToDelete)
	
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)