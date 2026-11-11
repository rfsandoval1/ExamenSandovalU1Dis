FROM python:3.12-slim

WORKDIR /app
COPY servidor.py .

EXPOSE 5000
CMD ["python", "servidor.py"]