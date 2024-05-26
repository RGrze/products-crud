from fastapi import FastAPI, Depends

from app.api.v1.routers import products
from app.api.v1.routers import users
from app.dependencies.auth import get_user


app = FastAPI()


app.include_router(
    products.router,
    prefix="/api/v1/products",
    tags=["products"],
    dependencies=[Depends(get_user)]
)


app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)
