from typing import Union, Dict
from fastapi import FastAPI

from common.errors.errors import StartupError
from api.v1.endpoints import create_app_v1

def create_app() -> FastAPI:
    version = "v1"
    setup_func = version_setup_dict[version]
    if setup_func is None:
        raise StartupError(f'version "{version}" is not a valid api version')
    
    app = setup_func()
    return app




version_setup_dict: Dict = {
    "v1": create_app_v1
}