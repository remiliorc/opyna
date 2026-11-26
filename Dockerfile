FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# dependencias primero (mejor cache)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "opyna.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
