
ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-rc-slim
 
LABEL fly_launch_runtime="flask"
 
WORKDIR /app
 

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
 

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 

COPY . .
 

RUN mkdir -p uploads faiss_indexes
 
EXPOSE 8080
 
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --workers=2 --timeout=120"
 
CMD ["gunicorn", "app:app"]
 
