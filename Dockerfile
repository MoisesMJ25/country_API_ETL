FROM apache/airflow:2.9.2
COPY requirements.txt /
RUN pip install --no-cache-dir apache-airflow==2.9.2 -r /requirements.txt
EXPOSE 8080
USER airflow
