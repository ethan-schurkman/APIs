from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = 'P4MNUQVZJ1L0YYHKIRDBVPUTEKJ5GBPLDXJHRCAI1ZK4CUDO'
foursquare_client_secret = '5AAZM0ORXDDHTXUIHVOKTZBA5OULTWYIUD10HF3N3GI4BALY'
google_api_key = 'AIzaSyDx5d3X6hwOI2NPOv2iVM3bzKaSG7SrETI'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  if request.method == 'GET':
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurants])
  if request.method == 'POST':
    location = request.args.get('location','')
    mealType = request.args.get('mealType','')
    print(location)
    print(mealType)
    restaurant_json = findARestaurant(mealType, location)
    restaurant = Restaurant(restaurant_name = restaurant_json['name'], restaurant_address = restaurant_json['address'], restaurant_image = restaurant_json['image'])
    session.add(restaurant)
    session.commit()
    return jsonify(restaurant = restaurant.serialize)
    
@app.route('/restaurants/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  if request.method == 'GET':
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    return jsonify(restaurant = restaurant.serialize)
    #return jsonify(restaurant = restaurant.serialize)
  if request.method == 'PUT':
    name = request.args.get('name','')
    location = request.args.get('location','')
    image = request.args.get('image', '')
    restaurant = session.query(Restaurant).filter_by(id = id).one()

    if name:
      restaurant.name = name
    if location:
      restaurant.location = location
    if image:
      restaurant.image = image

    session.add(restaurant)
    session.commit()
    return jsonify(restaurant = restaurant.serialize)
  if request.method == 'DELETE':
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.delete(restaurant)
    session.commit()
    return "Removed restaurant id:%s" % id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
