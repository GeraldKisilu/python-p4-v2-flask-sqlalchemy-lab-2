import pytest # type: ignore
from app import create_app, db
from models import Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

class TestAssociationProxy:
    def test_has_association_proxy(self, test_client):
        with test_client.application.app_context():
            c = Customer(name='John')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items
