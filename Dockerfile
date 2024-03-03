FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
  pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD streamlit run Home.py --server.enableCORS false --server.enableXsrfProtection false
