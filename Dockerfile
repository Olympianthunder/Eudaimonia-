FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && \
    pip install fastapi uvicorn pyyaml
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "svc.app:app", "--host", "0.0.0.0", "--port", "8080"]
