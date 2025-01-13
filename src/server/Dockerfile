FROM python:3.11-alpine

LABEL authors="scrvr"

ENV PYTHONDONTWRITEBYTECODE=1 \
		PYTHONUNBUFFERED=1 \
		SERVER_HOST=0.0.0.0 \
		SERVER_PORT=50000 \
		MAX_CONNECTIONS=2

WORKDIR /app/server

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $SERVER_PORT

WORKDIR /app

CMD ["sh", "-c", "python3 -m server -H $SERVER_HOST -p $SERVER_PORT -m $MAX_CONNECTIONS"]