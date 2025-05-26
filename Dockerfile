FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT app:app 