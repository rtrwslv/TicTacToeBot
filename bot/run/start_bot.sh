#!/usr/bin/env bash

if [[ "$WEBHOOK_MODE" == "True" && -n "$WEBHOOK_PORT" && -n "$WEBHOOK_DOMAIN" ]]; then
    exec uvicorn main_webhook:create_app --host 0.0.0.0 --port $WEBHOOK_PORT --factory
else
    poetry run python -m main
fi
