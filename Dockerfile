FROM python:3.12-alpine

WORKDIR /opt

# Install build dependencies using apk
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

CMD ["python", "run.py"]
