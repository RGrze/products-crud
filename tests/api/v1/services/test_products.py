import pytest
from sqlalchemy import select

from app.api.v1.models.products import ProductIn, ProductUpdate
from app.api.v1.services.products import create_product, get_product, delete_product, update_product
from app.database.models.products import Product


@pytest.fixture
def product(db_session):
    p = Product(
        name="Product 123",
        description="Description",
        stock=10,
        price=100,
    )
    db_session.add(p)
    db_session.commit()

    yield p


class TestProducts:
    def test_get_product(self, db_session, product):
        output = get_product(db_session, product.id)

        assert isinstance(output, Product)
        assert output.name == product.name

    def test_get_product_raises_on_non_existent_product(self, db_session):
        with pytest.raises(ValueError):
            get_product(db_session, 123)

    def test_create_product_no_labels(self, db_session):
        product_in: ProductIn = ProductIn(
            name="Product",
            description="Description",
            stock=10,
            price=100,
        )

        output = create_product(db_session, product_in)

        assert isinstance(output, Product)
        self._assert_product(output, product_in)
        assert len(output.labels) == 0

    def test_create_product_also_creates_missing_labels(self, db_session):
        product_in: ProductIn = ProductIn(
            name="Product",
            description="Description",
            stock=10,
            price=100,
            labels=["label1", "label2"],
        )

        output = create_product(db_session, product_in)

        assert isinstance(output, Product)
        self._assert_product(output, product_in)

        output_labels = {label.name for label in output.labels}
        assert output_labels == set(product_in.labels)

    def test_create_product_on_existing_name(self, db_session):
        product_in: ProductIn = ProductIn(
            name="Product",
            description="Description",
            stock=10,
            price=100,
        )
        product_in2: ProductIn = ProductIn(
            name="Product",
            description="Other Description",
            stock=123,
            price=444,
        )

        create_product(db_session, product_in)

        with pytest.raises(ValueError):
            create_product(db_session, product_in2)

    def test_delete_product(self, db_session, product):
        delete_product(db_session, product.id)

        stmt = select(Product).where(Product.id == product.id)
        output = db_session.execute(stmt).scalar()

        assert output is None

    def test_update_product(self, db_session, product):
        product_in: ProductUpdate = ProductUpdate(
            description="Description was modified",
            stock=10,
        )

        output = update_product(db_session, product.id, product_in)

        assert isinstance(output, Product)
        assert output.name == product.name
        assert output.description == product_in.description
        assert output.stock == product_in.stock

    def _assert_product(self, product_orm: Product, product_in: ProductIn):
        assert product_orm.name == product_in.name
        assert product_orm.description == product_in.description
        assert product_orm.stock == product_in.stock
        assert product_orm.price == product_in.price
