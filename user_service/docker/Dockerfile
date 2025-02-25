FROM python:3.11-slim
WORKDIR /app
COPY user_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY user_service/ user_service/
CMD ["python", "-m", "user_service.app.main"]