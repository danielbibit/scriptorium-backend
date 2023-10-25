import logging

from fastapi import FastAPI

from scriptorium.auth import controller as auth_controller
from scriptorium.logging import configure_logging
from scriptorium.users import controller as users_controller

configure_logging()

log = logging.getLogger(__name__)

app = FastAPI()

app.include_router(users_controller.router, tags=["Users"])
app.include_router(auth_controller.router, tags=["Auth"])
