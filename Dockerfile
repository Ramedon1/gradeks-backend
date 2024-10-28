FROM python:3.12-alpine

WORKDIR /opt

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_web.py"]