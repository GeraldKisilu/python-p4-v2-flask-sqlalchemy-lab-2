# testing/review_test.py
import pytest
from app import create_app
from models import db, Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert customer data
    customer1 = Customer(name='John Doe')
    db.session.add(customer1)

    # Insert item data
    item1 = Item(name='Sample Item', price=19.99)
    db.session.add(item1)

    # Commit the changes for the customer and item
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()

def test_can_be_instantiated():
    '''Review model in models.py'''
    r = Review()
    assert r
    assert isinstance(r, Review)

def test_has_comment():
    '''can be instantiated with a comment attribute.'''
    r = Review(comment='great product!')
    assert r.comment == 'great product!'

def test_can_be_saved_to_database(test_client, init_database):
    '''can be added to a transaction and committed to review table with comment column.'''
    with test_client.application.app_context():
        assert 'comment' in Review.__table__.columns
        r = Review(comment='great!')
        db.session.add(r)
        db.session.commit()

        # Add debugging information
        saved_review = db.session.query(Review).filter_by(id=r.id).first()
        assert saved_review, f"Review with id {r.id} was not found in the database."
        assert saved_review.comment == 'great!', f"Expected comment 'great!' but got '{saved_review.comment}'"

def test_is_related_to_customer_and_item(test_client, init_database):
    '''has foreign keys and relationships'''
    with test_client.application.app_context():
        assert 'customer_id' in Review.__table__.columns
        assert 'item_id' in Review.__table__.columns

        c = Customer.query.first()
        i = Item.query.first()

        r = Review(comment='great!', customer=c, item=i)
        db.session.add(r)
        db.session.commit()

        # check foreign keys
        assert r.customer_id == c.id
        assert r.item_id == i.id
        # check relationships
        assert r.customer == c
        assert r.item == i
        assert r in c.reviews
        assert r in i.reviews
