# app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate  # type: ignore
from flask_cors import CORS  # type: ignore
from models import db, Customer, Item, Message, Review

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return '<h1>Flask SQLAlchemy Lab 2</h1>'

    @app.route('/messages', methods=['GET'])
    def get_messages():
        messages = Message.query.all()
        return jsonify([message.to_dict() for message in messages])

    @app.route('/messages/<int:id>', methods=['GET'])
    def get_message_by_id(id):
        message = Message.query.get_or_404(id)
        return jsonify(message.to_dict())

    @app.route('/messages', methods=['POST'])
    def create_message():
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

    @app.route('/messages/<int:id>', methods=['PATCH'])
    def update_message(id):
        data = request.get_json()
        message = Message.query.get_or_404(id)
        if 'body' in data:
            message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())

    @app.route('/messages/<int:id>', methods=['DELETE'])
    def delete_message(id):
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return '', 204

    @app.route('/create_review', methods=['POST'])
    def create_review():
        data = request.get_json()
        new_review = Review(
            comment=data['comment'],
            customer_id=data['customer_id'],
            item_id=data['item_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)
