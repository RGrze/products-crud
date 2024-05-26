import pytest

from app.database.models.products import Product


@pytest.fixture
def fill_products(db_session):
    products = [
        Product(
            name=f"Product {i}",
            description=f"Description {i}",
            stock=i,
            price=i*100,
        )
        for i in range(1, 20)
    ]

    db_session.add_all(products)
    db_session.commit()


class TestProductsEndpoints:
    def test_get_products_returns_paginated_result(self, http_client, fill_products):
        response = http_client.get("/api/v1/products/?page=3&page_size=5")
        response_headers = response.headers

        assert response.status_code == 200
        assert len(response.json()) == 5
        assert response_headers["X-Current-Page"] == "3"
        assert response_headers["X-Page-Size"] == "5"
        assert response_headers["X-Total-Count"] == "19"
        assert response_headers["X-Page-Count"] == "4"


    def test_post_products(self, http_client):
        body = {
            "name": "Product 123",
            "description": "Description",
            "stock": 10,
            "price": 100,
        }

        response = http_client.post(
            "/api/v1/products/", json=body
        )
        response_json = response.json()

        assert response.status_code == 201
        for key in body:
            assert response_json[key] == body[key]


    def test_post_products_with_already_existing_name(self, http_client, fill_products):
        body = {
            "name": "Product 1",
            "description": "Description",
            "stock": 10,
            "price": 100,
        }

        response = http_client.post(
            "/api/v1/products/", json=body
        )

        assert response.status_code == 409


    def test_get_product(self, http_client, fill_products):
        response = http_client.get("/api/v1/products/1/")
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["id"] == 1
        assert response_json["name"] == "Product 1"


    def test_get_product_not_found(self, http_client):
        response = http_client.get("/api/v1/products/200/")

        assert response.status_code == 404


    def test_patch_product(self, http_client, fill_products):
        body = {
            "name": "Product #1",
            "description": "Description has changed",
            "price": 5,
            "labelsToAdd": ["label1", "label2"],
        }

        response = http_client.patch("/api/v1/products/1/", json=body)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["id"] == 1
        assert response_json["name"] == "Product #1"
        assert response_json["description"] == "Description has changed"
        assert response_json["price"] == 5
        assert response_json["stock"] == 1

        obj_labels = {label["name"] for label in response_json["labels"]}
        assert {"label1", "label2"} == obj_labels


    def test_patch_product_not_found(self, http_client):
        body = {
            "name": "Product #X",
        }

        response = http_client.patch("/api/v1/products/333/", json=body)

        assert response.status_code == 404


    def test_delete_product(self, http_client, fill_products):
        response = http_client.delete("/api/v1/products/1/")

        assert response.status_code == 204

        response_get = http_client.get("/api/v1/products/1/")

        assert response_get.status_code == 404


    def test_delete_product_multiple_calls_returns_204(self, http_client, fill_products):
        for _ in range(3):
            response = http_client.delete("/api/v1/products/1/")
            assert response.status_code == 204
