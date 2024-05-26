from typing import Annotated

from fastapi import APIRouter, Response, status, Query, Depends
from starlette.responses import JSONResponse

from sqlalchemy.orm import Session

import app.api.v1.services.products as products_srv
from app.api.v1.models.products import ProductOut, ProductIn, ProductUpdate
from app.database.db import get_db
from app.settings.app import app_settings

PAGE_SIZE = app_settings.PAGE_SIZE

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def get_products(
    db: Annotated[Session, Depends(get_db)],
    response: Response,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = PAGE_SIZE,
    label: Annotated[str | None, Query()] = None,
):
    total_count, products = products_srv.get_products(db, page, page_size, label)

    headers = {
        "X-Current-Page": str(page),
        "X-Page-Size": str(page_size),
        "X-Total-Count": str(total_count),
        "X-Page-Count": str((total_count + page_size - 1) // page_size),
    }
    response.headers.update(headers)

    return products


@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
def create_product(db: Annotated[Session, Depends(get_db)], product: ProductIn):
    try:
        return products_srv.create_product(db, product)
    except ValueError:
        return JSONResponse(
            content={"status": "Product already exists."},
            status_code=status.HTTP_409_CONFLICT,
        )


@router.get("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
def get_product(db: Annotated[Session, Depends(get_db)], product_id: int):
    try:
        return products_srv.get_product(db, product_id)
    except ValueError:
        return JSONResponse(
            content={"status": "Product not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.patch(
    "/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductOut
)
def update_product(
    db: Annotated[Session, Depends(get_db)], product_id: int, product: ProductUpdate
):
    try:
        return products_srv.update_product(db, product_id, product)
    except ValueError:
        return JSONResponse(
            content={"status": "Product not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(db: Annotated[Session, Depends(get_db)], product_id: int):
    products_srv.delete_product(db, product_id)
    return
