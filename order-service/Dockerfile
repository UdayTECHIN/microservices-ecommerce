FROM python:3.12-slim

WORKDIR /app

COPY app.py .

RUN pip install flask requests psycopg[binary]

EXPOSE 8002

CMD ["python", "app.py"]


