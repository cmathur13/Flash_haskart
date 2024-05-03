from app import app,db
from flask import request,jsonify
from app.models import Products

@app.before_first_request
def create_tables():
    db.create_all()



#Add new product (only admin)
@app.route('/product/<int:user_id>',methods=['POST'])
def add_product(user_id):
    data = request.get_json()
    print(data)
    new_product = Products(product_name=data['product_name'],
                           price=data['price'],
                           ratings=data['ratings'],
                           description=data['description'],
                           category=data['category'],
                           quantity=data['quantity'],
                           user_id=user_id)
    print("new product",new_product)
    print("new product",new_product.ratings)
    db.session.add(new_product)
    db.session.commit()
    return {"message":"Data added successfully"},201


#user can fetch product
@app.route('/product/<int:id>')
def get_product(id):
    product = Products.query.filter_by(id=id).first()
    if product:
        response={"product_name":product.product_name,
                    "price":product.price,
                    "ratings":product.ratings,
                    "category":product.category,
                    "description":product.description,
                    "quantity":product.quantity,
                    "id":product.id}
        return response,200
    return {"message":"coudent find product"},404

@app.route('/products')
def get_all_products():
    products = Products.query.all()
    output=[]
    for product in products:
        new_prod={"id":product.id,
                "product_name":product.product_name,
                    "price":product.price,
                    "ratings":product.ratings,
                    "category":product.category,
                    "description":product.description,
                    "quantity":product.quantity}
        output.append(new_prod)
    response = jsonify({'products' : output})
    return response



#Admin can delete products
@app.route('/product/<int:id>',methods=['DELETE'])
def delete_product(id):
    data = request.get_json()
    product = Products.query.filter_by(id=id).first() 
    print(product)
    db.session.delete(product)
    db.session.commit()
    return{"message":"product deleted successfully"}
    
    
    
    
#reduce products by given quantity
@app.route('/product/quantity/<int:quantity>/<int:id>',methods=['PUT'])
def update_product_quantity_by_value(quantity,id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return {"message":"couldn't find product"}, 404
    product.quantity= product.quantity-quantity
    db.session.commit()
    return {"message":"Quantity updated"}, 200


#get product by category
@app.route('/product/<string:category>')
def get_product_by_category(category):
    products = Products.query.filter(Products.category.like(category)).all()
    output=[]
    for product in products:
        new_prod={"id":product.id,
                "product_name":product.product_name,
                    "price":product.price,
                    "ratings":product.ratings,
                    "category":product.category,
                    "description":product.description,
                    "quantity":product.quantity}
        output.append(new_prod)
    response = jsonify({'products' : output})
    if len(output)==0:
        return{"message":"Products not found"},404
    return response


#Reduce quantity on successfull purchase
@app.route('/product/quantity/<int:id>',methods=['PUT'])
def update_product_quantity(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return {"message":"product not found"},404
    product.quantity= product.quantity-1
    db.session.commit()
    return {"message":"product updated successfully"}


@app.route('/product/rating', methods=['GET'])
def sort_product_by_rating():
    sorted_product = Products.query.order_by(Products.ratings.desc()).all()
    print("in rating")
    output = []

    for product in sorted_product:
        prod = {}
        prod['name'] = product.product_name
        prod['category'] = product.category
        prod['quantity'] = product.quantity
        prod['amount'] = product.price
        prod['rating']=product.ratings
        prod['description']=product.description
        output.append(prod)

    response = jsonify({'product' : output})
    return response

@app.route('/product/price', methods=['GET'])
def sort_product_by_price():
    sorted_product = Products.query.order_by(Products.price.desc()).all()

    output = []

    for product in sorted_product:
        prod = {}
        prod['name'] = product.product_name
        prod['category'] = product.category
        prod['quantity'] = product.quantity
        prod['amount'] = product.price
        prod['rating']=product.ratings
        prod['description']=product.description
        output.append(prod)

    response = jsonify({'product' : output})
    return response