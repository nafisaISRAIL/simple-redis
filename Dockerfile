FROM library/python:3.11-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app/. /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["python3", "main.py"]
