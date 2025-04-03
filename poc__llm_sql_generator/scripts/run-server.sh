#!/bin/sh
uvicorn --app-dir ./ "main:create_app" --factory --reload --host=0.0.0.0 --port=8000