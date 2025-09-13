uv build && \
docker compose -f docker-compose.yaml down -v && \
docker build . -t extended_airflow:latest && \
docker compose -f docker-compose.yaml up -d
