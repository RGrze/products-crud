from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.orm import Session

import app.api.v1.models.products as products_schema
import app.database.models.products as products_orm


def get_products(
    db: Session, page: int, page_size: int, label: str | None
) -> tuple[int, Sequence[products_orm.Product]]:
    """Returns paginated products with optional label filtering.

    Args:
        db: SQLAlchemy session
        page: Page number
        page_size: Number of items per page
        label: Label to filter products by

    Returns:
        Tuple of total items count and products on the page.

    """
    products_query = (
        select(products_orm.Product).offset((page - 1) * page_size).limit(page_size)
    )

    if label:
        products_query = products_query.join(products_orm.Product.labels).filter(
            products_orm.Label.name == label
        )

    products_on_page = db.execute(products_query).scalars().all()

    # Separate query to calculate the total count of products
    total_items_count_query = select(func.count()).select_from(products_orm.Product)

    if label:
        total_items_count_query = total_items_count_query.join(
            products_orm.Product.labels
        ).filter(products_orm.Label.name == label)

    total_items_count = db.execute(total_items_count_query).scalar_one()

    return total_items_count, products_on_page


def get_product(db: Session, product_id: int) -> products_orm.Product:
    """Get single product by ID.

    Args:
        db: SQLAlchemy session
        product_id: Product ID

    Returns:
        Product entity.

    """
    product_stmt = select(products_orm.Product).where(
        products_orm.Product.id == product_id
    )
    product = db.execute(product_stmt).scalar()
    if not product:
        raise ValueError("Product not found")

    return product


def create_product(
    db: Session, product_schema: products_schema.ProductIn
) -> products_orm.Product:
    """Create a new product.

    Args:
            db: SQLAlchemy session
            product_schema: Product schema

    Returns:
            Created product entity.

    """
    exists_stmt = select(products_orm.Product).where(
        products_orm.Product.name == product_schema.name
    )
    out = db.execute(exists_stmt).scalar()
    if out:
        raise ValueError("Product already exists")

    labels = set()
    if product_schema.labels:
        labels.update(_get_or_create_labels(db, product_schema.labels))

    product = products_orm.Product(
        name=product_schema.name,
        description=product_schema.description,
        stock=product_schema.stock,
        price=product_schema.price,
        labels=labels,
    )
    db.add(product)
    db.commit()

    return product


def delete_product(db: Session, product_id: int) -> None:
    """Delete a product.

    Args:
        db: SQLAlchemy session
        product_id: Product ID


    """
    try:
        product = get_product(db, product_id)
    except ValueError:
        return

    db.delete(product)
    db.commit()


def update_product(
    db: Session, product_id: int, product: products_schema.ProductUpdate
) -> products_orm.Product:
    """Update a product.

    Args:
        db: SQLAlchemy session
        product_id: Product ID
        product: Product schema for update

    Returns:
        Updated product entity.

    """
    try:
        product_orm = get_product(db, product_id)
    except ValueError:
        raise

    changed_attrs = product.model_dump(exclude_unset=True)
    for attr, value in changed_attrs.items():
        setattr(product_orm, attr, value)

    if product.labels_to_add:
        product_orm.labels.update(_get_or_create_labels(db, product.labels_to_add))

    if product.labels_to_remove:
        labels_to_remove = _get_or_create_labels(db, product.labels_to_remove)
        product_orm.labels.difference_update(labels_to_remove)

    db.commit()

    return product_orm


def _get_or_create_labels(
    db: Session, label_names: list[str]
) -> set[products_orm.Label]:
    existing_labels_stmt = select(products_orm.Label).where(
        products_orm.Label.name.in_(label_names)
    )
    existing_labels = db.execute(existing_labels_stmt).scalars().all()
    existing_label_names = {label.name for label in existing_labels}

    new_labels = set()
    for name in set(label_names) - existing_label_names:
        new_label = products_orm.Label(name=name)
        db.add(new_label)
        new_labels.add(new_label)

    db.flush()

    return set(existing_labels) | new_labels
