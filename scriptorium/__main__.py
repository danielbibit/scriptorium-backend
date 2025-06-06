from fastapi import FastAPI

import scriptorium.logging as logging
from scriptorium.auth import controller as auth_controller
from scriptorium.users import controller as users_controller

logging.configure_logging()

log = logging.get_logger()

app = FastAPI()

app.include_router(users_controller.router, tags=["Users"])
app.include_router(auth_controller.router, tags=["Auth"])
