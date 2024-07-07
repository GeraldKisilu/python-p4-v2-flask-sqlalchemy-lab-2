import pytest
from app import create_app, db
from models import Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    with flask_app.app_context():
        db.create_all()

    yield testing_client

    with flask_app.app_context():
        db.drop_all()

    ctx.pop()

class TestSerialization:
    '''models in models.py'''

    def test_customer_is_serializable(self, test_client):
        '''customer is serializable'''
        with test_client.application.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()
            customer_dict = c.to_dict()

            # Debugging: print the serialized customer
            print("Serialized Customer:", customer_dict)

            assert 'id' in customer_dict
            assert customer_dict['name'] == 'Phil'
            assert 'reviews' in customer_dict
            assert 'customer' not in customer_dict['reviews'][0]  # Ensure no circular reference

    def test_item_is_serializable(self, test_client):
        '''item is serializable'''
        with test_client.application.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()

            # Debugging: print the serialized item
            print("Serialized Item:", item_dict)

            assert 'id' in item_dict
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert 'reviews' in item_dict
            assert 'item' not in item_dict['reviews'][0]  # Ensure no circular reference

    def test_review_is_serializable(self, test_client):
        '''review is serializable'''
        with test_client.application.app_context():
            c = Customer(name='Phil')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()

            # Debugging: print the serialized review
            print("Serialized Review:", review_dict)

            assert 'id' in review_dict
            assert 'customer' in review_dict
            assert 'item' in review_dict
            assert review_dict['comment'] == 'great!'
            assert 'reviews' not in review_dict['customer']  # Ensure no circular reference
            assert 'reviews' not in review_dict['item']  # Ensure no circular reference
