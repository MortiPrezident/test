FROM python:3.12
WORKDIR /app
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
COPY ./main ./test/main
COPY ./tests ./test/tests
ENV PYTHONPATH=/app


CMD ["python", "-m", "test.main.main"]