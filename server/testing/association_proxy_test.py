from app import create_app, db
from server.models import Customer, Item, Review


class TestAssociationProxy:
    def test_has_association_proxy(self):
        app = create_app()
        with app.app_context():
            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items
