FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install .[docs] fastapi uvicorn
CMD ["uvicorn", "eudaimonia.api:app", "--host", "0.0.0.0", "--port", "8000"]
