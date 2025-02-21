FROM python:3.12
workdir /app
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
COPY . ./test
ENV PYTHONPATH=/app


CMD ["python", "-m" "test/main/main"]