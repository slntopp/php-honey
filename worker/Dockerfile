FROM python:3.11.4-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY export.py outlets.yaml ./
COPY templates/ templates/

CMD ["python", "export.py", "--outlets", "outlets.yaml"]
