FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

# Required environment variables (the app enforces these at startup). Provide them at runtime, e.g. with
#   docker run -e MONGO_URI=... -e DB_NAME=... -e FRONTEND_ORIGINS=...
# - MONGO_URI: MongoDB connection string
# - DB_NAME: database name to use
# - FRONTEND_ORIGINS: comma-separated allowed CORS origins (e.g. "http://localhost:3000")
ENV MONGO_URI=
ENV DB_NAME=
ENV FRONTEND_ORIGINS=

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
