FROM python:3.11

WORKDIR /app

COPY . .
COPY client_secret.json .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
ENV PORT=8080

HEALTHCHECK CMD curl --fail http://localhost:8080/ || exit 1

CMD ["uvicorn", "wedding_gallery_backend.app:app", "--host", "0.0.0.0", "--port", "8080"]
