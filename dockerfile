FROM python:3.12
COPY requirements.txt ./requirements.txt
workdir /home

RUN pip install -r requirements.txt
COPY . ./test
ENV PYTHONPATH=/home


CMD ["python", "-m" "test/main/main"]