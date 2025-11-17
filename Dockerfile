FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ToDoApp.py .

EXPOSE 7000

ENV FLASK_APP=ToDoApp.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "--workers", "4", "ToDoApp:app"]