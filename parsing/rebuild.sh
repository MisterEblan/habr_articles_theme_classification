uv build && \
docker build . -t extended_airflow:latest && \
cd ../airflow_dags/ && \
docker-compose down && docker-compose up -d && \
cd ../parsing
