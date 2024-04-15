from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db' # Ubicación de la base de datos
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    output = []
    for item in items:
        item_data = {'id': item.id, 'name': item.name}
        output.append(item_data)
    return jsonify({'items': output})

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    item_data = {'id': item.id, 'name': item.name}
    return jsonify({'item': item_data})

@app.route('/item', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'})

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

