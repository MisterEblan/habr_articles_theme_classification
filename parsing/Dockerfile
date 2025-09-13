FROM apache/airflow:3.0.6

COPY requirements.txt .
COPY dist/pipeline_tools-0.2.1-py3-none-any.whl .

RUN pip install -r requirements.txt
RUN pip install pipeline_tools-0.2.1-py3-none-any.whl

