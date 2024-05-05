sh bin.dev/restart-mongo.sh

uvicorn src.main:app --reload --host 0.0.0.0 --port=9000