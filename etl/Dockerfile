FROM python:3.10-slim

WORKDIR /app

COPY run_etl.py .

RUN pip install requests snowflake-connector-python

CMD ["python", "run_etl.py"]
