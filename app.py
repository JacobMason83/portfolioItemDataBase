from flask import Flask, request, jsonify # imported it into your file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  + os.path.join(basedir, 'app.sqlite')  
db = SQLAlchemy(app)
ma = Marshmallow(app)
# creating the model for the database, with the id, title and content structure before initializing the class 
class Portfolio (db.Model) : 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique= False)
    content = db.Column(db.String(150), unique= False)
    def __init__(self, title, content): 
        self.title = title
        self.content = content 
# creating the schema for the class 
class PortfolioSchema(ma.Schema): 
    class Meta:
        fields = ('title', 'content')
        

portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)



# getting the crud functionality for the routes below:

# creating the post route 
@app.route('/portfolioItem', methods=['POST'])
def add_item():
    # requesting the data from site, or postman for posting the data
    title = request.json['title']
    content = request.json['content']
    # making the new item for the database
    new_item = Portfolio(title, content)
    
    db.session.add(new_item) # addin the new content to the database
    db.session.commit() # commiting the new content to the database 
    
    # returning the data that was just put into the database
    item = Portfolio.query.get(new_item.id)
    
    # returing the queried item so that you know what was placed in the database 
    return portfolio_schema.jsonify(item) 
#get one item route x
@app.route('/portfolioItem/<id>', methods=['GET'])
def get_item(id):
    #query the item 
    item = Portfolio.query.get(id)
    #returning the item so you know what is there
    return portfolio_schema.jsonify(item)

# get all of the items route x
@app.route('/portfolioItems', methods=['GET'])
def get_all_items ():
    #querying all the items 
    all_items = Portfolio.query.all()
    
    # dumping all the items into one variable 
    item_results = portfolios_schema.dump(all_items)
    
    #returing all of the items in the database and jsonifying them only need to jsonify it cause you already put it in a schema 
    return jsonify(item_results)
    


# Put/ patch or update the data x
@app.route('/portfolioItem/<id>', methods=['PUT'])
def update_item(id): 
    #getting the specific part you want to change 
    item = Portfolio.query.get(id)
    title = request.json['title']
    content = request.json['content']
    
    #overriding the data in the database
    item.title = title
    item.content = content
    # adding changes to the database
    db.session.commit()
    # return the data so you know what was changed 
    return portfolio_schema.jsonify(item)

# delete the data x
@app.route('/portfolioItem/<id>', methods=['DELETE'])
def delete_item(id): 
    # query the item you want to delete 
    item = Portfolio.query.get(id)
    
    #delete from the database 
    
    db.session.delete(item)
    db.session.commit()
    # return that action was completed 
    return "Thats my credo... No regrets...its deleted"
    


        

if __name__ == "__main__":
 app.run(debug=True)